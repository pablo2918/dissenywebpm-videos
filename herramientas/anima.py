"""Motor de los formatos animados (busqueda, mito, plantilla, bienmal, montaje,
pregunta). Un video = una funcion `fotograma(t)` que devuelve una imagen
1080x1920; aqui esta lo comun: fuentes, piezas pre-dibujadas (sprites),
subtitulos karaoke, tarjeta final, escritura con ffmpeg y hoja de revision.

Las piezas fijas se dibujan al doble con las ayudas de carrusel.py y se
reducen (bordes suaves); lo que cambia cada fotograma se pinta a tamano real.
"""
import json
import math
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import carrusel as C  # noqa: E402
import voz_video as VV  # noqa: E402

RAIZ = C.RAIZ
W, H, FPS = 1080, 1920, 30
AZUL, AMARILLO, CREMA, GRIS = C.AZUL, C.AMARILLO, C.CREMA, C.GRIS
BLANCO, ROJO, VERDE, LINEA = C.BLANCO, C.ROJO, C.VERDE, C.LINEA
GRIS_CLARO, FONDO_FILA = C.GRIS_CLARO, C.FONDO_FILA
# Zona de subtitulos (la misma que en los videos de carrusel): fuera del 20 %
# inferior y de los botones laterales de las apps.
SUB = (1262, 1490, 150)

TXT = {
    "es": {"cta": "Escríbeme por WhatsApp", "guardar": "Guárdalo para después"},
    "ca": {"cta": "Escriu-me per WhatsApp", "guardar": "Desa-ho per a després"},
}

_f = {}


def F(peso, tam):
    """Fuente a tamano real (sin escala)."""
    k = (peso, int(tam))
    if k not in _f:
        _f[k] = ImageFont.truetype(str(RAIZ / "fuentes" / f"Montserrat-{peso}.otf"), int(tam))
    return _f[k]


# ---------------------------------------------------------------- tiempo

