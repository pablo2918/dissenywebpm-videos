"""Pruebas de estilo con video de archivo de Pexels (idea de MoneyPrinterTurbo,
hecha a nuestra manera: marca, voz Azure, subtitulos karaoke y efectos propios).
Ver planes/plan_archivo.py.

Estilos:
  completo  video a pantalla completa, oscurecido, voz y subtitulos grandes
  mito      «Mito o verdad» con video de fondo (desenfocado y oscuro)
  partido   video arriba, tarjetas de marca abajo, voz y subtitulos
"""
import subprocess

import numpy as np
from PIL import Image, ImageDraw

import anima as A
import f_mito
import mixkit
import pexels

C = A.C


def fuente(q):
    """Un numero = clip de Mixkit (sin clave); un texto = busqueda en Pexels."""
    return mixkit.clip(q) if isinstance(q, int) else pexels.clips(q)[0]


class Clip:
    """Lee un video fotograma a fotograma ya recortado a (w, h), en bucle.
    `oscuro` 0..1 baja el brillo; `desenfoque` en pixeles."""

    def __init__(self, ruta, w, h, oscuro=0.0, desenfoque=0):
        vf = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={A.FPS}"
        if desenfoque:
            vf += f",boxblur={desenfoque}:2"
        if oscuro:
            vf += f",eq=brightness={-oscuro * 0.5:.2f}:saturation=0.9"
        self.w, self.h = w, h
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-nostdin", "-stream_loop", "-1", "-i", str(ruta),
                                   "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE)
        self.n, self.ult = -1, None

    def en(self, t):
        quiero = int(t * A.FPS)
        while self.n < quiero:
            b = self.p.stdout.read(self.w * self.h * 3)
            self.ult = Image.frombuffer("RGB", (self.w, self.h), b, "raw", "RGB", 0, 1)
            self.n += 1
        return self.ult

    def cierra(self):
        self.p.kill()


def degradado(w, h, arriba=150, abajo=200):
    """Velo oscuro arriba y abajo para que se lea el texto sobre el video."""
    a = np.zeros((h, 1), np.float32)
    y = np.arange(h)[:, None]
    a += np.clip(1 - y / (h * 0.35), 0, 1) * arriba
    a += np.clip((y - h * 0.45) / (h * 0.55), 0, 1) * abajo
    m = Image.fromarray(np.repeat(a, w, axis=1).astype(np.uint8), "L")
    v = Image.new("RGBA", (w, h), (5, 9, 20, 0))
    v.putalpha(m)
    return v


def marca():
    return A.pastilla("DISSENY WEB PM", 30, fondo=(255, 255, 255), color=A.AZUL)


# ---------------------------------------------------------------- estilo 1

def completo(v, idi, salida, rev, tmp):
    c = v[idi]
    textos = [x[0] for x in c["tramos"]]
    vz = A.voz(salida.parent.name + "_" + v["id"], idi, textos, tmp)
    rutas = [fuente(x[1]) for x in c["tramos"]]
    clips = [Clip(r, A.W, A.H, oscuro=0.25) for r in rutas]
    ini = [x["inicio"] for x in vz["tramos"]]
    subs = A.Subtitulos(vz["palabras"], quitar=(0,))
    velo = degradado(A.W, A.H)
    tit = A.titulo(c["titulo"], 940, 700, 120, 70, centrado=True, max_lineas=5)
    mk = marca()
    t_final = vz["duracion"] + 0.3
    dur = t_final + 2.6
    final = A.tarjeta_final(idi, c["final"])

    def fotograma(t):
        k = max(i for i in range(len(ini)) if ini[i] - 0.2 <= t) if t >= ini[0] else 0
        im = clips[k].en(t - ini[k] + 0.2).copy()
        # fundido corto entre planos
        if k > 0 and t < ini[k]:
            im = Image.blend(clips[k - 1].en(t - ini[k - 1] + 0.2), im, A.tramo(t, ini[k] - 0.2, 0.2))
        im.paste(velo, (0, 0), velo)
        A.pega(im, mk, (A.W - mk.width) / 2, 140)
        if k == 0:
            e = A.rebote(A.tramo(t, 0, 0.4))
            A.pega(im, tit, (A.W - tit.width) / 2, 760 - tit.height / 2, k=0.9 + 0.1 * e, centro=True)
        subs.pinta(im, t, zona=(960, 1320, 80), tam_max=100)
        return A.entra_final(im, final, t, t_final)

    marcas = [0.2, 1.5] + [x + 1.0 for x in ini[1:]] + [dur - 0.3]
    A.graba(fotograma, dur, salida, vz["wav"], rev, marcas[:8])
    for cl in clips:
        cl.cierra()
    return [r.stem for r in rutas]


