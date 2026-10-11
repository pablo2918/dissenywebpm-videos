"""Formato «Así no / Así sí» (sin voz). Ver planes/plan_bienmal.py."""
from PIL import Image, ImageDraw

import anima as A
from plan_bienmal import PIE

C = A.C
UI = {"es": {"no": "ASÍ NO", "si": "ASÍ SÍ"}, "ca": {"no": "AIXÍ NO", "si": "AIXÍ SÍ"}}
PW, PH = 920, 550                 # panel apaisado (uno encima del otro)
Y_MAL, Y_BIEN = 400, 975
LW, LH, LY = 495, 1080, 400       # panel alto (moviles, uno al lado del otro)
DUR_PAR = 6.0
K = {"movil": 1.0, "movil_boton": 1.0, "resenas": 1.28}
MOVILES = ("movil", "movil_boton")


def web_grande(base, d, box, m, ctx):
    """Primera pantalla de una web, con letra grande para leerla en el video."""
    x0, y0, x1, y1 = box
    d.rect(box, fill=C.BLANCO, outline=C.LINEA, r=18, width=2)
    d.rect((x0, y0, x1, y0 + 52), fill=C.FONDO_FILA, r=18)
    d.rect((x0, y0 + 34, x1, y0 + 52), fill=C.FONDO_FILA)
    for i, col in enumerate(((255, 95, 87), (254, 188, 46), (40, 200, 64))):
        d.ellipse((x0 + 20 + i * 24, y0 + 19, x0 + 36 + i * 24, y0 + 35), fill=col)
    d.rect((x0 + 120, y0 + 11, x1 - 24, y0 + 41), fill=C.BLANCO, r=15)
    d.text((x0 + 140, y0 + 26), ctx["dominio"], C.f("Medium", 22), C.GRIS, anchor="lm")
    x = x0 + 34
    y = y0 + 80
    d.text((x, y), ctx["negocio"], C.f("ExtraBold", 28), C.AZUL, anchor="lm")
    y += 36
    cajas = {}
    ft = C.f("ExtraBold", 54)
    ty = y
    lin = C.parte(m["titulo"], ft, x1 - x0 - 68, d)
    for l in lin:
        d.text((x, ty), l, ft, C.AZUL)
        ty += 62
    cajas["titulo"] = (x - 6, y - 4, x + max(d.tl(l, ft) for l in lin) + 6, ty + 4)
    ty += 16
    d.text((x, ty), m["subtitulo"], C.f("Medium", 30), C.GRIS)
    ty += 48
    if m.get("lugar"):
        d.ellipse((x, ty + 4, x + 26, ty + 30), fill=C.ROJO)
        d.ellipse((x + 8, ty + 12, x + 18, ty + 22), fill=C.BLANCO)
        fl = C.f("Bold", 32)
        d.text((x + 40, ty + 17), m["lugar"], fl, C.AZUL, anchor="lm")
        cajas["lugar"] = (x - 6, ty - 4, x + 46 + d.tl(m["lugar"], fl), ty + 38)
        ty += 52
    if m.get("boton"):
        fb = C.f("Bold", 30)
        bw = d.tl(m["boton"], fb) + 100
        caja = (x, ty, x + bw, ty + 66)
        d.rect(caja, fill=C.VERDE, r=33)
        C.icono_whatsapp(d, x + 38, ty + 33, 17, fondo=(30, 140, 78))
        d.text((x + 66, ty + 33), m["boton"], fb, C.BLANCO, anchor="lm")
        cajas["boton"] = caja
    if m.get("senala") in cajas:
        C.senala(d, cajas[m["senala"]], 12)
    if m.get("mal"):
        ft = C.f("Bold", 30)
        tw = d.tl(m["mal"], ft) + 48
        d.rect((x, ty, x + tw, ty + 58), fill=C.ROJO, r=29)
        d.text((x + tw / 2, ty + 29), m["mal"], ft, C.BLANCO, anchor="mm")


