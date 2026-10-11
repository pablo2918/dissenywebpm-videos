#!/usr/bin/env python3
"""Monta un video vertical con voz sobre las laminas de un carrusel.

Cada tramo del guion va con una lamina. Subtitulos = texto del guion tal cual,
con los tiempos de palabra que dejo voz.py. Sin zoom ni efectos.

Uso:
  python3 herramientas/voz_video.py .tmp/04_precio_ca \
      --carpeta salida/carruseles/04_precio_ca \
      --laminas 1_portada,2_01,3_02,4_03,7_cierre \
      --salida salida/04_precio_ca_voz.mp4
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
AZUL = (9, 15, 32)
AMARILLO = (251, 190, 1)
# Lamina 4:5 reducida al 80 %, dejando sitio debajo para los subtitulos.
LAM_W, LAM_H, LAM_Y, RADIO = 864, 1080, 190, 28
# Zona de subtitulos: entre la lamina y el 20 % inferior (margen 430 px),
# con 160 px a los lados (botones de las apps).
SUB_TOP, SUB_BOT, SUB_LADO = LAM_Y + LAM_H + 24, H - 430, 160
TAM_SUB, TAM_MIN = 76, 52
COLA = 1.6               # segundos de cierre en silencio al final
RAIZ = Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "fuentes" / "Montserrat-Black.otf"
if not FUENTE.exists():
    FUENTE = Path("/usr/share/fonts/julietaula-montserrat-fonts/Montserrat-ExtraBold.otf")


# Palabras tras las que no conviene cortar un subtitulo (articulos, preposiciones...).
NO_CORTAR = set("""el la els les lo los las un una uns unes de del dels al als a i y o
en per para por que amb con sense sin mi tu su teu teva meu seu no es se te et em me
hi ho the""".split())


def _coste(trozo):
    n = len(trozo)
    c = 1 + {1: 10, 2: 3}.get(n, 0)
    # Un subtitulo que dura menos de 0,7 s no da tiempo a leerlo.
    if trozo[-1]["fin"] - trozo[0]["inicio"] < 0.7:
        c += 5
    ult = trozo[-1]["texto"]
    if re.search(r"[,;:]$", ult):
        c -= 2
    elif re.sub(r"\W", "", ult.lower()) in NO_CORTAR:
        c += 7
    return c


def _parte_frase(fr):
    """Mejor reparto de una frase en bloques de 1-5 palabras (programacion
    dinamica): pocos bloques, ni de 1 ni de 2 palabras si se puede, cortes
    en comas y nunca justo despues de un articulo o preposicion."""
    # Frase corta dicha deprisa: entera, en un solo bloque de 2 lineas.
    # Partirla dejaria trozos que pasan antes de poder leerlos.
    if len(fr) <= 7 and fr[-1]["fin"] - fr[0]["inicio"] < 2.2:
        return [fr]
    mejor = [(0, [])] + [None] * len(fr)
    for i in range(1, len(fr) + 1):
        for k in range(1, 6):
            if i - k >= 0 and mejor[i - k] is not None:
                c = mejor[i - k][0] + _coste(fr[i - k:i])
                if mejor[i] is None or c < mejor[i][0]:
                    mejor[i] = (c, mejor[i - k][1] + [fr[i - k:i]])
    return mejor[-1][1]


def bloques(palabras):
    """Bloques de 3-5 palabras que no cruzan de un tramo a otro ni de una
    frase a otra."""
    out, fr = [], []
    for i, p in enumerate(palabras):
        fr.append(p)
        sig = palabras[i + 1] if i + 1 < len(palabras) else None
        if sig is None or sig["tramo"] != p["tramo"] or re.search(r"[.?!]$", p["texto"]):
            out += _parte_frase(fr)
            fr = []
    return out


def reparte(texto, fuente, ancho, d):
    """Una linea si cabe; si no, dos lineas lo mas parejas posible."""
    pal = texto.split()
    if d.textlength(texto, font=fuente) <= ancho or len(pal) == 1:
        return [texto]
    opciones = []
    for k in range(1, len(pal)):
        a, b = " ".join(pal[:k]), " ".join(pal[k:])
        opciones.append((max(d.textlength(a, font=fuente), d.textlength(b, font=fuente)), [a, b]))
    return min(opciones)[1]


def ajusta_sub(texto, d):
    """Mayor cuerpo con el que el bloque cabe en 2 lineas dentro de la zona."""
    ancho, alto = W - 2 * SUB_LADO, SUB_BOT - SUB_TOP
    for tam in range(TAM_SUB, TAM_MIN - 1, -2):
        f = ImageFont.truetype(str(FUENTE), tam)
        lin = reparte(texto, f, ancho, d)
        paso = int(tam * 1.18)
        if len(lin) <= 2 and all(d.textlength(l, font=f) <= ancho for l in lin) \
                and paso * len(lin) <= alto:
            return f, lin, paso, tam
    print(f"  aviso: «{texto}» no cabe ni a {TAM_MIN} px; acortar el bloque")
    f = ImageFont.truetype(str(FUENTE), TAM_MIN)
    return f, reparte(texto, f, ancho, d), int(TAM_MIN * 1.18), TAM_MIN


def lamina(ruta):
    im = Image.open(ruta).convert("RGB").resize((LAM_W, LAM_H), Image.LANCZOS)
    m = Image.new("L", (LAM_W * 4, LAM_H * 4), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, LAM_W * 4 - 1, LAM_H * 4 - 1), RADIO * 4, fill=255)
    return im, m.resize((LAM_W, LAM_H), Image.LANCZOS)


def fotograma(lam, sub, activa=-1, completo=False):
    """`completo`: la lamina ocupa toda la pantalla (pantalla de gancho).
    `activa`: indice de la palabra que se esta diciendo (sale en amarillo)."""
    if completo:
        return lam[0].copy()
    im = Image.new("RGB", (W, H), AZUL)
    x = (W - LAM_W) // 2
    # Filete fino para que las laminas azules no se fundan con el fondo.
    ImageDraw.Draw(im).rounded_rectangle((x - 2, LAM_Y - 2, x + LAM_W + 1, LAM_Y + LAM_H + 1),
                                         RADIO + 2, fill=(40, 50, 78))
    im.paste(lam[0], (x, LAM_Y), lam[1])
    if sub:
        d = ImageDraw.Draw(im)
        f, lin, paso, tam = ajusta_sub(sub, d)
        borde = max(5, tam // 10)
        y = SUB_TOP + ((SUB_BOT - SUB_TOP) - paso * len(lin)) // 2
        esp = d.textlength(" ", font=f)
        k = 0
        for l in lin:
            x = W / 2 - d.textlength(l, font=f) / 2
            for w in l.split():
                color = AMARILLO if k == activa else "white"
                # sombra suave debajo y contorno negro grueso: se lee sobre cualquier fondo
                # todas las palabras sobre la misma linea base
                base = y + f.getmetrics()[0]
                d.text((x, base + 6), w, font=f, fill=(0, 0, 0), anchor="ls",
                       stroke_width=borde, stroke_fill=(0, 0, 0))
                d.text((x, base), w, font=f, fill=color, anchor="ls",
                       stroke_width=borde, stroke_fill="black")
                x += d.textlength(w, font=f) + esp
                k += 1
            y += paso
    return im


def a_frame(t):
    return round(t * FPS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("voz", help="ruta sin extension que dejo voz.py (.wav + .json)")
    ap.add_argument("--carpeta", required=True, help="carpeta con las laminas PNG")
    ap.add_argument("--laminas", help="nombres sin .png, uno por tramo, separados por comas")
    ap.add_argument("--salida", required=True)
    a = ap.parse_args()

    base = Path(a.voz)
    datos = json.loads(base.with_suffix(".json").read_text(encoding="utf-8"))
    wav = base.with_suffix(".wav")
    tramos, palabras = datos["tramos"], datos["palabras"]
    carpeta = Path(a.carpeta)
    gancho = RAIZ / "salida" / "ganchos" / f"{carpeta.name}.png"
    if a.laminas:
        nombres = a.laminas.split(",")
    elif gancho.exists():
        # el gancho (pantalla completa) sustituye a la portada en el video
        nombres = ["0_gancho"] + [p.stem for p in sorted(carpeta.glob("*.png")) if p.stem != "1_portada"]
    else:
        nombres = [p.stem for p in sorted(carpeta.glob("*.png"))]
    if len(nombres) != len(tramos):
        sys.exit(f"Hay {len(tramos)} tramos y {len(nombres)} laminas: usa --laminas.")
    lams = [(Image.open(gancho).convert("RGB").resize((W, H), Image.LANCZOS), None)
            if n == "0_gancho" else lamina(carpeta / f"{n}.png") for n in nombres]
    completos = {i for i, n in enumerate(nombres) if n == "0_gancho"}
    if datos.get("simulado"):
        print("AVISO: la voz es SIMULADA (muda). Este video es solo de prueba.")

    total = a_frame(datos["duracion"] + COLA)
    # Lamina de cada frame.
    ini_tramo = [0] + [a_frame(t["inicio"]) for t in tramos[1:]]
    # Subtitulo de cada frame.
    bl = bloques([p for p in palabras if p["tramo"] not in completos])
    subs = []      # (inicio, fin, texto, [inicios de cada palabra])
    for i, b in enumerate(bl):
        ini = a_frame(b[0]["inicio"])
        sig = bl[i + 1] if i + 1 < len(bl) else None
        if sig and sig[0]["tramo"] == b[0]["tramo"]:
            fin = a_frame(sig[0]["inicio"])
        else:
            fin = a_frame(b[-1]["fin"] + 0.35)
            if sig:
                fin = min(fin, a_frame(sig[0]["inicio"]))
        subs.append((ini, fin, " ".join(p["texto"] for p in b), [a_frame(p["inicio"]) for p in b]))

    cortes = sorted({0, total, *ini_tramo, *[s[0] for s in subs], *[s[1] for s in subs],
                     *[t for s in subs for t in s[3]]})
    cortes = [c for c in cortes if 0 <= c <= total]

    tmp = Path(tempfile.mkdtemp(prefix="vozvideo_"))
    cache, lista = {}, []
    for c0, c1 in zip(cortes, cortes[1:]):
        if c1 <= c0:
            continue
        li = max(i for i, s in enumerate(ini_tramo) if s <= c0)
        sub = next((s for s in subs if s[0] <= c0 < s[1]), None)
        texto = sub[2] if sub else None
        activa = max((k for k, t in enumerate(sub[3]) if t <= c0), default=-1) if sub else -1
        clave = (li, texto, activa)
        if clave not in cache:
            ruta = tmp / f"f{len(cache):03d}.png"
            fotograma(lams[li], texto, activa, li in completos).save(ruta)
            cache[clave] = ruta
        lista.append((cache[clave], (c1 - c0) / FPS))

    txt = tmp / "lista.txt"
    with open(txt, "w") as f:
        for ruta, dur in lista:
            f.write(f"file '{ruta}'\nduration {dur:.6f}\n")
        f.write(f"file '{lista[-1][0]}'\n")

    salida = Path(a.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-v", "error", "-y",
           "-f", "concat", "-safe", "0", "-i", str(txt), "-i", str(wav),
           "-filter_complex", f"[0:v]fps={FPS},format=yuv420p[v];"
                              f"[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,apad,atrim=0:{total / FPS:.3f}[a]",
           "-map", "[v]", "-map", "[a]", "-t", f"{total / FPS:.3f}",
           "-c:v", "libx264", "-preset", "slow", "-crf", "19",
           "-profile:v", "high", "-level", "4.2",
           "-c:a", "aac", "-b:a", "128k", "-ac", "2",
           "-movflags", "+faststart", str(salida)]
    subprocess.run(cmd, check=True)
    shutil.rmtree(tmp)
    print(f"{len(bl)} bloques de subtitulos · {len(cache)} fotogramas distintos · "
          f"{total / FPS:.1f} s\n-> {salida}")


if __name__ == "__main__":
    main()