# ---------------------------------------------------------------- estilo 2

def mito(v, idi, salida, rev, tmp):
    import plan_mito
    base = plan_mito.VIDEOS[v["mito"] - 1]
    rutas = [fuente(q) for q in v["buscar"]]
    clips = [Clip(r, A.W, A.H, oscuro=0.55, desenfoque=14) for r in rutas]
    tinte = Image.new("RGBA", (A.W, A.H), (9, 15, 32, 110))

    def fondo(i, tl):
        im = clips[i].en(tl).copy()
        im.paste(tinte, (0, 0), tinte)
        return im
    f_mito.hacer(base, idi, salida, rev, tmp, fondos=fondo)
    for cl in clips:
        cl.cierra()
    return [r.stem for r in rutas]


# ---------------------------------------------------------------- estilo 3

ALTO_V = 1000


def tarjeta(n, txt):
    w = 960
    ft = A.F("Black", 64)
    lin = A.envuelve(txt, ft, w - 220)
    h = max(150, 60 + 76 * len(lin))

    def dib(im, d):
        d.rect((0, 0, w, h), fill=C.BLANCO, r=34)
        d.ellipse((30, h / 2 - 52, 134, h / 2 + 52), fill=C.AMARILLO)
        d.text((82, h / 2 + 2), str(n), C.f("Black", 64), C.AZUL, anchor="mm")
        y = h / 2 - 76 * len(lin) / 2
        for l in lin:
            d.text((170, y + 38), l, C.f("Black", 64), C.AZUL, anchor="lm")
            y += 76
    return A.sprite(w, h, dib)


def partido(v, idi, salida, rev, tmp):
    c = v[idi]
    tramos = [c["gancho"][0]] + [p[1] for p in c["puntos"]] + [c["cierre"][0]]
    consultas = [c["gancho"][1]] + [p[2] for p in c["puntos"]] + [c["cierre"][1]]
    vz = A.voz(salida.parent.name + "_" + v["id"], idi, tramos, tmp)
    rutas = [fuente(q) for q in consultas]
    clips = [Clip(r, A.W, ALTO_V) for r in rutas]
    ini = [x["inicio"] for x in vz["tramos"]]
    subs = A.Subtitulos(vz["palabras"], quitar=(0,))
    tit = A.titulo(c["titulo"], 940, 560, 100, 60, centrado=True, max_lineas=4)
    cards = [tarjeta(i + 1, p[0]) for i, p in enumerate(c["puntos"])]
    mk = marca()
    t_final = vz["duracion"] + 0.3
    dur = t_final + 2.6
    final = A.tarjeta_final(idi, c["final"])
    sombra = degradado(A.W, ALTO_V, arriba=110, abajo=60)

    def fotograma(t):
        im = Image.new("RGB", (A.W, A.H), A.AZUL)
        k = max(i for i in range(len(ini)) if ini[i] - 0.2 <= t) if t >= ini[0] else 0
        im.paste(clips[k].en(t - ini[k] + 0.2), (0, 0))
        im.paste(sombra, (0, 0), sombra)
        # filete amarillo entre el video y la parte de marca
        ImageDraw.Draw(im).rectangle((0, ALTO_V, A.W, ALTO_V + 10), fill=A.AMARILLO)
        A.pega(im, mk, (A.W - mk.width) / 2, 140)
        if k == 0:
            A.pega(im, tit, (A.W - tit.width) / 2, ALTO_V + 40, a=1)
        elif k <= len(cards):
            cd = cards[k - 1]
            e = A.rebote(A.tramo(t, ini[k] - 0.1, 0.4))
            A.pega(im, cd, (A.W - cd.width) / 2, ALTO_V + 50, k=0.85 + 0.15 * e, centro=True)
        if k > 0:
            subs.pinta(im, t)
        return A.entra_final(im, final, t, t_final)

    marcas = [0.2, 1.5] + [x + 1.0 for x in ini[1:]] + [dur - 0.3]
    A.graba(fotograma, dur, salida, vz["wav"], rev, marcas[:8])
    for cl in clips:
        cl.cierra()
    return [r.stem for r in rutas]


def hacer(v, idi, salida, rev, tmp):
    ids = {"completo": completo, "mito": mito, "partido": partido}[v["estilo"]](v, idi, salida, rev, tmp)
    (salida.parent / "clips_archivo.txt").write_text(
        "Vídeos de archivo usados (Mixkit, Stock Video Free License: uso comercial, sin atribución):\n"
        + "\n".join(f"https://assets.mixkit.co/videos/{i}/{i}-1080.mp4" for i in ids) + "\n", encoding="utf-8")


def publicar(v, ruta):
    pass
