#!/usr/bin/env python3
"""Genera la voz de un guion con Azure Speech y los tiempos de cada palabra.

El guion es un .txt con tramos separados por una linea en blanco; cada tramo
ira con su lamina. Cada linea del guion es una frase. El texto NO se toca:
los subtitulos salen de el tal cual; Azure solo pone el audio.

Uso:
  python3 herramientas/voz.py guiones/04_precio_ca.txt --idioma ca --salida .tmp/04_precio_ca
  python3 herramientas/voz.py ... --simulado      (audio mudo, solo para pruebas)

La clave:
  - en la nube de Claude la pone el propio entorno (secreto de red con la
    cabecera Ocp-Apim-Subscription-Key): el script no la ve ni la necesita;
  - en un ordenador normal, se lee de AZURE_SPEECH_KEY (variable o .env).
Region: AZURE_SPEECH_REGION, por defecto swedencentral.

Como se sacan los tiempos: se pide a Azure una frase cada vez, asi se sabe
exactamente donde empieza y acaba cada frase. Dentro de la frase, las
palabras se reparten por silabas y, si hay comas, se anclan a las pausas
reales del audio.

Deja <salida>.wav y <salida>.json.
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np

VOCES = {"ca": "ca-ES-EnricNeural", "es": "es-ES-Tristan:DragonHDLatestNeural"}
LOCALE = {"ca": "ca-ES", "es": "es-ES"}
SR = 48000
PAUSA_FRASE = 0.18        # silencio entre frases de un mismo tramo (s)
PAUSA_TRAMO = 0.32        # silencio entre tramos (s)
MARGEN = 0.09             # silencio que se deja al recortar cada frase (s)
VELOCIDAD = "+20%"        # ritmo de la voz (1,2x, elegido por Pablo)


def lee_env(raiz):
    f = raiz / ".env"
    if f.exists():
        for linea in f.read_text(encoding="utf-8").splitlines():
            if "=" in linea and not linea.lstrip().startswith("#"):
                k, v = linea.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def lee_guion(ruta):
    texto = Path(ruta).read_text(encoding="utf-8").replace("\r\n", "\n")
    tramos = [[l.strip() for l in t.split("\n") if l.strip()]
              for t in re.split(r"\n\s*\n", texto) if t.strip()]
    if not tramos:
        sys.exit("El guion esta vacio.")
    return tramos


def para_hablar(texto):
    """Lo que se le manda a la voz. Mismas palabras y en el mismo orden que el
    guion (los subtitulos siguen saliendo del guion tal cual); solo cambia la
    puntuacion que hace titubear a la voz."""
    t = re.sub(r"[«»\"“”]", "", texto)
    t = re.sub(r":(\s)", r",\1", t)          # «Uno: tienes...» -> «Uno, tienes...»
    return t


def pide_audio(frase, idioma, voz):
    region = os.environ.get("AZURE_SPEECH_REGION", "swedencentral")
    ssml = (f'<speak version="1.0" xml:lang="{LOCALE[idioma]}"><voice name="{voz}">'
            f'<prosody rate="{VELOCIDAD}">{escape(frase)}</prosody></voice></speak>')
    cab = {"Content-Type": "application/ssml+xml",
           "X-Microsoft-OutputFormat": "riff-48khz-16bit-mono-pcm",
           "User-Agent": "dissenywebpm-videos"}
    if os.environ.get("AZURE_SPEECH_KEY"):
        cab["Ocp-Apim-Subscription-Key"] = os.environ["AZURE_SPEECH_KEY"]
    req = urllib.request.Request(
        f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1",
        data=ssml.encode("utf-8"), headers=cab, method="POST")
    for intento in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                datos = r.read()
            break
        except urllib.error.HTTPError as e:
            # 429 (cupo por minuto) y errores del servidor: esperar y repetir
            if e.code in (429, 500, 502, 503, 504) and intento < 5:
                time.sleep(5 * 2 ** intento)
                continue
            pista = {401: "clave incorrecta o no configurada",
                     429: "demasiadas peticiones o cupo gratis agotado"}.get(e.code, "")
            sys.exit(f"Azure ha respondido {e.code} {pista}".strip())
        except (urllib.error.URLError, TimeoutError):
            if intento == 5:
                raise
            time.sleep(5 * 2 ** intento)
    with wave.open(io.BytesIO(datos)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)


def energia(pcm, ventana=0.01):
    n = int(SR * ventana)
    m = len(pcm) // n
    x = pcm[:m * n].astype(np.float32).reshape(m, n) / 32768
    return 20 * np.log10(np.sqrt((x ** 2).mean(axis=1)) + 1e-9), ventana


def recorta(pcm, umbral=-45):
    db, v = energia(pcm)
    voz = np.where(db > umbral)[0]
    if not len(voz):
        return pcm
    a = max(0, int((voz[0] * v - MARGEN) * SR))
    b = min(len(pcm), int(((voz[-1] + 1) * v + MARGEN) * SR))
    return pcm[a:b]


def pausas(pcm, umbral=-40, minimo=0.09):
    """Centros de las pausas internas (silencios de al menos `minimo` s)."""
    db, v = energia(pcm)
    calla = db < umbral
    out, ini = [], None
    for i, c in enumerate(calla):
        if c and ini is None:
            ini = i
        elif not c and ini is not None:
            if (i - ini) * v >= minimo and ini > 0:
                out.append(((ini + i) / 2 * v, ini * v, i * v))
            ini = None
    return out


def peso(palabra):
    return max(1, len(re.findall(r"[aeiouàèéíïòóúü]+", palabra.lower())))


def reparte(palabras, t0, t1):
    """Reparte [t0, t1] entre palabras segun sus silabas."""
    pesos = [peso(p) for p in palabras]
    total, t, out = sum(pesos), t0, []
    for p, w in zip(palabras, pesos):
        d = (t1 - t0) * w / total
        out.append((t, t + d))
        t += d
    return out


def tiempos_frase(frase, pcm):
    """Tiempos de cada palabra dentro de una frase ya recortada."""
    palabras = frase.split()
    dur = len(pcm) / SR
    trozos, cur = [], []
    for i, p in enumerate(palabras):
        cur.append(p)
        # cada signo de puntuacion (coma o punto) deja una pausa en la voz
        if i < len(palabras) - 1 and re.search(r"[,;:.?!»]$", p):
            trozos.append(cur)
            cur = []
    if cur:
        trozos.append(cur)
    ps = pausas(pcm)
    # Cada signo de puntuacion se ancla a la pausa real mas cercana al punto
    # donde caeria si el habla fuera regular (por silabas). Si no hay pausas
    # suficientes, se reparte todo por silabas.
    if len(trozos) > 1 and len(ps) >= len(trozos) - 1:
        total = sum(peso(p) for p in palabras)
        acum, esperados = 0, []
        for tr in trozos[:-1]:
            acum += sum(peso(p) for p in tr)
            esperados.append(MARGEN + (dur - 2 * MARGEN) * acum / total)
        elegidas, libres = [], list(ps)
        for e in esperados:
            mejor = min(libres, key=lambda x: abs(x[0] - e))
            elegidas.append(mejor)
            libres.remove(mejor)
        elegidas.sort()
        limites = [(MARGEN, None)]
        for _, pa, pb in elegidas:
            limites[-1] = (limites[-1][0], pa)
            limites.append((pb, None))
        limites[-1] = (limites[-1][0], dur - MARGEN)
    else:
        trozos = [palabras]
        limites = [(MARGEN, dur - MARGEN)]
    out = []
    for tr, (a, b) in zip(trozos, limites):
        out += reparte(tr, a, b)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("guion")
    ap.add_argument("--idioma", choices=["ca", "es"], required=True)
    ap.add_argument("--voz", help="voz de Azure; por defecto la del idioma")
    ap.add_argument("--salida", required=True, help="ruta sin extension")
    ap.add_argument("--simulado", action="store_true")
    a = ap.parse_args()

    lee_env(Path(__file__).resolve().parent.parent)
    voz = a.voz or VOCES[a.idioma]
    tramos = lee_guion(a.guion)
    if a.simulado:
        print("MODO SIMULADO: audio mudo, tiempos estimados. No publicar.")

    trozos_audio, palabras, ini_tramos, t = [], [], [], 0.0
    for i, tramo in enumerate(tramos):
        if i:
            trozos_audio.append(np.zeros(int(PAUSA_TRAMO * SR), np.int16))
            t += PAUSA_TRAMO
        ini_tramos.append(t)
        # el tramo entero de una vez: la voz enlaza las frases con su entonacion
        texto = " ".join(tramo)
        hablado = para_hablar(texto)
        if a.simulado:
            pcm = np.zeros(int(sum(peso(p) for p in texto.split()) / 4.2 * SR), np.int16)
        else:
            pcm = recorta(pide_audio(hablado, a.idioma, voz))
        for pal, (p0, p1) in zip(texto.split(), tiempos_frase(hablado, pcm)):
            palabras.append({"texto": pal, "tramo": i,
                             "inicio": round(t + p0, 3), "fin": round(t + p1, 3)})
        trozos_audio.append(pcm)
        t += len(pcm) / SR

    salida = Path(a.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    wav = salida.with_suffix(".wav")
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.concatenate(trozos_audio).tobytes())

    datos = {"idioma": a.idioma, "voz": voz, "simulado": a.simulado,
             "duracion": round(t, 3),
             "tramos": [{"inicio": round(x, 3), "texto": "\n".join(tr)}
                        for x, tr in zip(ini_tramos, tramos)],
             "palabras": palabras}
    salida.with_suffix(".json").write_text(
        json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Voz: {voz} · {t:.1f} s · {len(palabras)} palabras · {len(tramos)} tramos")
    print(f"-> {wav}\n-> {salida.with_suffix('.json')}")


if __name__ == "__main__":
    main()
