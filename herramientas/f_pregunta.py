"""Formato «Pregunta de cliente» (con voz). Ver planes/plan_pregunta.py."""
from PIL import Image

import anima as A
from plan_pregunta import PIE

C = A.C
UI = {"es": "ME PREGUNTAN", "ca": "EM PREGUNTEN"}
TOP_CARDS, BOT_CARDS = 640, 1225


def globo(txt):
    """Globo de WhatsApp (mensaje recibido) con la pregunta en grande."""
    # se dibuja grande (gancho) y luego se encoge hasta arriba
    ft = A.F("ExtraBold", 104)
    lin = A.envuelve(txt, ft, 820)
    w = max(A.ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(l, font=ft) for l in lin) + 120
    h = 84 + 122 * len(lin)

    def dib(im, d):
        d.poly([(0, 0), (60, 0), (60, 60)], fill=C.BLANCO)
        d.rect((34, 0, 34 + w, h), fill=C.BLANCO, r=50)
        y = 42
        for l in lin:
            d.text((34 + 60, y + 61), l, C.f("ExtraBold", 104), C.AZUL, anchor="lm")
            y += 122
    return A.sprite(w + 34, h, dib)


def tarjeta(txt):
    w = 900
    ft = A.F("Bold", 56)
    lin = A.envuelve(txt, ft, w - 170)
    h = 54 + 68 * len(lin)

    def dib(im, d):
        d.rect((0, 0, w, h), fill=(24, 34, 62), r=30)
        cy = h / 2
        d.ellipse((34, cy - 36, 106, cy + 36), fill=C.AMARILLO)
        d.line((52, cy + 2, 66, cy + 16, 90, cy - 12), fill=C.AZUL, width=8)
        y = cy - 68 * len(lin) / 2
        for l in lin:
            d.text((140, y + 34), l, C.f("Bold", 56), C.BLANCO, anchor="lm")
            y += 68
    return A.sprite(w, h, dib)


def hacer(v, idi, salida, rev, tmp):
    c = v[idi]
    tramos = [c["gancho"]] + [p[0] for p in c["puntos"]] + [c["cierre"]]
    vz = A.voz(salida.parent.name + "_" + v["id"], idi, tramos, tmp)
    n = len(tramos)
    subs = A.Subtitulos(vz["palabras"], quitar=(0, n - 1))
    pas = A.pastilla(UI[idi], 36)
    gl = globo(c["pregunta"])
    cards = [tarjeta(p[1]) for p in c["puntos"]]
    alto = sum(cd.height for cd in cards)
    gap = min(34, (BOT_CARDS - TOP_CARDS - alto) / max(1, len(cards) - 1))
    k_cards = min(1.0, (BOT_CARDS - TOP_CARDS) / (alto + gap * (len(cards) - 1)))
    t_final = vz["tramos"][-1]["inicio"] - 0.15
    dur = vz["duracion"] + 1.4
    final = A.tarjeta_final(idi, c["final"])
    fondo = Image.new("RGB", (A.W, A.H), A.AZUL)
    y_gl = 150 + pas.height + 40
    K_GL = 0.62
    # si el globo es alto, las tarjetas empiezan mas abajo
    top = max(TOP_CARDS, y_gl + gl.height * K_GL + 50)
    t_sube = vz["tramos"][1]["inicio"] - 0.45
    # gancho: pastilla y globo grandes, centrados en la pantalla
    y_pas1 = (A.H - 430 - gl.height - pas.height - 50) / 2 + 40
    y_gl1 = y_pas1 + pas.height + 50

    def fotograma(t):
        im = fondo.copy()
        s_ = A.eo(A.tramo(t, t_sube, 0.5))
        x1 = (A.W - gl.width) / 2
        A.pega(im, pas, x1 + 34 + (104 - x1 - 34) * s_, y_pas1 + (150 - y_pas1) * s_)
        k = 1 + (K_GL - 1) * s_
        e = A.rebote(A.tramo(t, 0, 0.35))
        A.pega(im, gl, x1 + (70 - x1) * s_, y_gl1 + (y_gl - y_gl1) * s_, k=k * (0.96 + 0.04 * e))
        y = top
        for i, cd in enumerate(cards):
            t0 = vz["tramos"][i + 1]["inicio"]
            e = A.eo(A.tramo(t, t0 - 0.1, 0.4))
            A.pega(im, cd, (A.W - cd.width * k_cards) / 2 + 80 * (1 - e), y, a=e, k=k_cards)
            y += (cd.height + gap) * k_cards
        subs.pinta(im, t)
        return A.entra_final(im, final, t, t_final)

    ts = [x["inicio"] for x in vz["tramos"]]
    marcas = [0.0, ts[0] + 1.0] + [x + 1.0 for x in ts[1:-1]] + [ts[-1] - 0.4, dur - 0.3]
    A.graba(fotograma, dur, salida, vz["wav"], rev, marcas[:8])


def publicar(v, ruta):
    A.publicar(ruta, f"Pregunta de cliente · {v['es']['pregunta']}",
               {i: PIE[i] for i in ("es", "ca")})