def lim(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def tramo(t, t0, dur):
    """0..1 entre t0 y t0+dur."""
    return lim((t - t0) / dur) if dur > 0 else float(t >= t0)


def eo(x):
    """Frenada suave (ease out cubic)."""
    return 1 - (1 - lim(x)) ** 3


def rebote(x):
    """Entra pasandose un poco y vuelve (ease out back)."""
    x = lim(x)
    c = 1.70158
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


# ---------------------------------------------------------------- piezas

def sprite(w, h, dibuja, fondo=(0, 0, 0, 0)):
    """Dibuja con carrusel.D al doble y reduce: bordes y letras suaves."""
    im = Image.new("RGBA", (int(w * C.S), int(h * C.S)), fondo)
    dibuja(im, C.D(im))
    return im.resize((int(round(w)), int(round(h))), Image.LANCZOS)


def sombra(w, h, r=28, pad=40, fuerza=110):
    """Sombra negra difusa para pegar debajo de una tarjeta."""
    from PIL import ImageFilter
    m = Image.new("L", (int(w + 2 * pad), int(h + 2 * pad)), 0)
    ImageDraw.Draw(m).rounded_rectangle((pad, pad + 14, pad + w, pad + h + 14), r, fill=fuerza)
    m = m.filter(ImageFilter.GaussianBlur(pad / 2.2))
    s = Image.new("RGBA", m.size, (0, 0, 0, 0))
    s.putalpha(m)
    return s


def pega(fondo, sp, x, y, a=1.0, k=1.0, centro=False):
    """Pega una pieza con opacidad `a` y escala `k` (desde su centro si centro)."""
    if sp is None or a <= 0.003 or k <= 0.01:
        return
    if k != 1.0:
        w, h = max(1, int(sp.width * k)), max(1, int(sp.height * k))
        if centro:
            x, y = x + (sp.width - w) / 2, y + (sp.height - h) / 2
        sp = sp.resize((w, h), Image.BILINEAR)
    if a < 0.997:
        sp = sp.copy()
        sp.putalpha(sp.getchannel("A").point(lambda v: int(v * a)))
    fondo.paste(sp, (int(round(x)), int(round(y))), sp)


def titulo(texto, ancho, alto_max, tam_max=120, tam_min=60, color=BLANCO, max_lineas=4,
           centrado=False, peso="Black", interlinea=1.04, mayus=True):
    """Titular con *resaltado* amarillo, ajustado a la caja. Devuelve sprite."""
    tmp = Image.new("RGBA", (10, 10))
    d = C.D(tmp)
    font, lin, tam = C.ajusta_titulo(texto, peso, tam_max, tam_min, ancho, alto_max, max_lineas, d,
                                     mayus=mayus, interlinea=interlinea)
    alto = len(lin) * tam * interlinea + tam * 0.1

    def dib(im, d):
        C.escribe_titulo(d, tam * 0.14, 0, font, lin, tam, color, interlinea=interlinea,
                         centrado=centrado, ancho=ancho)
    return sprite(ancho + tam * 0.28, alto, dib)


def pastilla(txt, tam=36, fondo=AMARILLO, color=AZUL, peso="ExtraBold"):
    ft = C.f(peso, tam)
    tmp = C.D(Image.new("RGBA", (10, 10)))
    w = tmp.tl(txt, ft) + tam * 1.8
    h = tam * 2.05

    def dib(im, d):
        d.rect((0, 0, w, h), fill=fondo, r=h / 2)
        d.text((w / 2, h / 2 + 1), txt, ft, color, anchor="mm")
    return sprite(w, h, dib)


def envuelve(texto, font, ancho):
    """Lineas parejas (como carrusel.equilibra) a tamano real."""
    tmp = C.D(Image.new("RGBA", (10, 10)))
    s0 = C.S
    C.S = 1
    try:
        return C.equilibra(texto, font, ancho, tmp)
    finally:
        C.S = s0


def logo(ancho):
    lg = Image.open(RAIZ / "logo" / "logo.png").convert("RGBA")
    return lg.resize((int(ancho), int(ancho * lg.height / lg.width)), Image.LANCZOS)


def tarjeta_final(idi, frase):
    """Ultima pantalla: logo, frase, boton de WhatsApp, telefono y web."""
    im = Image.new("RGB", (W, H), AZUL)
    lg = logo(360)
    ff = F("ExtraBold", 76)
    lin = envuelve(frase, ff, 880)
    ft = C.f("ExtraBold", 54)
    bw = C.D(Image.new("RGBA", (10, 10))).tl(TXT[idi]["cta"], ft) + 130

    def bt(im2, d):
        d.rect((0, 0, bw, 132), fill=AMARILLO, r=66)
        d.text((bw / 2, 67), TXT[idi]["cta"], ft, AZUL, anchor="mm")
    boton = sprite(bw, 132, bt)
    alto = lg.height + 100 + 92 * len(lin) + 80 + 132 + 80 + 76 + 50 + 44
    y = (H - alto) / 2 - 50
    im.paste(lg, ((W - lg.width) // 2, int(y)), lg)
    y += lg.height + 100
    d = ImageDraw.Draw(im)
    for l in lin:
        d.text((W / 2, y + 46), l, font=ff, fill=BLANCO, anchor="mm")
        y += 92
    y += 80
    im.paste(boton, ((W - boton.width) // 2, int(y)), boton)
    y += 132 + 80
    d.text((W / 2, y + 38), C.TELEFONO, font=F("ExtraBold", 76), fill=AMARILLO, anchor="mm")
    y += 76 + 50
    d.text((W / 2, y + 22), C.DOMINIO_PM, font=F("SemiBold", 42), fill=GRIS_CLARO, anchor="mm")
    return im


def entra_final(fondo, final, t, t0, dur=0.35):
    """Fundido a la tarjeta final."""
    a = tramo(t, t0, dur)
    if a <= 0:
        return fondo
    if a >= 1:
        return final.copy()
    return Image.blend(fondo, final, eo(a))


# ---------------------------------------------------------------- voz

def voz(nombre, idi, tramos, carpeta):
    """Llama a voz.py con el guion (lista de tramos) y devuelve sus datos."""
    carpeta.mkdir(parents=True, exist_ok=True)
    guion = carpeta / f"{nombre}.txt"
    guion.write_text("\n\n".join(tramos) + "\n", encoding="utf-8")
    salida = carpeta / nombre
    subprocess.run([sys.executable, str(RAIZ / "herramientas" / "voz.py"), str(guion),
                    "--idioma", idi, "--salida", str(salida)], check=True, cwd=RAIZ)
    d = json.loads(salida.with_suffix(".json").read_text(encoding="utf-8"))
    d["wav"] = str(salida.with_suffix(".wav"))
    # fin de cada tramo = fin de su ultima palabra
    for i, tr in enumerate(d["tramos"]):
        ps = [p for p in d["palabras"] if p["tramo"] == i]
        tr["fin"] = ps[-1]["fin"] if ps else tr["inicio"]
    return d


class Subtitulos:
    """Bloques karaoke como en voz_video.py, para pintar en cualquier zona."""

    def __init__(self, palabras, quitar=()):
        ps = [p for p in palabras if p["tramo"] not in quitar]
        bl = VV.bloques(ps)
        self.subs = []
        for i, b in enumerate(bl):
            sig = bl[i + 1] if i + 1 < len(bl) else None
            if sig and sig[0]["tramo"] == b[0]["tramo"]:
                fin = sig[0]["inicio"]
            else:
                fin = b[-1]["fin"] + 0.35
                if sig:
                    fin = min(fin, sig[0]["inicio"])
            self.subs.append((b[0]["inicio"], fin, " ".join(p["texto"] for p in b),
                              [p["inicio"] for p in b]))

    def pinta(self, im, t, zona=SUB):
        s = next((s for s in self.subs if s[0] <= t < s[1]), None)
        if not s:
            return
        activa = max((k for k, x in enumerate(s[3]) if x <= t), default=-1)
        top, bot, lado = zona
        d = ImageDraw.Draw(im)
        ancho = W - 2 * lado
        for tam in range(VV.TAM_SUB, VV.TAM_MIN - 1, -2):
            f = F("Black", tam)
            lin = VV.reparte(s[2], f, ancho, d)
            paso = int(tam * 1.18)
            if len(lin) <= 2 and all(d.textlength(l, font=f) <= ancho for l in lin) and paso * len(lin) <= bot - top:
                break
        borde = max(5, tam // 10)
        y = top + ((bot - top) - paso * len(lin)) // 2
        esp = d.textlength(" ", font=f)
        k = 0
        for l in lin:
            x = W / 2 - d.textlength(l, font=f) / 2
            base = y + f.getmetrics()[0]
            for w in l.split():
                color = AMARILLO if k == activa else "white"
                d.text((x, base + 6), w, font=f, fill=(0, 0, 0), anchor="ls", stroke_width=borde, stroke_fill=(0, 0, 0))
                d.text((x, base), w, font=f, fill=color, anchor="ls", stroke_width=borde, stroke_fill="black")
                x += d.textlength(w, font=f) + esp
                k += 1
            y += paso


# ---------------------------------------------------------------- salida

def graba(fotograma, dur, salida, wav=None, revision=None, marcas=None, normaliza=True):
    """Pinta `dur` segundos llamando a fotograma(t) y los codifica.
    `revision`: ruta de la hoja de contacto (8 fotogramas en `marcas`).
    `normaliza`: igualar el volumen a -16 LUFS (voz); los efectos sueltos no."""
    salida = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    n = int(round(dur * FPS))
    cmd = ["ffmpeg", "-v", "error", "-y", "-nostdin",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if wav:
        cmd += ["-i", str(wav), "-filter_complex",
                f"[1:a]{'loudnorm=I=-16:TP=-1.5:LRA=11,' if normaliza else ''}aresample=48000,apad,atrim=0:{n / FPS:.3f}[a]",
                "-map", "0:v", "-map", "[a]"]
    else:
        # sin voz: pista de audio muda (la musica se pone desde la app)
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                "-map", "0:v", "-map", "1:a"]
    cmd += ["-t", f"{n / FPS:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
            "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.2",
            "-c:a", "aac", "-b:a", "128k", "-ac", "2", "-movflags", "+faststart", str(salida)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    marcas = sorted(marcas or [])
    quiero = {min(n - 1, int(m * FPS)): m for m in marcas}
    fotos = {}
    for i in range(n):
        im = fotograma(i / FPS)
        if im.mode != "RGB":
            im = im.convert("RGB")
        if i in quiero:
            fotos[i] = im.resize((360, 640), Image.LANCZOS)
        p.stdin.write(im.tobytes())
    p.stdin.close()
    if p.wait():
        sys.exit(f"ffmpeg ha fallado con {salida}")
    if revision and fotos:
        hoja = Image.new("RGB", (360 * 4, 640 * 2), "white")
        for k, i in enumerate(sorted(fotos)[:8]):
            hoja.paste(fotos[i], ((k % 4) * 360, (k // 4) * 640))
        Path(revision).parent.mkdir(parents=True, exist_ok=True)
        hoja.save(revision)
    print(f"{n / FPS:.1f} s -> {salida}")


def publicar(ruta, titulo_md, partes, aviso=None, nota=None):
    """PUBLICAR.md: texto para pegar en cada red, por idioma."""
    tit = {"es": "Castellano", "ca": "Català"}
    txt = f"# {titulo_md}\n\n"
    if aviso:
        txt += f"> **Aviso:** {aviso}\n\n"
    if nota:
        txt += f"{nota}\n\n"
    for idi, (pie, tags) in partes.items():
        txt += f"**{tit[idi]}** (vídeo: `{idi}/video.mp4`)\n\n{pie}\n\n{tags}\n\n"
    Path(ruta).write_text(txt.rstrip() + "\n", encoding="utf-8")


def limpio(t):
    return re.sub(r"\s+", " ", t.replace("*", "").replace("//", " ")).strip()


# ---------------------------------------------------------------- movil

def movil(w, h):
    """Marco de movil (pantalla transparente) y la mascara de la pantalla.
    Devuelve (marco, mascara, (x0, y0, x1, y1) de la pantalla)."""
    from PIL import ImageChops
    b = 14

    def cuerpo(im, d):
        d.rect((0, 0, w, h), fill=(70, 80, 110), r=58)
        d.rect((3, 3, w - 3, h - 3), fill=(24, 28, 40), r=55)
        d.rect((w / 2 - 62, b + 14, w / 2 + 62, b + 44), fill=(24, 28, 40), r=15)

    def pantalla(im, d):
        d.rect((b, b, w - b, h - b), fill=(255, 255, 255), r=46)
    marco = sprite(w, h, cuerpo)
    hueco = sprite(w, h, pantalla).getchannel("A")
    # la isla de la camara tapa la pantalla
    isla = sprite(w, h, lambda im, d: d.rect((w / 2 - 62, b + 14, w / 2 + 62, b + 44), fill=(0, 0, 0), r=15)).getchannel("A")
    hueco = ImageChops.subtract(hueco, isla)
    marco.putalpha(ImageChops.subtract(marco.getchannel("A"), hueco))
    caja = (b, b, w - b, h - b)
    return marco, hueco.crop(caja), caja
