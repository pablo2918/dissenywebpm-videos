#!/usr/bin/env python3
"""Dibuja las 7 laminas de un carrusel (portada, 5 puntos, cierre).

Mismo estilo que los carruseles de Disseny Web PM: 1080x1350 logicos (4:5),
dibujado al doble y guardado a 1440x1800 (lo maximo que sirve Instagram).

Uso:  python3 herramientas/carrusel.py carruseles/23_busca_es.json
Deja: salida/<tema>/<idioma>/carrusel/1_portada.png ... 7_cierre.png
      y salida/<tema>/<idioma>/gancho.png (pantalla de gancho del video)

En los textos: *entre asteriscos* = resaltador amarillo; // = salto de linea.
Las maquetas son ilustraciones de un negocio ficticio, sin marcas de nadie.
"""
import json
import math
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
S = 2                                   # escala de dibujo
W, H = 1080, 1350                       # espacio logico
SALIDA = (1440, 1800)
MARGEN = 86

AZUL = (9, 15, 32)
AMARILLO = (251, 190, 1)
CREMA = (246, 243, 237)
GRIS = (104, 112, 128)
GRIS_CLARO = (150, 158, 178)
BLANCO = (255, 255, 255)
LINEA = (228, 231, 238)
FONDO_FILA = (245, 247, 250)
ROJO = (214, 48, 49)
VERDE = (37, 163, 92)
TELEFONO = "641 27 74 95"
DOMINIO_PM = "dissenywebpm.com"

_fuentes = {}


def f(peso, tam):
    k = (peso, tam, S)
    if k not in _fuentes:
        _fuentes[k] = ImageFont.truetype(str(RAIZ / "fuentes" / f"Montserrat-{peso}.otf"), int(tam * S))
    return _fuentes[k]


class D:
    """ImageDraw que recibe coordenadas logicas y escala por dentro."""

    def __init__(self, im):
        self.im = im
        self.d = ImageDraw.Draw(im)

    def _xy(self, xy):
        return [v * S for v in xy]

    def rect(self, xy, fill=None, r=0, outline=None, width=1):
        self.d.rounded_rectangle(self._xy(xy), radius=r * S, fill=fill,
                                 outline=outline, width=int(width * S))

    def ellipse(self, xy, fill=None, outline=None, width=1):
        self.d.ellipse(self._xy(xy), fill=fill, outline=outline, width=int(width * S))

    def line(self, xy, fill, width=1):
        self.d.line(self._xy(xy), fill=fill, width=int(width * S))

    def poly(self, pts, fill):
        self.d.polygon([(x * S, y * S) for x, y in pts], fill=fill)

    def text(self, xy, txt, font, fill, anchor="la", **kw):
        if "stroke_width" in kw:
            kw["stroke_width"] = int(kw["stroke_width"] * S)
        self.d.text((xy[0] * S, xy[1] * S), txt, font=font, fill=fill, anchor=anchor, **kw)

    def tl(self, txt, font):
        return self.d.textlength(txt, font=font) / S


def lienzo(color):
    return Image.new("RGB", (W * S, H * S), color)


def guarda(im, ruta):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").resize(SALIDA, Image.LANCZOS).save(ruta, optimize=True)


# ---------------------------------------------------------------- texto

def trocea(texto):
    """[(palabra, resaltada, salto_antes)]"""
    out, dentro, salto = [], False, False
    for tok in texto.split():
        if tok == "//":
            salto = True
            continue
        empieza = tok.startswith("*")
        if empieza:
            dentro = True
            tok = tok[1:]
        cierra = re.search(r"\*([.,:;?!»]*)$", tok)
        if cierra:
            tok = tok[:cierra.start()] + cierra.group(1)
        out.append((tok, dentro, salto))
        salto = False
        if cierra:
            dentro = False
    return out


def lineas_titulo(palabras, font, ancho, d, mayus, forzadas=None):
    """Reparte el titular en lineas. En `forzadas` anota que lineas empiezan
    por un // (salto puesto a proposito)."""
    lineas, cur = [], []
    for w, res, salto in palabras:
        w2 = w.upper() if mayus else w
        prueba = " ".join(x[0] for x in cur + [(w2, res)])
        if cur and (salto or d.tl(prueba, font) > ancho):
            lineas.append(cur)
            cur = []
            if salto and forzadas is not None:
                forzadas.add(len(lineas))
        cur.append((w2, res))
    if cur:
        lineas.append(cur)
    return lineas


def ajusta_titulo(texto, peso, maximo, minimo, ancho, alto_max, max_lineas, d, mayus=True, interlinea=1.0):
    pal = trocea(texto)
    for tam in range(maximo, minimo - 1, -2):
        font = f(peso, tam)
        forzadas = set()
        lin = lineas_titulo(pal, font, ancho, d, mayus, forzadas)
        anchos_ok = all(d.tl(w, font) <= ancho for w, _, _ in
                        [(x.upper() if mayus else x, 0, 0) for x, _, _ in pal])
        alto = len(lin) * tam * interlinea
        # palabra corta colgando sola (salvo que el salto sea a proposito)
        # (un salto a proposito solo se respeta si deja la palabra al final:
        # «SI ABRES / HOY» si; «TU CARTA, / SIN / «CONSULTAR»» no)
        huerfana = any(len(l) == 1 and len(l[0][0]) <= 4
                       and not (i in forzadas and i == len(lin) - 1)
                       for i, l in enumerate(lin) if i)
        if len(lin) <= max_lineas and alto <= alto_max and anchos_ok and not huerfana:
            return font, lin, tam
    font = f(peso, minimo)
    return font, lineas_titulo(pal, font, ancho, d, mayus), minimo


def escribe_titulo(d, x, y, font, lineas, tam, color, color_res=AZUL, interlinea=1.0, centrado=False, ancho=0):
    """Pinta el resaltador amarillo y luego el texto. Devuelve la y final."""
    esp = d.tl(" ", font)
    paso = tam * interlinea
    for li, linea in enumerate(lineas):
        ly = y + li * paso
        total = d.tl(" ".join(w for w, _ in linea), font)
        lx = x + (ancho - total) / 2 if centrado else x
        cx = lx
        tramos = []
        for w, res in linea:
            wl = d.tl(w, font)
            if res:
                if tramos and tramos[-1][1] >= cx - esp - 0.5:
                    tramos[-1][1] = cx + wl
                else:
                    tramos.append([cx, cx + wl])
            cx += wl + esp
        for a, b in tramos:
            d.rect((a - tam * 0.12, ly + tam * 0.02, b + tam * 0.12, ly + tam * 0.98), fill=AMARILLO, r=tam * 0.1)
        cx = lx
        for w, res in linea:
            d.text((cx, ly + tam * 0.5), w, font, color_res if res else color, anchor="lm")
            cx += d.tl(w, font) + esp
    return y + len(lineas) * paso


