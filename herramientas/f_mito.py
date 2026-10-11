"""Formato «Mito o verdad» (sin voz), 3 preguntas por video.
Ver planes/plan_mito.py."""
from PIL import Image, ImageDraw

import anima as A
from plan_mito import PIE

UI = {"es": {"pregunta": "¿MITO O VERDAD?", "mito": "MITO", "verdad": "VERDAD",
             "es_mito": "ES UN MITO", "es_verdad": "ES VERDAD", "piensa": "¿Tú qué dices?",
             "sello_m": "¡MITO!", "sello_v": "¡VERDAD!"},
      "ca": {"pregunta": "MITE O VERITAT?", "mito": "MITE", "verdad": "VERITAT",
             "es_mito": "ÉS UN MITE", "es_verdad": "ÉS VERITAT", "piensa": "Tu què en dius?",
             "sello_m": "MITE!", "sello_v": "VERITAT!"}}

# tiempos dentro de cada pregunta
T_BOT = 0.7          # salen los botones y empieza la cuenta
T_RESP = 3.9         # la respuesta
T_PORQUE = 4.8       # la linea del porque
DUR_P = 7.6          # lo que dura cada pregunta
SALE = 0.35          # transicion a la siguiente
Y_PAS, Y_FRASE, Y_BOT = 300, 440, 1290


def boton(txt, color, lleno):
    w, h = 420, 150

    def dib(im, d):
        if lleno:
            d.rect((0, 0, w, h), fill=color, r=75)
            d.text((w / 2, h / 2 + 2), txt, A.C.f("Black", 62), A.BLANCO, anchor="mm")
        else:
            d.rect((3, 3, w - 3, h - 3), outline=color, r=72, width=7)
            d.text((w / 2, h / 2 + 2), txt, A.C.f("Black", 62), color, anchor="mm")
    return A.sprite(w, h, dib)


def sello(txt, color):
    ft = A.C.f("Black", 170)
    tw = A.C.D(Image.new("RGBA", (10, 10))).tl(txt, ft)
    w, h = tw + 110, 250

    def dib(im, d):
        d.rect((0, 0, w, h), fill=A.BLANCO, r=40)
        d.rect((14, 14, w - 14, h - 14), fill=color, r=30)
        d.text((w / 2, h / 2 + 6), txt, ft, A.BLANCO, anchor="mm")
    sp = A.sprite(w, h, dib).rotate(7, resample=Image.BICUBIC, expand=True)
    if sp.width > 1000:
        sp = sp.resize((1000, int(sp.height * 1000 / sp.width)), Image.LANCZOS)
    return sp


def porque(txt, color):
    """La explicacion: una sola tarjeta, letra grande, con un filete del color de la respuesta."""
    w = 940
    ft = A.F("ExtraBold", 62)
    lin = A.envuelve(txt, ft, w - 110)
    h = 70 + 78 * len(lin)

    def dib(im, d):
        d.rect((0, 0, w, h), fill=A.BLANCO, r=34)
        d.rect((0, 0, 18, h), fill=color, r=9)
        y = h / 2 - 78 * len(lin) / 2
        for l in lin:
            d.text((w / 2 + 6, y + 39), l, A.C.f("ExtraBold", 62), A.AZUL, anchor="mm")
            y += 78
    return A.sprite(w, h, dib)


