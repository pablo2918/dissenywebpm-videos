"""Formato «Mito o verdad» (sin voz). Ver planes/plan_mito.py."""
from PIL import Image, ImageDraw

import anima as A
from plan_mito import PIE

UI = {"es": {"pregunta": "¿MITO O VERDAD?", "mito": "MITO", "verdad": "VERDAD",
             "es_mito": "ES UN MITO", "es_verdad": "ES VERDAD", "piensa": "¿Tú qué dices?"},
      "ca": {"pregunta": "MITE O VERITAT?", "mito": "MITE", "verdad": "VERITAT",
             "es_mito": "ÉS UN MITE", "es_verdad": "ÉS VERITAT", "piensa": "Tu què en dius?"}}

T_BOT = 1.0          # salen los botones y empieza la cuenta
T_RESP = 5.6         # la respuesta
T_FASE2 = 6.9        # empieza la explicacion


def boton(txt, color, lleno):
    w, h = 420, 150

    def dib(im, d):
        if lleno:
            d.rect((0, 0, w, h), fill=color, r=75)
            d.text((w / 2, h / 2 + 2), txt, A.C.f("Black", 64), A.BLANCO, anchor="mm")
        else:
            d.rect((3, 3, w - 3, h - 3), outline=color, r=72, width=7)
            d.text((w / 2, h / 2 + 2), txt, A.C.f("Black", 64), color, anchor="mm")
    return A.sprite(w, h, dib)


def sello(txt, color):
    ft = A.C.f("Black", 190)
    tw = A.C.D(Image.new("RGBA", (10, 10))).tl(txt, ft)
    w, h = tw + 120, 270

    def dib(im, d):
        d.rect((0, 0, w, h), fill=A.BLANCO, r=40)
        d.rect((14, 14, w - 14, h - 14), fill=color, r=30)
        d.text((w / 2, h / 2 + 6), txt, ft, A.BLANCO, anchor="mm")
    return A.sprite(w, h, dib).rotate(7, resample=Image.BICUBIC, expand=True)


def tarjeta(txt, n):
    w = 920
    ft = A.F("Bold", 54)
    lin = A.envuelve(txt, ft, w - 140 - 44)
    h = 64 + 66 * len(lin)

    def dib(im, d):
        d.rect((0, 0, w, h), fill=A.BLANCO, r=30)
        d.ellipse((34, h / 2 - 34, 102, h / 2 + 34), fill=A.AMARILLO)
        d.text((68, h / 2 + 1), str(n), A.C.f("Black", 36), A.AZUL, anchor="mm")
        y = h / 2 - 66 * len(lin) / 2
        for l in lin:
            d.text((140, y + 33), l, A.C.f("Bold", 54), A.AZUL, anchor="lm")
            y += 66
    return A.sprite(w, h, dib)