def parte(texto, font, ancho, d):
    lineas, cur = [], ""
    for w in texto.split():
        p = f"{cur} {w}".strip()
        if cur and d.tl(p, font) > ancho:
            lineas.append(cur)
            cur = w
        else:
            cur = p
    if cur:
        lineas.append(cur)
    # sin palabra corta sola en la ultima linea
    if len(lineas) > 1 and len(lineas[-1].split()) == 1:
        prev = lineas[-2].split()
        if len(prev) > 2:
            lineas[-2] = " ".join(prev[:-1])
            lineas[-1] = prev[-1] + " " + lineas[-1]
    return lineas


NO_FINAL = set("el la els les los las un una de del a al i y o en per para por que amb con tu teu teva su".split())


def equilibra(texto, font, ancho, d):
    """Como parte(), pero con lineas parejas y sin acabar en articulo o preposicion."""
    pal = texto.split()
    n = len(parte(texto, font, ancho, d))
    if n == 1:
        return [texto]
    mejor = None
    def busca(i, quedan, acc):
        nonlocal mejor
        if quedan == 1:
            l = " ".join(pal[i:])
            if d.tl(l, font) > ancho:
                return
            lin = acc + [l]
            anchos = [d.tl(x, font) for x in lin]
            coste = (max(anchos) - min(anchos) + 400 * sum(x.split()[-1].lower() in NO_FINAL for x in lin[:-1])
                     - 250 * sum(x.endswith(",") for x in lin[:-1]))
            if mejor is None or coste < mejor[0]:
                mejor = (coste, lin)
            return
        for k in range(i + 1, len(pal)):
            l = " ".join(pal[i:k])
            if d.tl(l, font) > ancho:
                break
            busca(k, quedan - 1, acc + [l])
    busca(0, n, [])
    return mejor[1] if mejor else parte(texto, font, ancho, d)


# ---------------------------------------------------------------- piezas

PALETAS = [((255, 214, 170), (240, 140, 90)), ((190, 220, 255), (90, 140, 220)),
           ((200, 238, 210), (70, 160, 110)), ((255, 205, 220), (200, 90, 130)),
           ((235, 225, 255), (130, 100, 210)), ((255, 236, 170), (220, 160, 40))]


# Fotos reales por tema (fotos/<sector>/, ver herramientas/banco_fotos.py).
# Si un tema no tiene sector o no hay fotos, se dibuja la ilustracion de siempre.
SECTOR = {
    "09_proceso": "oficina", "12_clinica": "dentista", "13_reformas": "reformas", "14_rural": "rural", "15_gimnasio": "gimnasio",
    "17_asesoria": "oficina", "18_estetica": "estetica", "23_busca": "peluqueria", "28_bienvenidos": "restaurante",
    "29_movil": "fisio", "30_taller": "taller", "31_tienda": "ferreteria", "32_turistas": "restaurante",
    "33_veterinario": "veterinario", "34_academia": "academia", "35_inmobiliaria": "inmobiliaria",
    "36_fotografo": "fotografo", "37_autoescuela": "autoescuela", "38_floristeria": "floristeria",
    "39_psicologo": "psicologo", "40_pasteleria": "pasteleria", "41_abogado": "abogado", "42_canina": "perros",
    "43_resena_mala": "restaurante", "45_dominio": "peluqueria", "46_datos": "taller", "48_web_nueva": "peluqueria",
    "49_bilingue": "ferreteria", "53_mayores": "farmacia", "54_presupuesto": "reformas", "55_web_y_ficha": "peluqueria",
    "58_oferta": "estetica", "59_preguntas": "taller", "60_boca": "fontaneria",
}
BANCO = []


def usa_banco(tema):
    """Carga las fotos del sector del tema (o del cafe/tienda generico)."""
    BANCO.clear()
    carpeta = RAIZ / "fotos" / SECTOR.get(tema, "cafe")
    BANCO.extend(sorted(carpeta.glob("*.jpg")) if carpeta.exists() else [])


def foto(w, h, i, r=14):
    """Hueco de foto: una foto real del sector del tema, recortada al hueco."""
    if BANCO:
        W2, H2 = int(w * S), int(h * S)
        src = Image.open(BANCO[i % len(BANCO)]).convert("RGB")
        k = max(W2 / src.width, H2 / src.height)
        src = src.resize((max(W2, int(src.width * k + 0.5)), max(H2, int(src.height * k + 0.5))), Image.LANCZOS)
        x, y = (src.width - W2) // 2, (src.height - H2) // 2
        im = src.crop((x, y, x + W2, y + H2))
        m = Image.new("L", (W2, H2), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, W2 - 1, H2 - 1], radius=int(r * S), fill=255)
        return im, m
    return foto_dibujada(w, h, i, r)


def foto_dibujada(w, h, i, r=14):
    """Hueco de foto ilustrado: degradado y formas. Nunca un gris plano."""
    a, b = PALETAS[i % len(PALETAS)]
    W2, H2 = int(w * S), int(h * S)
    im = Image.new("RGB", (W2, H2))
    px = ImageDraw.Draw(im)
    for y in range(H2):
        t = y / max(1, H2 - 1)
        px.line([(0, y), (W2, y)], fill=tuple(int(a[k] * (1 - t) + b[k] * t * 0.35 + a[k] * t * 0.65) for k in range(3)))
    sol = tuple(min(255, c + 30) for c in a)
    mont = tuple(int(c * 0.75) for c in b)
    mont2 = tuple(int(c * 0.9) for c in b)
    px.ellipse([W2 * 0.68, H2 * 0.14, W2 * 0.86, H2 * 0.14 + W2 * 0.18], fill=sol)
    px.polygon([(0, H2), (W2 * 0.35, H2 * 0.45), (W2 * 0.7, H2)], fill=mont2)
    px.polygon([(W2 * 0.3, H2), (W2 * 0.68, H2 * 0.55), (W2 * 1.05, H2)], fill=mont)
    m = Image.new("L", (W2, H2), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, W2 - 1, H2 - 1], radius=int(r * S), fill=255)
    return im, m


def pega_foto(base, xy, w, h, i, r=14):
    im, m = foto(w, h, i, r)
    base.paste(im, (int(xy[0] * S), int(xy[1] * S)), m)