def hacer(v, idi, salida, rev, tmp):
    u = UI[idi]
    n = len(v["preguntas"])
    bot = {"m": (boton(u["mito"], A.ROJO, False), boton(u["mito"], A.ROJO, True)),
           "v": (boton(u["verdad"], A.VERDE, False), boton(u["verdad"], A.VERDE, True))}
    ps = []
    for i, (verdad, txt) in enumerate(v["preguntas"]):
        frase, pq = txt[idi]
        color = A.VERDE if verdad else A.ROJO
        ps.append({
            "verdad": verdad,
            "pre": A.pastilla(f"{i + 1}/{n} · {u['pregunta']}", 38),
            "resp": A.pastilla(f"{i + 1}/{n} · " + (u["es_verdad"] if verdad else u["es_mito"]), 38,
                               fondo=color, color=A.BLANCO),
            "frase": A.titulo(f"«{frase}»", 920, 640, 116, 64, centrado=True, max_lineas=5, mayus=False),
            "sello": sello(u["sello_v"] if verdad else u["sello_m"], color),
            "porque": porque(pq, color)})
    t_final = n * DUR_P
    dur = t_final + 3.2
    final = A.tarjeta_final(idi, v["final"][idi])
    fondo = Image.new("RGB", (A.W, A.H), A.AZUL)

    def fotograma(t):
        im = fondo.copy()
        i = min(n - 1, int(t // DUR_P))
        p, tl = ps[i], t - i * DUR_P
        # entra desde la derecha (salvo la primera: ya esta en el fotograma 0) y sale por la izquierda
        ent = 1 if i == 0 else A.eo(A.tramo(tl, 0, SALE))
        sal = A.eo(A.tramo(tl, DUR_P - SALE, SALE)) if i < n - 1 else 0
        dx = 1100 * (1 - ent) - 1100 * sal
        a = min(ent, 1 - sal)
        r = A.tramo(tl, T_RESP, 0.25)
        # pastilla: pregunta -> respuesta
        if r < 1:
            A.pega(im, p["pre"], (A.W - p["pre"].width) / 2 + dx, Y_PAS, a=a * (1 - r))
        if r > 0:
            A.pega(im, p["resp"], (A.W - p["resp"].width) / 2 + dx, Y_PAS, a=a * r)
        fr = p["frase"]
        y_fr = Y_FRASE + (640 - fr.height) / 2
        A.pega(im, fr, (A.W - fr.width) / 2 + dx, y_fr, a=a * (1 - 0.35 * A.tramo(tl, T_PORQUE, 0.3)))
        # botones y cuenta atras (hasta que sale el porque)
        f2 = A.eo(A.tramo(tl, T_PORQUE - 0.15, 0.3))
        if f2 < 1:
            a_b = A.eo(A.tramo(tl, T_BOT, 0.3)) * (1 - f2) * a
            for k, (clave, gana) in enumerate((("m", not p["verdad"]), ("v", p["verdad"]))):
                b = bot[clave]
                bx = A.W / 2 - 450 + k * 480 + dx
                by = Y_BOT + 40 * (1 - A.eo(A.tramo(tl, T_BOT, 0.3)))
                if r > 0 and gana:
                    A.pega(im, b[1], bx, by, a=a_b, k=1 + 0.12 * A.rebote(r), centro=True)
                else:
                    A.pega(im, b[0], bx, by, a=a_b * (1 - 0.8 * r))
            if tl < T_RESP:
                d = ImageDraw.Draw(im)
                d.text((A.W / 2 + dx, 1205), u["piensa"], font=A.F("Bold", 46), fill=A.GRIS_CLARO, anchor="mm")
                q = 1 - A.tramo(tl, T_BOT, T_RESP - T_BOT)
                if tl >= T_BOT:
                    d.rounded_rectangle((140 + dx, 1490, 940 + dx, 1506), 8, fill=(40, 50, 78))
                    if q > 0.01:
                        d.rounded_rectangle((140 + dx, 1490, 140 + dx + 800 * q, 1506), 8, fill=A.AMARILLO)
        # sello grande
        if T_RESP <= tl < T_PORQUE + 0.3:
            st = p["sello"]
            ks = 1.6 - 0.6 * A.rebote(A.tramo(tl, T_RESP, 0.35))
            a_s = A.tramo(tl, T_RESP, 0.12) * (1 - A.tramo(tl, T_PORQUE - 0.1, 0.3))
            A.pega(im, st, (A.W - st.width) / 2 + dx, y_fr + fr.height / 2 - st.height / 2, a=a_s * a, k=ks, centro=True)
        # el porque
        e = A.eo(A.tramo(tl, T_PORQUE, 0.4))
        if e > 0:
            pq = p["porque"]
            A.pega(im, pq, (A.W - pq.width) / 2 + dx, 1230 - pq.height / 2 + 50 * (1 - e) + 60, a=e * a)
        return A.entra_final(im, final, t, t_final)

    marcas = [0.0, T_RESP + 0.4, T_PORQUE + 1.0, DUR_P + 2.0, DUR_P + T_PORQUE + 1.0,
              2 * DUR_P + T_RESP + 0.4, 2 * DUR_P + T_PORQUE + 1.5, dur - 0.5]
    A.graba(fotograma, dur, salida, None, rev, marcas)


def publicar(v, ruta):
    resp = " · ".join(("VERDAD" if vv else "MITO") for vv, _ in v["preguntas"])
    A.publicar(ruta, f"Mito o verdad · {v['preguntas'][0][1]['es'][0]}",
               {i: PIE[i] for i in ("es", "ca")},
               nota="**Sin voz:** añade una música de la app (Instagram/TikTok) al subirlo.\n"
                    f"**Respuestas:** {resp}.")