def ficha_grande(base, d, box, m, ctx):
    """Ficha de Google con letra grande: nombre, nota y tres filas."""
    x0, y0, x1, y1 = box
    d.text((x0, y0 + 26), ctx["negocio"], C.f("ExtraBold", 46), C.AZUL, anchor="lm")
    fv = C.f("SemiBold", 34)
    d.text((x0, y0 + 92), m.get("valoracion", "4,7"), fv, C.GRIS, anchor="lm")
    C.estrellas(d, x0 + d.tl(m.get("valoracion", "4,7"), fv) + 16, y0 + 76, 5, 32)
    y = y0 + 140
    alto = (y1 - y) / len(m["filas"])
    for i, (et, val, mal) in enumerate(m["filas"]):
        cy = y + i * alto + alto / 2
        fe, fval = C.cabe_fila(d, et, val, "SemiBold", "Bold" if mal else "Medium", 36, 34, x1 - x0)
        d.text((x0, cy), et, fe, C.AZUL, anchor="lm")
        d.text((x1, cy), val, fval, C.ROJO if mal else C.GRIS, anchor="rm")
        if mal:
            C.senala(d, (x0 - 8, cy - alto / 2 + 10, x1 + 8, cy + alto / 2 - 10))
        elif i < len(m["filas"]) - 1:
            d.line((x0, cy + alto / 2, x1, cy + alto / 2), C.LINEA, 2)


def chat_grande(base, d, box, m, ctx):
    """Conversacion de WhatsApp en grande (sin movil): se lee en el video."""
    x0, y0, x1, y1 = box
    d.rect(box, fill=(236, 229, 221), r=22)
    d.rect((x0, y0, x1, y0 + 74), fill=(18, 110, 90), r=22)
    d.rect((x0, y0 + 40, x1, y0 + 74), fill=(18, 110, 90))
    d.ellipse((x0 + 22, y0 + 15, x0 + 66, y0 + 59), fill=C.AMARILLO)
    d.text((x0 + 82, y0 + 37), ctx["negocio"], C.f("Bold", 28), C.BLANCO, anchor="lm")
    ft = C.f("Medium", 40)
    globos = []
    for g in m["globos"]:
        lin = C.parte(g["texto"], ft, 600, d)
        globos.append((g, lin, 30 + 50 * len(lin)))
    alto = sum(h for _, _, h in globos) + 22 * (len(globos) - 1)
    y = y0 + 74 + max(20, (y1 - y0 - 74 - alto) / 2)
    for g, lin, gh in globos:
        mio = g["de"] == "cliente"
        gw = max(d.tl(l, ft) for l in lin) + 40
        gx = x1 - 24 - gw if mio else x0 + 24
        d.rect((gx, y, gx + gw, y + gh), fill=(217, 253, 211) if mio else C.BLANCO, r=18)
        ly = y + 15
        for l in lin:
            d.text((gx + 20, ly), l, ft, C.AZUL)
            ly += 50
        y += gh + 22


def marca(bien):
    r = 44

    def dib(im, d):
        d.ellipse((0, 0, 2 * r, 2 * r), fill=C.BLANCO)
        d.ellipse((5, 5, 2 * r - 5, 2 * r - 5), fill=C.VERDE if bien else C.ROJO)
        if bien:
            d.line((r * .52, r * 1.02, r * .86, r * 1.36, r * 1.5, r * .66), fill=C.BLANCO, width=9)
        else:
            d.line((r * .62, r * .62, r * 1.38, r * 1.38), fill=C.BLANCO, width=9)
            d.line((r * 1.38, r * .62, r * .62, r * 1.38), fill=C.BLANCO, width=9)
    return A.sprite(2 * r, 2 * r, dib)


PROPIAS = {"chat_grande": chat_grande, "web": web_grande, "ficha": ficha_grande}


def panel(m, ctx, tag, bien, alto=False):
    pw, ph = (LW, LH) if alto else (PW, PH)

    def dib(im, d):
        d.rect((0, 0, pw, ph), fill=C.BLANCO, r=30)
        box = (40, 96, pw - 40, ph - 30)
        if m["tipo"] in PROPIAS:
            PROPIAS[m["tipo"]](im, d, box, m, ctx)
        else:
            mm = dict(m)
            mm.setdefault("k", K.get(m["tipo"], 1.0))
            C.dibuja_maqueta(im, box, mm, ctx)
            d = C.D(im)
        ft = C.f("ExtraBold", 30)
        tw = d.tl(tag, ft) + 60
        d.rect((30, 24, 30 + tw, 76), fill=C.VERDE if bien else C.ROJO, r=26)
        d.text((30 + tw / 2, 51), tag, ft, C.BLANCO, anchor="mm")
    return A.sprite(pw, ph, dib)