def tarjeta(base, box, r=28, color=BLANCO):
    x0, y0, x1, y1 = box
    sombra = Image.new("L", base.size, 0)
    ImageDraw.Draw(sombra).rounded_rectangle([x0 * S, (y0 + 10) * S, x1 * S, (y1 + 12) * S], radius=r * S, fill=60)
    sombra = sombra.filter(ImageFilter.GaussianBlur(18 * S))
    base.paste(Image.new("RGB", base.size, (215, 210, 200)), (0, 0), sombra)
    D(base).rect(box, fill=color, r=r)


def senala(d, box, r=14):
    """Cerco amarillo: esto es lo que importa."""
    x0, y0, x1, y1 = box
    d.rect((x0 - 7, y0 - 7, x1 + 7, y1 + 7), outline=AMARILLO, r=r + 6, width=6)


def estrellas(d, x, y, n, tam=22, color=AMARILLO):
    for i in range(5):
        cx, cy = x + i * tam * 1.15 + tam / 2, y + tam / 2
        pts = []
        for k in range(10):
            ang = -math.pi / 2 + k * math.pi / 5
            rad = tam / 2 if k % 2 == 0 else tam / 4.6
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        d.poly(pts, fill=color if i < n else LINEA)


def casilla(d, x, y, marcada, tam=34):
    if marcada:
        d.rect((x, y, x + tam, y + tam), fill=AZUL, r=7)
        d.line((x + tam * .24, y + tam * .52, x + tam * .43, y + tam * .72, x + tam * .78, y + tam * .3), fill=BLANCO, width=4)
    else:
        d.rect((x, y, x + tam, y + tam), outline=(200, 205, 215), r=7, width=3)


def boton(d, box, txt, font, fondo, color):
    d.rect(box, fill=fondo, r=(box[3] - box[1]) / 2)
    d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), txt, font, color, anchor="mm")


def telefono(d, box):
    """Marco de movil; devuelve la caja de pantalla."""
    x0, y0, x1, y1 = box
    d.rect(box, fill=(24, 28, 40), r=46)
    d.rect((x0 + 12, y0 + 12, x1 - 12, y1 - 12), fill=BLANCO, r=36)
    d.rect(((x0 + x1) / 2 - 50, y0 + 22, (x0 + x1) / 2 + 50, y0 + 44), fill=(24, 28, 40), r=11)
    return (x0 + 12, y0 + 12, x1 - 12, y1 - 12)


def icono_whatsapp(d, cx, cy, r, fondo=VERDE):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fondo)
    d.ellipse((cx - r * .55, cy - r * .55, cx + r * .55, cy + r * .55), outline=BLANCO, width=max(2, r * .14))
    d.poly([(cx - r * .55, cy + r * .35), (cx - r * .7, cy + r * .75), (cx - r * .25, cy + r * .55)], fill=BLANCO)


def cabe_fila(d, et, val, peso_et, peso_val, tam_et, tam_val, ancho, hueco=36):
    """Reduce los dos cuerpos de letra hasta que etiqueta y valor caben en la fila."""
    while tam_et > 18 and d.tl(et, f(peso_et, tam_et)) + (d.tl(val, f(peso_val, tam_val)) if val else 0) + hueco > ancho:
        tam_et -= 1
        tam_val = max(16, tam_val - 1)
    return f(peso_et, tam_et), f(peso_val, tam_val)


# ---------------------------------------------------------------- maquetas
# Cada maqueta dibuja dentro de la caja de trabajo de la tarjeta y recibe
# sus textos del JSON (asi cada idioma lleva los suyos).

def m_ficha(base, d, box, m, ctx):
    """Ficha de negocio tipo buscador de mapas, con filas de datos."""
    x0, y0, x1, y1 = box
    pega_foto(base, (x0, y0), x1 - x0, 150, 1, 18)
    y = y0 + 180
    d.text((x0, y), ctx["negocio"], f("Bold", 40), AZUL)
    y += 58
    d.text((x0, y), m.get("valoracion", "4,7"), f("SemiBold", 26), GRIS)
    estrellas(d, x0 + d.tl(m.get("valoracion", "4,7"), f("SemiBold", 26)) + 14, y + 3, 5, 22)
    y += 62
    filas = m["filas"]
    alto = (y1 - y) / len(filas)
    for i, (et, val, mal) in enumerate(filas):
        fy = y + i * alto
        cy = fy + alto / 2
        d.ellipse((x0, cy - 16, x0 + 32, cy + 16), fill=FONDO_FILA, outline=LINEA, width=2)
        fe, fv = cabe_fila(d, et, val, "SemiBold", "Medium", 31, 29, x1 - x0 - 52)
        d.text((x0 + 52, cy), et, fe, AZUL, anchor="lm")
        d.text((x1, cy), val, fv, ROJO if mal else GRIS, anchor="rm")
        if mal:
            senala(d, (x0 - 6, cy - alto / 2 + 10, x1 + 6, cy + alto / 2 - 10))
        elif i < len(filas) - 1:
            d.line((x0, fy + alto, x1, fy + alto), LINEA, 2)


def m_lista(base, d, box, m, ctx):
    """Lista con casillas o precios; una fila puede ir senalada."""
    x0, y0, x1, y1 = box
    d.text((x0, y0), m["titulo"], f("Bold", 40), AZUL)
    y = y0 + 84
    filas = m["filas"]
    alto = min(118, (y1 - y) / len(filas))
    y += ((y1 - y) - alto * len(filas)) / 2
    for i, fila in enumerate(filas):
        et, val, estado = fila
        cy = y + i * alto + alto / 2
        tx = x0
        if m.get("casillas"):
            casilla(d, x0, cy - 17, estado != "mal")
            tx = x0 + 58
        fe, fv = cabe_fila(d, et, val, "SemiBold", "Medium" if estado != "bien" else "Bold", 34, 32, x1 - tx)
        d.text((tx, cy), et, fe, AZUL, anchor="lm")
        d.text((x1, cy), val, fv, ROJO if estado == "mal" else (AZUL if estado == "bien" else GRIS), anchor="rm")
        if estado == "mal":
            senala(d, (x0 - 6, cy - alto / 2 + 12, x1 + 6, cy + alto / 2 - 12))
        elif i < len(filas) - 1:
            d.line((x0, cy + alto / 2, x1, cy + alto / 2), LINEA, 2)


