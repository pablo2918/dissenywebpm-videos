#!/usr/bin/env python3
"""Vídeos con el motor nuevo (Remotion). Un guion -> vídeo terminado.

    python3 herramientas/remo.py <guion> [--audio voz_de_pablo.wav] [--solo-datos]

<guion> es `remotion/guiones/<nombre>.json`:
    {"id": "antes_despues", "idioma": "es", "composicion": "AntesDespues",
     "escenas": [{"voz": "Frase que se dice", ...lo que dibuja esa escena}, ...],
     ...}

Pasos:
1. Voz: sin --audio, la voz Azure provisional (voz.py). Con --audio (la voz
   clonada de Pablo hecha con VoiceStudio), se transcribe con faster-whisper
   para sacar el tiempo de cada palabra y se reparte por escenas.
2. Deja en remotion/public/<id>_<idioma>/ el audio y datos.json (escenas con
   inicio/fin, palabras con tiempos) para que Remotion lo anime.
3. Renderiza con Remotion, iguala volumen a -16 LUFS y deja en
   salida/remotion/<id>/<idioma>/: video.mp4, guion_voz.txt (el texto para
   pasar a VoiceStudio) y hoja de revisión en .tmp/revision/remotion/.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import anima as A  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
REMO = RAIZ / "remotion"


def _norma(w):
    import unicodedata
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(ch for ch in w if ch.isalnum())


def voz_propia(audio, escenas, idi, tmp):
    """Voz de Pablo (VoiceStudio): se transcribe con faster-whisper (tiempo de
    cada palabra) y se alinea con el guion palabra a palabra. Si la IA dice
    algo distinto («cuarenta y ocho» por «48»), esas palabras se reparten entre
    las vecinas sin descuadrar el resto."""
    import difflib
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    # se decodifica con ffmpeg (16 kHz mono) en vez de dejarselo a faster-whisper:
    # asi no depende de la version de la libreria «av» y vale mp3, wav, m4a...
    import numpy as np
    crudo = subprocess.run(["ffmpeg", "-v", "error", "-i", str(audio), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                           check=True, capture_output=True).stdout
    segs, _ = m.transcribe(np.frombuffer(crudo, np.float32), language=idi, word_timestamps=True)
    oidas = [w for s in segs for w in s.words if _norma(w.word)]
    guion = [(i, t) for i, e in enumerate(escenas) for t in e["voz"].split() if _norma(t)]
    sm = difflib.SequenceMatcher(None, [_norma(t) for _, t in guion], [_norma(w.word) for w in oidas], autojunk=False)
    tiempos = [None] * len(guion)
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op == "equal":
            for k in range(a1 - a0):
                w = oidas[b0 + k]
                tiempos[a0 + k] = (w.start, w.end)
        elif op == "replace" and b1 > b0:
            # mismo trozo dicho de otra forma: se reparte su duracion
            t0, t1 = oidas[b0].start, oidas[b1 - 1].end
            n = a1 - a0
            for k in range(n):
                tiempos[a0 + k] = (t0 + (t1 - t0) * k / n, t0 + (t1 - t0) * (k + 1) / n)
    # huecos (palabras del guion que no se oyeron): entre la anterior y la siguiente
    for k in range(len(tiempos)):
        if tiempos[k] is None:
            prev = next((tiempos[j][1] for j in range(k - 1, -1, -1) if tiempos[j]), 0.0)
            sig = next((tiempos[j][0] for j in range(k + 1, len(tiempos)) if tiempos[j]), prev + 0.3)
            tiempos[k] = (prev, max(prev, sig))
    pal = [{"texto": t, "tramo": i, "inicio": round(a, 3), "fin": round(b, 3)} for (i, t), (a, b) in zip(guion, tiempos)]
    wav = tmp / "voz.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(audio), "-ac", "1", "-ar", "48000",
                    "-sample_fmt", "s16", str(wav)], check=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", str(wav)]).decode())
    tramos = []
    for i in range(len(escenas)):
        ps = [p for p in pal if p["tramo"] == i]
        tramos.append({"inicio": ps[0]["inicio"] if ps else 0, "fin": ps[-1]["fin"] if ps else 0})
    acierto = sum(b1 - b0 for op, a0, a1, b0, b1 in sm.get_opcodes() if op == "equal") / max(1, len(guion))
    print(f"voz propia: {len(oidas)} palabras oídas, {acierto:.0%} coinciden con el guion")
    if acierto < 0.6:
        print("OJO: el audio no parece leer este guion (¿audio equivocado?). Revisar antes de seguir.")
    return {"wav": str(wav), "palabras": pal, "tramos": tramos, "duracion": dur}


def mete_pausas(vz, pausas, destino):
    """Silencio de `seg` segundos justo despues de la frase k (p. ej. la cuenta
    atras del mito). Mueve los tiempos de todo lo que va detras."""
    import wave
    import numpy as np
    with wave.open(vz["wav"]) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, ch)
    trozos, desde, extra = [], 0, 0.0
    for k, seg in sorted(pausas):
        corte = vz["tramos"][k]["fin"] + 0.12
        i = int(round(corte * sr))
        trozos += [pcm[desde:i], np.zeros((int(seg * sr), ch), np.int16)]
        desde = i
        for p in vz["palabras"]:
            if p["tramo"] > k:
                p["inicio"] += seg
                p["fin"] += seg
        for j, tr in enumerate(vz["tramos"]):
            if j > k:
                tr["inicio"] += seg
                tr["fin"] += seg
        extra += seg
    trozos.append(pcm[desde:])
    with wave.open(str(destino), "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(sw)
        w.setframerate(sr)
        w.writeframes(np.concatenate(trozos).tobytes())
    vz["duracion"] += extra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("guion")
    ap.add_argument("--audio", help="voz de Pablo (wav/mp3) para este guion")
    ap.add_argument("--solo-datos", action="store_true", help="no renderiza (para previsualizar en Studio)")
    a = ap.parse_args()

    g = json.loads(Path(a.guion).read_text(encoding="utf-8"))
    idi = g.get("idioma", "es")
    nombre = f"{g['id']}_{idi}"
    tmp = RAIZ / ".tmp" / "remotion" / nombre
    tmp.mkdir(parents=True, exist_ok=True)
    salida = RAIZ / "salida" / "remotion" / g["id"] / idi
    salida.mkdir(parents=True, exist_ok=True)
    escenas = g["escenas"]
    (salida / "guion_voz.txt").write_text(
        "Texto para la voz (una escena por párrafo; léelo tal cual):\n\n"
        + "\n\n".join(e["voz"] for e in escenas if e.get("voz")) + "\n", encoding="utf-8")

    con_voz = [e for e in escenas if e.get("voz")]
    if a.audio:
        vz = voz_propia(Path(a.audio), con_voz, idi, tmp)
    else:
        vz = A.voz(nombre, idi, [e["voz"] for e in con_voz], tmp)
        for i, tr in enumerate(vz["tramos"]):
            ps = [p for p in vz["palabras"] if p["tramo"] == i]
            tr["fin"] = ps[-1]["fin"] if ps else tr["inicio"]

    pub = REMO / "public" / nombre
    pub.mkdir(parents=True, exist_ok=True)
    pausas = [(k, e["pausa"]) for k, e in enumerate(con_voz) if e.get("pausa")]
    if pausas:
        mete_pausas(vz, pausas, pub / "voz.wav")
    else:
        shutil.copy(vz["wav"], pub / "voz.wav")
    # cada escena va desde que empieza su frase hasta que empieza la siguiente
    k = 0
    for e in escenas:
        if e.get("voz"):
            tr = vz["tramos"][k]
            e["inicio"], e["finVoz"] = tr["inicio"], tr["fin"]
            e["palabras"] = [p for p in vz["palabras"] if p["tramo"] == k]
            k += 1
    for i, e in enumerate(escenas):
        e.setdefault("inicio", escenas[i - 1]["fin"] if i else 0)
        sig = next((x for x in escenas[i + 1:] if "inicio" in x), None)
        e["fin"] = sig["inicio"] if sig else vz["duracion"] + e.get("extra", 0.4)
    datos = dict(g, carpeta=nombre, escenas=escenas, duracion=escenas[-1]["fin"] + g.get("cola", 2.8),
                 audio=f"{nombre}/voz.wav")
    (pub / "datos.json").write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    print("datos:", pub / "datos.json", f"({datos['duracion']:.1f} s)")
    if a.solo_datos:
        return

    crudo = tmp / "crudo.mp4"
    subprocess.run([shutil.which("npx") or "npx", "remotion", "render", g["composicion"], str(crudo),
                    f"--props={pub / 'datos.json'}", "--log=error"], check=True, cwd=REMO)
    video = salida / "video.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(crudo), "-c:v", "copy",
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    str(video)], check=True)
    # hoja de revision: 12 fotogramas repartidos
    rev = RAIZ / ".tmp" / "revision" / "remotion"
    rev.mkdir(parents=True, exist_ok=True)
    d = datos["duracion"]
    n = 12
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf",
                    f"fps={n / d:.4f},scale=270:-1,tile=6x2:padding=6:color=white", "-frames:v", "1",
                    str(rev / f"{nombre}.jpg")], check=True)
    print("vídeo:", video)
    print("revisión:", rev / f"{nombre}.jpg")


if __name__ == "__main__":
    main()