def hacer(v, idi, salida, rev, tmp):
    c = v[idi]
    ctx = {"negocio": c["negocio"], "dominio": c["dominio"]}
    pares = []
    for i, p in enumerate(c["parejas"]):
        alto = p["mal"]["tipo"] in MOVILES and p["bien"]["tipo"] in MOVILES
        pares.append({"alto": alto,
            "tit": A.titulo(p["titulo"], 900, 200, 78, 54, centrado=True, max_lineas=2, mayus=False),
            "num": A.pastilla(f"{i + 1}/{len(c['parejas'])}", 30),
            "mal": panel(p["mal"], ctx, UI[idi]["no"], False, alto),
            "bien": panel(p["bien"], ctx, UI[idi]["si"], True, alto)})
    m_mal, m_bien = marca(False), marca(True)
    t_final = DUR_PAR * len(pares)
    dur = t_final + 3.2
    final = A.tarjeta_final(idi, c["final"])
    fondo = Image.new("RGB", (A.W, A.H), A.AZUL)
    x0 = (A.W - PW) / 2

    def fotograma(t):
        im = fondo.copy()
        i = min(len(pares) - 1, int(t // DUR_PAR))
        p, tl = pares[i], t - i * DUR_PAR
        sal = A.eo(A.tramo(tl, DUR_PAR - 0.3, 0.3)) if i < len(pares) - 1 else 0
        # el primero ya esta en pantalla en el fotograma 0 (miniatura)
        e_mal = 1 if i == 0 else A.eo(A.tramo(tl, 0.0, 0.45))
        e_bien = A.eo(A.tramo(tl, 1.3, 0.45))
        a_tit = (1 if i == 0 else A.eo(A.tramo(tl, 0, 0.3))) * (1 - sal)
        A.pega(im, p["num"], (A.W - p["num"].width) / 2, 130, a=a_tit)
        A.pega(im, p["tit"], (A.W - p["tit"].width) / 2, 210 + (170 - p["tit"].height) / 2, a=a_tit)
        if p["alto"]:
            pos = ((30, LY), (A.W - 30 - LW, LY))
            ancho = LW
        else:
            pos = ((x0, Y_MAL), (x0, Y_BIEN))
            ancho = PW
        (xm, ym), (xb, yb) = pos
        A.pega(im, p["mal"], xm - 1100 * (1 - e_mal), ym - 80 * sal, a=e_mal * (1 - sal))
        A.pega(im, p["bien"], xb + 1100 * (1 - e_bien), yb - 80 * sal, a=e_bien * (1 - sal))
        for mk, t0, (x, y) in ((m_mal, 0.5 if i else 0.35, pos[0]), (m_bien, 1.8, pos[1])):
            e = A.tramo(tl, t0, 0.3)
            if e > 0:
                A.pega(im, mk, x + ancho - mk.width + 14, y - 24 - 80 * sal, a=(1 - sal),
                       k=1.5 - 0.5 * A.rebote(e), centro=True)
        return A.entra_final(im, final, t, t_final)

    marcas = [0.0, 2.6, DUR_PAR + 0.8, DUR_PAR + 3.0, 2 * DUR_PAR + 3.0, 3 * DUR_PAR - 0.5, t_final + 0.6, dur - 0.3]
    A.graba(fotograma, dur, salida, None, rev, marcas)


def publicar(v, ruta):
    A.publicar(ruta, f"Así no / Así sí · {A.limpio(v['es']['parejas'][0]['titulo'])}",
               {i: PIE[i] for i in ("es", "ca")},
               aviso="los negocios, teléfonos, precios y reseñas son de ejemplo (inventados).",
               nota="**Sin voz:** añade una música de la app (Instagram/TikTok) al subirlo.")