def m_galeria(base, d, box, m, ctx):
    x0, y0, x1, y1 = box
    d.text((x0, y0), m["titulo"], f("Bold", 36), AZUL)
    gy = y0 + 76
    cols, filas, hueco = 3, 2, 18
    cw = (x1 - x0 - hueco * (cols - 1)) / cols
    ch = (y1 - gy - 60 - hueco) / filas
    etiquetas = m.get("etiquetas", [])
    for k in range(cols * filas):
        cx = x0 + (k % cols) * (cw + hueco)
        cy = gy + (k // cols) * (ch + hueco)
        pega_foto(base, (cx, cy), cw, ch, k + 2, 16)
        if k < len(etiquetas) and etiquetas[k]:
            ft = f("Bold", 20)
            tw = d.tl(etiquetas[k], ft)
            d.rect((cx + 12, cy + ch - 46, cx + 32 + tw, cy + ch - 12), fill=(255, 255, 255), r=17)
            d.text((cx + 22, cy + ch - 29), etiquetas[k], ft, AZUL, anchor="lm")
    d.text((x0, y1 - 22), m["pie"], f("Medium", 24), GRIS, anchor="lm")


def m_resenas(base, d, box, m, ctx, solo_medir=False):
    x0, y0, x1, y1 = box
    if not solo_medir:
        alto = m_resenas(base, d, box, m, ctx, solo_medir=True)
        y0 = y0 + max(0, (y1 - y0 - alto) / 2)
    y = y0
    ft, fr = f("Medium", 28), f("Medium", 25)
    for i, r in enumerate(m["resenas"]):
        if not solo_medir:
            d.ellipse((x0, y, x0 + 64, y + 64), fill=PALETAS[i + 1][1])
            d.text((x0 + 32, y + 32), r["nombre"][0], f("Bold", 28), BLANCO, anchor="mm")
            d.text((x0 + 84, y + 2), r["nombre"], f("Bold", 30), AZUL)
            estrellas(d, x0 + 84, y + 42, r["estrellas"], 22)
        ty = y + 88
        for l in parte(r["texto"], ft, x1 - x0, d):
            if not solo_medir:
                d.text((x0, ty), l, ft, (60, 66, 80))
            ty += 40
        y = ty + 14
        if r.get("respuesta"):
            lineas = parte(r["respuesta"], fr, x1 - x0 - 110, d)
            alto = 66 + 36 * len(lineas)
            caja = (x0 + 40, y, x1, y + alto)
            if not solo_medir:
                d.rect(caja, fill=FONDO_FILA, r=16)
                d.text((x0 + 66, y + 20), m["respuesta_titulo"], f("Bold", 24), AZUL)
                ly = y + 56
                for l in lineas:
                    d.text((x0 + 66, ly), l, fr, GRIS)
                    ly += 36
                senala(d, caja, 16)
            y += alto + 26
        if i < len(m["resenas"]) - 1:
            if not solo_medir:
                d.line((x0, y, x1, y), LINEA, 2)
            y += 30
    return y - y0


def m_movil_boton(base, d, box, m, ctx):
    """Movil con la web del negocio y un boton de WhatsApp senalado."""
    x0, y0, x1, y1 = box
    pw = 420
    px0 = (x0 + x1) / 2 - pw / 2
    sx0, sy0, sx1, sy1 = telefono(d, (px0, y0 - 4, px0 + pw, y1 + 4))
    y = sy0 + 50
    d.text((sx0 + 26, y), ctx["dominio"], f("Medium", 17), GRIS)
    y += 36
    # la foto se queda con el sitio que dejan los textos y el boton
    ft1, ft2 = f("ExtraBold", 30), f("Medium", 21)
    l1 = parte(m["titular"], ft1, sx1 - sx0 - 52, d)
    l2 = parte(m["texto"], ft2, sx1 - sx0 - 52, d)
    alto_txt = 38 * len(l1) + 8 + 28 * len(l2)
    fh = min(260, (sy1 - 96 - 30) - y - 24 - alto_txt)
    pega_foto(base, (sx0 + 18, y), sx1 - sx0 - 36, fh, 3, 16)
    y += fh + 24
    for l in parte(m["titular"], f("ExtraBold", 30), sx1 - sx0 - 52, d):
        d.text((sx0 + 26, y), l, f("ExtraBold", 30), AZUL)
        y += 38
    y += 8
    for l in parte(m["texto"], f("Medium", 21), sx1 - sx0 - 52, d):
        d.text((sx0 + 26, y), l, f("Medium", 21), GRIS)
        y += 28
    by = sy1 - 96
    caja = (sx0 + 22, by, sx1 - 22, by + 60)
    d.rect(caja, fill=VERDE, r=30)
    icono_whatsapp(d, caja[0] + 34, by + 30, 15, fondo=(30, 140, 78))
    tb = 22
    while d.tl(m["boton"], f("Bold", tb)) > caja[2] - caja[0] - 80:
        tb -= 1
    d.text((caja[0] + 62, by + 30), m["boton"], f("Bold", tb), BLANCO, anchor="lm")
    senala(d, caja, 30)


def empeora(im, txt):
    """La misma foto, «antes»: segun lo que diga la etiqueta (flash, sucio,
    filtro...) o, si no, apagada y en gris."""
    from PIL import ImageEnhance
    t = txt.lower()
    if "flash" in t:
        # flash: centro quemado y fondo negro
        im = ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(1.9)).enhance(1.6)
        w, h = im.size
        luz = Image.new("L", im.size, 0)
        ImageDraw.Draw(luz).ellipse((w * 0.25, h * 0.2, w * 0.75, h * 0.7), fill=200)
        luz = luz.filter(ImageFilter.GaussianBlur(w * 0.12))
        im = Image.composite(Image.new("RGB", im.size, (255, 255, 250)), im, luz)
        borde = Image.new("L", im.size, 255)
        ImageDraw.Draw(borde).ellipse((-w * 0.1, -h * 0.1, w * 1.1, h * 1.1), fill=0)
        return Image.composite(Image.new("RGB", im.size, (10, 10, 10)), im, borde.filter(ImageFilter.GaussianBlur(w * 0.08)))
    if "limpi" in t:
        return im.filter(ImageFilter.GaussianBlur(5 * S))
    if "filtro" in t:
        im = ImageEnhance.Color(im).enhance(2.3)
        return Image.blend(im, Image.new("RGB", im.size, (255, 140, 40)), 0.25)
    if "recog" in t:
        return ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(0.6)).enhance(0.75)
    # por defecto: vieja y apagada (gris amarillento, oscura, sin contraste)
    im = Image.blend(im.convert("L").convert("RGB"), Image.new("RGB", im.size, (150, 125, 85)), 0.3)
    return ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(0.72)).enhance(0.75)