def hacer(v, idi, salida, rev, tmp):
    u, c = UI[idi], v[idi]
    color = A.VERDE if v["verdad"] else A.ROJO
    p_preg = A.pastilla(u["pregunta"], 40)
    p_resp = A.pastilla(u["es_verdad"] if v["verdad"] else u["es_mito"], 40, fondo=color, color=A.BLANCO)
    frase = A.titulo(f"«{c['frase']}»", 920, 620, 120, 66, centrado=True, max_lineas=5, mayus=False)
    b_mito = (boton(u["mito"], A.ROJO, False), boton(u["mito"], A.ROJO, True))
    b_ver = (boton(u["verdad"], A.VERDE, False), boton(u["verdad"], A.VERDE, True))
    st = sello("¡" + (u["verdad"] if v["verdad"] else u["mito"]) + "!" if idi == "es"
               else (u["verdad"] if v["verdad"] else u["mito"]) + "!", color)
    cards = [tarjeta(t, i + 1) for i, t in enumerate(c["puntos"])]
    # tiempo de lectura de cada tarjeta segun sus palabras
    t_card, t = [], T_FASE2 + 0.25
    for txt in c["puntos"]:
        t_card.append(t)
        t += max(2.4, 0.9 + 0.30 * len(txt.split()))
    t_final = t + 0.6
    dur = t_final + 3.2
    final = A.tarjeta_final(idi, c["final"])
    fondo = Image.new("RGB", (A.W, A.H), A.AZUL)

    # fase 1: pastilla, frase grande, botones; fase 2: todo centrado en pantalla
    y_pas, y_frase = 330, 470
    k2 = 0.5
    total = p_resp.height + 40 + frase.height * k2 + 60 + sum(cd.height for cd in cards) + 34 * (len(cards) - 1)
    y_pas2 = max(180, (180 + 1540 - total) / 2)
    y_frase2 = y_pas2 + p_resp.height + 40
    y_cards = y_frase2 + frase.height * k2 + 60

    def fotograma(t):
        im = fondo.copy()
        d = ImageDraw.Draw(im)
        f2 = A.eo(A.tramo(t, T_FASE2, 0.45))           # paso a la explicacion
        # pastilla de arriba: pregunta -> respuesta
        if f2 < 1:
            A.pega(im, p_preg, (A.W - p_preg.width) / 2, y_pas + (y_pas2 - y_pas) * f2, a=1 - f2)
        if f2 > 0:
            A.pega(im, p_resp, (A.W - p_resp.width) / 2, y_pas + (y_pas2 - y_pas) * f2, a=f2)
        # la frase: grande; despues pequena y arriba
        k = 1 + (k2 - 1) * f2
        x = (A.W - frase.width * k) / 2
        y = y_frase + (y_frase2 - y_frase) * f2
        A.pega(im, frase, x, y, a=1 - 0.35 * f2, k=k)
        # botones y cuenta atras
        if f2 < 1:
            a_b = A.eo(A.tramo(t, T_BOT, 0.35)) * (1 - f2)
            r = A.tramo(t, T_RESP, 0.25)
            for i, (b, gana) in enumerate(((b_mito, not v["verdad"]), (b_ver, v["verdad"]))):
                bx = A.W / 2 - 450 + i * 480
                by = 1290 + 40 * (1 - A.eo(A.tramo(t, T_BOT, 0.35)))
                if r > 0 and gana:
                    k_b = 1 + 0.12 * A.rebote(r)
                    A.pega(im, b[1], bx, by, a=a_b, k=k_b, centro=True)
                else:
                    A.pega(im, b[0], bx, by, a=a_b * (1 - 0.8 * r))
            if t < T_RESP:
                ft = A.F("Bold", 46)
                d.text((A.W / 2, 1200), u["piensa"], font=ft, fill=A.GRIS_CLARO, anchor="mm")
                q = 1 - A.tramo(t, T_BOT, T_RESP - T_BOT)
                if t >= T_BOT:
                    d.rounded_rectangle((140, 1490, 940, 1506), 8, fill=(40, 50, 78))
                    if q > 0.01:
                        d.rounded_rectangle((140, 1490, 140 + 800 * q, 1506), 8, fill=A.AMARILLO)
        # sello grande
        if T_RESP <= t < T_FASE2 + 0.3:
            ks = 1.6 - 0.6 * A.rebote(A.tramo(t, T_RESP, 0.35))
            a_s = A.tramo(t, T_RESP, 0.12) * (1 - A.tramo(t, T_FASE2, 0.3))
            A.pega(im, st, (A.W - st.width) / 2, y_frase + frase.height / 2 - st.height / 2, a=a_s, k=ks, centro=True)
        # tarjetas de la explicacion
        y = y_cards
        for cd, tc in zip(cards, t_card):
            e = A.eo(A.tramo(t, tc, 0.4))
            A.pega(im, cd, (A.W - cd.width) / 2, y + 50 * (1 - e), a=e)
            y += cd.height + 34
        return A.entra_final(im, final, t, t_final)

    marcas = [0.0, 2.0, T_RESP + 0.5, T_FASE2 + 0.6, t_card[1] + 0.6, t_card[-1] + 0.8, t_final - 0.1, dur - 0.5]
    A.graba(fotograma, dur, salida, None, rev, marcas)


def publicar(v, ruta):
    from plan_mito import VIDEOS  # noqa: F401
    A.publicar(ruta, f"Mito o verdad · {v['es']['frase']}",
               {i: PIE[i] for i in ("es", "ca")},
               nota="**Sin voz:** añade una música de la app (Instagram/TikTok) al subirlo.\n"
                    f"**Respuesta:** {'VERDAD' if v['verdad'] else 'MITO'}.")