def m_antes_despues(base, d, box, m, ctx):
    x0, y0, x1, y1 = box
    mid = (x0 + x1) / 2
    h = y1 - y0 - 70
    i = m.get("foto", 2)
    im1, msk = foto(mid - x0 - 6, h, i, 18)
    base.paste(empeora(im1, m["antes"]), (int(x0 * S), int(y0 * S)), msk)
    pega_foto(base, (mid + 6, y0), x1 - mid - 6, h, i, 18)
    for x, txt, fondo, color in ((x0, m["antes"], AZUL, BLANCO), (mid + 6, m["despues"], AMARILLO, AZUL)):
        ft = f("Bold", 24)
        tw = d.tl(txt, ft)
        d.rect((x + 16, y0 + 16, x + 44 + tw, y0 + 62), fill=fondo, r=23)
        d.text((x + 30, y0 + 39), txt, ft, color, anchor="lm")
    d.text((x0, y1 - 26), m["pie"], f("SemiBold", 25), GRIS, anchor="lm")


def m_zonas(base, d, box, m, ctx):
    x0, y0, x1, y1 = box
    mh = 330
    d.rect((x0, y0, x1, y0 + mh), fill=(233, 240, 228), r=18)
    d.rect((x0 + 330, y0, x0 + 470, y0 + mh), fill=(214, 230, 245), r=0)
    d.rect((x0, y0, x1, y0 + mh), outline=LINEA, r=18, width=2)
    for xy in ((x0, y0 + 110, x1, y0 + 150), (x0 + 120, y0, x0 + 520, y0 + mh), (x0 + 600, y0, x0 + 700, y0 + mh)):
        d.line(xy, BLANCO, 10)
    pins = [(x0 + 210, y0 + 90), (x0 + 560, y0 + 190), (x0 + 380, y0 + 250), (x0 + 700, y0 + 80), (x0 + 120, y0 + 240)]
    for i, (px, py) in enumerate(pins[:len(m["zonas"])]):
        c = ROJO if i == 0 else AZUL
        d.ellipse((px - 20, py - 46, px + 20, py - 6), fill=c)
        d.poly([(px - 14, py - 18), (px + 14, py - 18), (px, py + 4)], fill=c)
        d.ellipse((px - 8, py - 34, px + 8, py - 18), fill=BLANCO)
    y = y0 + mh + 36
    d.text((x0, y), m["titulo"], f("Bold", 34), AZUL)
    y += 62
    cx = x0
    ft = f("SemiBold", 29)
    for z in m["zonas"]:
        tw = d.tl(z, ft) + 44
        if cx + tw > x1:
            cx = x0
            y += 70
        d.rect((cx, y, cx + tw, y + 56), fill=FONDO_FILA, outline=LINEA, r=28, width=2)
        d.text((cx + tw / 2, y + 28), z, ft, AZUL, anchor="mm")
        cx += tw + 14
    senala(d, (x0, y0 + mh + 94 - 6, x1, y + 56), 20)


def m_pasos(base, d, box, m, ctx):
    x0, y0, x1, y1 = box
    d.text((x0, y0), m["titulo"], f("Bold", 36), AZUL)
    pasos = m["pasos"]
    y = y0 + 96
    paso = (y1 - y) / len(pasos)
    for i, (t, sub) in enumerate(pasos):
        cy = y + i * paso + 34
        if i < len(pasos) - 1:
            d.line((x0 + 34, cy + 34, x0 + 34, cy + paso - 34), LINEA, 4)
        activo = i == m.get("senalado", -1)
        d.ellipse((x0, cy - 34, x0 + 68, cy + 34), fill=AMARILLO if activo else AZUL)
        d.text((x0 + 34, cy), str(i + 1), f("ExtraBold", 30), AZUL if activo else BLANCO, anchor="mm")
        d.text((x0 + 98, cy - 18), t, f("Bold", 34), AZUL, anchor="lm")
        d.text((x0 + 98, cy + 24), sub, f("Medium", 27), GRIS, anchor="lm")


def m_chat(base, d, box, m, ctx):
    """Conversacion de WhatsApp en un movil."""
    x0, y0, x1, y1 = box
    pw = 440
    px0 = (x0 + x1) / 2 - pw / 2
    sx0, sy0, sx1, sy1 = telefono(d, (px0, y0 - 4, px0 + pw, y1 + 4))
    d.rect((sx0, sy0, sx1, sy0 + 110), fill=(18, 110, 90), r=36)
    d.rect((sx0, sy0 + 60, sx1, sy0 + 110), fill=(18, 110, 90))
    d.ellipse((sx0 + 22, sy0 + 58, sx0 + 62, sy0 + 98), fill=AMARILLO)
    d.text((sx0 + 76, sy0 + 78), ctx["negocio"], f("Bold", 23), BLANCO, anchor="lm")
    d.rect((sx0, sy0 + 110, sx1, sy1), fill=(236, 229, 221))
    d.rect((sx0, sy1 - 40, sx1, sy1), fill=(236, 229, 221), r=36)
    y = sy0 + 134
    ft = f("Medium", 26)
    for g in m["globos"]:
        mio = g["de"] == "cliente"
        if g.get("fotos"):
            gw, gh = 170, 122
            gx = sx1 - 18 - gw * 2 - 8
            for k in range(2):
                pega_foto(base, (gx + k * (gw + 8), y), gw, gh, k + 1, 12)
            y += gh + 14
            continue
        lineas = parte(g["texto"], ft, 300, d)
        gw = max(d.tl(l, ft) for l in lineas) + 30
        gh = 28 + 34 * len(lineas)
        gx = sx1 - 18 - gw if mio else sx0 + 18
        d.rect((gx, y, gx + gw, y + gh), fill=(217, 253, 211) if mio else BLANCO, r=14)
        ly = y + 12
        for l in lineas:
            d.text((gx + 16, ly), l, ft, AZUL)
            ly += 34
        y += gh + 14


def _navegador(d, box, dominio):
    x0, y0, x1, y1 = box
    d.rect(box, fill=BLANCO, outline=LINEA, r=18, width=2)
    d.rect((x0, y0, x1, y0 + 46), fill=FONDO_FILA, r=18)
    d.rect((x0, y0 + 30, x1, y0 + 46), fill=FONDO_FILA)
    for i, c in enumerate(((255, 95, 87), (254, 188, 46), (40, 200, 64))):
        d.ellipse((x0 + 18 + i * 22, y0 + 16, x0 + 32 + i * 22, y0 + 30), fill=c)
    d.rect((x0 + 110, y0 + 10, x1 - 30, y0 + 36), fill=BLANCO, r=13)
    d.text((x0 + 128, y0 + 23), dominio, f("Medium", 17), GRIS, anchor="lm")
    return (x0, y0 + 46, x1, y1)


def etiqueta_mal(d, x, y, txt, ancla="l"):
    ft = f("Bold", 24)
    tw = d.tl(txt, ft) + 40
    if ancla == "r":
        x -= tw
    d.rect((x, y, x + tw, y + 46), fill=ROJO, r=23)
    d.text((x + tw / 2, y + 23), txt, ft, BLANCO, anchor="mm")


def m_web(base, d, box, m, ctx):
    """Primera pantalla de una web en el navegador. `senala` marca una pieza."""
    x0, y0, x1, y1 = box
    bx0, by0, bx1, by1 = _navegador(d, box, m.get("dominio", ctx["dominio"]))
    y = by0 + 22
    d.text((bx0 + 26, y + 14), m.get("negocio", ctx["negocio"]), f("ExtraBold", 21), AZUL, anchor="lm")
    mx = bx1 - 26
    for it in reversed(m.get("menu", [])):
        ft = f("Medium", 17)
        d.text((mx, y + 14), it, ft, GRIS, anchor="rm")
        mx -= d.tl(it, ft) + 24
    d.line((bx0, y + 42, bx1, y + 42), LINEA, 2)
    hx0, hy0 = bx0 + 30, y + 74
    col = (bx1 - bx0) * 0.56
    fw = bx1 - (bx0 + col) - 26
    pega_foto(base, (bx0 + col, hy0 - 6), fw, by1 - hy0 - 22, m.get("foto", 0), 16)
    ancho = col - 52
    cajas = {}
    ft = f("ExtraBold", m.get("tam_titulo", 40))
    ty = hy0
    lin = parte(m["titulo"], ft, ancho, d)
    for l in lin:
        d.text((hx0, ty), l, ft, AZUL)
        ty += m.get("tam_titulo", 40) * 1.15
    cajas["titulo"] = (hx0 - 4, hy0 - 6, hx0 + max(d.tl(l, ft) for l in lin) + 4, ty)
    ty += 12
    fs = f("Medium", 21)
    sy = ty
    for l in parte(m["subtitulo"], fs, ancho, d):
        d.text((hx0, ty), l, fs, GRIS)
        ty += 29
    cajas["subtitulo"] = (hx0 - 4, sy - 4, hx0 + ancho, ty)
    if m.get("lugar"):
        ty += 14
        d.ellipse((hx0, ty + 2, hx0 + 20, ty + 22), fill=ROJO)
        d.ellipse((hx0 + 6, ty + 8, hx0 + 14, ty + 16), fill=BLANCO)
        fl = f("Bold", 22)
        d.text((hx0 + 30, ty + 12), m["lugar"], fl, AZUL, anchor="lm")
        cajas["lugar"] = (hx0 - 4, ty - 4, hx0 + 34 + d.tl(m["lugar"], fl), ty + 28)
        ty += 30
    if m.get("valoracion"):
        ty += 16
        estrellas(d, hx0, ty, 5, 22)
        fv = f("SemiBold", 20)
        d.text((hx0 + 140, ty + 11), m["valoracion"], fv, AZUL, anchor="lm")
        cajas["valoracion"] = (hx0 - 4, ty - 6, hx0 + 144 + d.tl(m["valoracion"], fv), ty + 30)
        ty += 30
    if m.get("boton"):
        ty += 22
        fb = f("Bold", 21)
        bw = d.tl(m["boton"], fb) + 80
        caja = (hx0, ty, hx0 + bw, ty + 52)
        d.rect(caja, fill=VERDE, r=26)
        icono_whatsapp(d, hx0 + 30, ty + 26, 13, fondo=(30, 140, 78))
        d.text((hx0 + 52, ty + 26), m["boton"], fb, BLANCO, anchor="lm")
        cajas["boton"] = caja
    cajas["todo"] = (hx0 - 12, hy0 - 14, hx0 + ancho + 8, (cajas["boton"][3] if "boton" in cajas else ty) + 10)
    if m.get("senala") in cajas:
        senala(d, cajas[m["senala"]], 12)
    if m.get("mal"):
        etiqueta_mal(d, hx0, cajas["todo"][3] + 16, m["mal"])


def m_movil(base, d, box, m, ctx):
    """Movil grande con un fallo tipico de web no pensada para movil."""
    x0, y0, x1, y1 = box
    # movil de tamano fijo: si la caja es mas baja, se corta por abajo
    alto = max(y1 - y0, 820)
    pw = 430
    px0 = (x0 + x1) / 2 - pw / 2
    sx0, sy0, sx1, sy1 = telefono(d, (px0, y0 - 4, px0 + pw, y0 + alto + 4))
    sw = sx1 - sx0
    # barra de direccion
    d.rect((sx0 + 16, sy0 + 50, sx1 - 16, sy0 + 82), fill=FONDO_FILA, r=16)
    d.text((sx0 + 32, sy0 + 66), ctx["dominio"], f("Medium", 15), GRIS, anchor="lm")
    y = sy0 + 100
    v = m["variante"]
    if v == "zoom":
        # web de ordenador encogida: todo diminuto
        d.text((sx0 + 20, y), ctx["negocio"], f("Bold", 11), AZUL)
        d.text((sx1 - 20, y), m.get("menu_txt", ""), f("Medium", 7), GRIS, anchor="ra")
        y += 24
        pega_foto(base, (sx0 + 20, y), sw * 0.5, 120, 1, 6)
        for k in range(9):
            d.rect((sx0 + 30 + sw * 0.5, y + 6 + k * 13, sx1 - 24 - (k % 3) * 18, y + 11 + k * 13), fill=LINEA, r=2)
        y += 140
        for k in range(16):
            d.rect((sx0 + 20, y + k * 14, sx1 - 20 - (k % 4) * 30, y + 5 + k * 14), fill=LINEA, r=2)
        # gesto de pellizco
        cx, cy = (sx0 + sx1) / 2, y + 90
        for dx in (-38, 38):
            d.ellipse((cx + dx - 26, cy - 26, cx + dx + 26, cy + 26), fill=(255, 236, 170), outline=AMARILLO, width=4)
        d.line((cx - 10, cy, cx + 10, cy), AMARILLO, 4)
        etiqueta_mal(d, (sx0 + sx1) / 2 - d.tl(m["etiqueta"], f("Bold", 24)) / 2 - 20, cy + 46, m["etiqueta"])
    elif v == "telefono":
        pega_foto(base, (sx0 + 16, y), sw - 32, 200, 4, 14)
        y += 222
        d.text((sx0 + 22, y), ctx["negocio"], f("ExtraBold", 26), AZUL)
        y += 44
        d.text((sx0 + 22, y), m["texto"], f("Medium", 20), GRIS)
        y += 46
        ft = f("Medium", 24)
        d.text((sx0 + 22, y), m["telefono"], ft, (70, 76, 90))
        tw = d.tl(m["telefono"], ft)
        caja = (sx0 + 16, y - 8, sx0 + 30 + tw, y + 34)
        senala(d, caja, 10)
        cx, cy = sx0 + 30 + tw * 0.6, y + 14
        d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), outline=ROJO, width=4)
        etiqueta_mal(d, sx0 + 16, y + 70, m["etiqueta"])
    elif v == "blanco":
        d.rect((sx0 + 16, sy0 + 86, sx0 + 16 + (sw - 32) * 0.18, sy0 + 92), fill=(60, 130, 240), r=3)
        cx, cy = (sx0 + sx1) / 2, sy0 + 260
        d.ellipse((cx - 44, cy - 44, cx + 44, cy + 44), outline=LINEA, width=9)
        d.d.arc([(cx - 44) * S, (cy - 44) * S, (cx + 44) * S, (cy + 44) * S], 200, 300, fill=GRIS_CLARO, width=int(9 * S))
        etiqueta_mal(d, cx - d.tl(m["etiqueta"], f("Bold", 24)) / 2 - 20, cy + 80, m["etiqueta"])
    elif v == "juntos":
        d.text((sx0 + 22, y), ctx["negocio"], f("ExtraBold", 24), AZUL)
        y += 50
        ft = f("Medium", 16)
        for k, it in enumerate(m["enlaces"]):
            d.text((sx0 + 24, y + k * 22), it, ft, (40, 90, 200))
        dedo = y + 2 * 22 + 8
        d.ellipse((sx0 + 40, dedo - 32, sx0 + 104, dedo + 32), fill=(255, 220, 190), outline=(230, 170, 140), width=3)
        senala(d, (sx0 + 18, y + 22 - 4, sx0 + 200, y + 4 * 22 + 4), 8)
        y += len(m["enlaces"]) * 22 + 30
        for k in range(10):
            d.rect((sx0 + 22, y + k * 16, sx1 - 22 - (k % 3) * 40, y + 6 + k * 16), fill=LINEA, r=3)
        etiqueta_mal(d, sx0 + 18, y - 14, m["etiqueta"])
    elif v == "formulario":
        d.text((sx0 + 22, y), m["titulo"], f("ExtraBold", 24), AZUL)
        y += 48
        ft = f("Medium", 17)
        for campo in m["campos"]:
            d.text((sx0 + 22, y), campo, ft, GRIS)
            y += 24
            alto = 90 if campo == m["campos"][-1] else 40
            d.rect((sx0 + 22, y, sx1 - 22, y + alto), outline=LINEA, r=8, width=2)
            y += alto + 14
        d.rect((sx0 + 22, y, sx0 + 150, y + 44), fill=(200, 205, 215), r=8)
        d.text((sx0 + 86, y + 22), m["enviar"], f("Bold", 17), BLANCO, anchor="mm")
        etiqueta_mal(d, sx1 - 18, sy0 + 92, m["etiqueta"], ancla="r")


MAQUETAS = {"ficha": m_ficha, "lista": m_lista, "galeria": m_galeria, "resenas": m_resenas,
            "movil_boton": m_movil_boton, "antes_despues": m_antes_despues,
            "zonas": m_zonas, "pasos": m_pasos, "chat": m_chat,
            "web": m_web, "movil": m_movil}


def con_escala(base, box, k, fn, m, ctx):
    """Dibuja una maqueta como si la caja midiera box/k y la amplia (k>1) o
    reduce (k<1) entera: textos, fotos y margenes mantienen su proporcion."""
    global S
    # margen alrededor para que los cercos amarillos no se corten
    pad = 18
    x0, y0, x1, y1 = box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad
    bw, bh = x1 - x0, y1 - y0
    sub = Image.new("RGB", (int(bw * S), int(bh * S)), BLANCO)
    s0 = S
    S = s0 * k
    try:
        fn(sub, D(sub), (pad / k, pad / k, (bw - pad) / k, (bh - pad) / k), m, ctx)
    finally:
        S = s0
    base.paste(sub, (int(x0 * S), int(y0 * S)))


def dibuja_maqueta(base, box, m, ctx, entero=False):
    fn = MAQUETAS[m["tipo"]]
    if m["tipo"] == "movil":
        # en el gancho se ve el movil entero; en las laminas, grande y cortado
        con_escala(base, box, (box[3] - box[1]) / 820 if entero else m.get("k", 1.0), fn, m, ctx)
    elif m.get("k"):
        con_escala(base, box, m["k"], fn, m, ctx)
    else:
        fn(base, D(base), box, m, ctx)


# ---------------------------------------------------------------- laminas

def etiqueta(c):
    # Pablo trabaja en toda Espana: fuera el «· Girona» de las etiquetas viejas
    return re.sub(r"\s*·\s*Girona\s*$", "", c["etiqueta"]).upper()


def portada(c):
    """Portada: pastilla, titulo grande y, debajo, el problema dibujado (la
    maqueta del gancho) asomando por abajo, girada, con una flecha de deslizar."""
    im = lienzo(AZUL)
    d = D(im)
    ft = f("SemiBold", 26)
    d.text((MARGEN, 130), etiqueta(c), ft, GRIS_CLARO, anchor="lm")
    fp = f("ExtraBold", 34)
    pw = d.tl(c["pastilla"].upper(), fp) + 64
    y = 200
    d.rect((MARGEN, y, MARGEN + pw, y + 70), fill=AMARILLO, r=35)
    d.text((MARGEN + 32, y + 36), c["pastilla"].upper(), fp, AZUL, anchor="lm")
    font, lin, tam = ajusta_titulo(c["portada"], "Black", 120, 64, W - 2 * MARGEN, 400, 4, d, interlinea=1.04)
    y_fin = escribe_titulo(d, MARGEN, y + 112, font, lin, tam, BLANCO, interlinea=1.04)
    m = (c.get("gancho") or {}).get("maqueta")
    if m:
        # la tarjeta mide siempre lo mismo y se corta por abajo: «hay mas, desliza»
        movil = m["tipo"] == "movil"
        cw, ch = (840, 900) if m["tipo"] in ("movil", "chat", "ficha") else (840, 620)
        sub = Image.new("RGB", (int(cw * S), int(ch * S)), BLANCO)
        dibuja_maqueta(sub, (40, 40, cw - 40, ch - 40), m, c, entero=movil)
        msk = Image.new("L", sub.size, 0)
        ImageDraw.Draw(msk).rounded_rectangle([0, 0, sub.width - 1, sub.height - 1], radius=int(30 * S), fill=255)
        sub = sub.convert("RGBA")
        sub.putalpha(msk)
        sub = sub.rotate(-3, resample=Image.BICUBIC, expand=True)
        top = max(y_fin + 70, 640)
        x = (W - cw) / 2 + 20
        sombra = Image.new("L", im.size, 0)
        sombra.paste(sub.getchannel("A").point(lambda a: a * 0.55), (int(x * S), int((top + 24) * S)))
        sombra = sombra.filter(ImageFilter.GaussianBlur(26 * S))
        im.paste(Image.new("RGB", im.size, (0, 0, 0)), (0, 0), sombra)
        im.paste(sub, (int(x * S), int(top * S)), sub)
        d = D(im)
    # flecha de deslizar
    cx, cy, r = W - MARGEN - 46, H - 120, 58
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=AMARILLO)
    d.line((cx - 22, cy, cx + 20, cy), AZUL, 9)
    d.line((cx + 2, cy - 20, cx + 22, cy, cx + 2, cy + 20), AZUL, 9)
    if not m:
        d.text((MARGEN, H - 120), c["desliza"], f("SemiBold", 40), GRIS_CLARO, anchor="lm")
    return im


def contenido(c, n, lam):
    im = lienzo(CREMA)
    d = D(im)
    fn = f("Black", 110)
    num = f"{n:02d}"
    d.text((MARGEN, 190), num, fn, AMARILLO, anchor="ls")
    d.text((MARGEN + d.tl(num, fn) + 26, 168), c["de"], f("SemiBold", 34), GRIS, anchor="ls")
    font, lin, tam = ajusta_titulo(lam["titulo"], "Black", 74, 46, W - 2 * MARGEN, 170, 2, d)
    y_fin = escribe_titulo(d, MARGEN, 232, font, lin, tam, AZUL)
    caja = (100, max(410, y_fin + 46), W - 100, 1072)
    tarjeta(im, caja)
    d = D(im)
    m = lam["maqueta"]
    dibuja_maqueta(im, (caja[0] + 46, caja[1] + 46, caja[2] - 46, caja[3] - 46), m, c)
    d = D(im)
    fnota = f("Bold", 38)
    lineas = equilibra(lam["nota"], fnota, W - 2 * 100 - 64, d)
    alto = 44 + 50 * len(lineas)
    d.rect((100, 1096, W - 100, 1096 + alto), fill=AMARILLO, r=26)
    ly = 1096 + 22 + 25
    for l in lineas:
        d.text((132, ly), l, fnota, AZUL, anchor="lm")
        ly += 50
    return im


def cierre(c):
    im = lienzo(AZUL)
    d = D(im)
    logo = Image.open(RAIZ / "logo" / "logo.png").convert("RGBA")
    lw = 250
    lh = lw * logo.height / logo.width
    logo = logo.resize((int(lw * S), int(lh * S)), Image.LANCZOS)
    ff = f("Bold", 50)
    lineas = equilibra(c["cierre"], ff, W - 2 * 110, d)
    alto = lh + 110 + 62 * len(lineas) + 50 + 34 + 46 + 104 + 60 + 58 + 52 + 40
    y = (H - alto) / 2
    im.paste(logo, (int((W - lw) / 2 * S), int(y * S)), logo)
    y += lh + 110
    for l in lineas:
        d.text((W / 2, y + 31), l, ff, BLANCO, anchor="mm")
        y += 62
    y += 50
    d.text((W / 2, y + 17), c["guardar"], f("SemiBold", 30), GRIS_CLARO, anchor="mm")
    y += 34 + 46
    fc = f("ExtraBold", 44)
    cw = d.tl(c["cta"], fc) + 110
    boton(d, ((W - cw) / 2, y, (W + cw) / 2, y + 104), c["cta"], fc, AMARILLO, AZUL)
    y += 104 + 60
    d.text((W / 2, y + 29), TELEFONO, f("ExtraBold", 50), AMARILLO, anchor="mm")
    y += 58 + 52
    d.text((W / 2, y + 20), DOMINIO_PM, f("SemiBold", 36), GRIS_CLARO, anchor="mm")
    return im


def gancho(c):
    """Pantalla de gancho del video (1080x1920): frase grande + el problema
    dibujado. Es lo primero que se ve y hace de miniatura."""
    g = c["gancho"]
    GW, GH = 1080, 1920
    im = Image.new("RGB", (GW * S, GH * S), AZUL)
    d = D(im)
    fp = f("ExtraBold", 38)
    pw = d.tl(g["pastilla"].upper(), fp) + 70
    y = 210
    d.rect((80, y, 80 + pw, y + 78), fill=AMARILLO, r=39)
    d.text((80 + 35, y + 40), g["pastilla"].upper(), fp, AZUL, anchor="lm")
    font, lin, tam = ajusta_titulo(g["texto"], "Black", 124, 70, GW - 160, 560, 4, d, interlinea=1.04)
    y_fin = escribe_titulo(d, 80, y + 118, font, lin, tam, BLANCO, interlinea=1.04)
    caja = (80, y_fin + 56, GW - 80, 1560)
    tarjeta(im, caja)
    d = D(im)
    dibuja_maqueta(im, (caja[0] + 40, caja[1] + 40, caja[2] - 40, caja[3] - 40), g["maqueta"], c)
    return im, (GW, GH)


def main():
    ruta = Path(sys.argv[1])
    c = json.loads(ruta.read_text(encoding="utf-8"))
    tema, idioma = c["id"].rsplit("_", 1)
    usa_banco(tema)
    base = RAIZ / "salida" / tema / idioma
    dest = base / "carrusel"
    guarda(portada(c), dest / "1_portada.png")
    for i, lam in enumerate(c["laminas"], 1):
        guarda(contenido(c, i, lam), dest / f"{i + 1}_{i:02d}.png")
    guarda(cierre(c), dest / "7_cierre.png")
    if c.get("gancho"):
        im, tam = gancho(c)
        # solo para el video: va fuera de carrusel/ para no subirla por error
        g = base / "gancho.png"
        im.resize(tam, Image.LANCZOS).save(g, optimize=True)
    print(f"-> {dest}")


if __name__ == "__main__":
    main()
