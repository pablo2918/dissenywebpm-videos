"""Formato «Plantilla para copiar» (con voz). Ver planes/plan_plantilla.py."""
import re

from PIL import Image, ImageDraw

import anima as A
from plan_plantilla import PIE

C = A.C
UI = {"es": {"pas": "PLANTILLA PARA COPIAR", "cab": "Texto para copiar", "leyenda": "En amarillo: cámbialo por lo tuyo",
             "captura": "HAZ CAPTURA"},
      "ca": {"pas": "PLANTILLA PER COPIAR", "cab": "Text per copiar", "leyenda": "En groc: canvia-ho pel teu",
             "captura": "FES CAPTURA"}}
CW = 940                          # ancho de la tarjeta
PAD = 54


def tokens(p):
    """[(palabra, parte_ejemplo)] a partir de «Hola, {Marta}.»: la parte de
    ejemplo es lo que va dentro de las llaves (sin la puntuacion de fuera)."""
    out, dentro = [], False
    for w in p.split():
        if w.startswith("{"):
            dentro = True
            w = w[1:]
        if dentro and "}" in w:
            ej, resto = w.split("}", 1)
            out.append((ej + resto, ej))
            dentro = False
        else:
            out.append((w, w if dentro else ""))
    return out


def maqueta(parrafos, ft, ancho, d):
    """Lineas de cada parrafo: [[ [(palabra, ejemplo), ...], ...], ...]"""
    res = []
    for p in parrafos:
        lin, cur = [], []
        for w, ej in tokens(p):
            prueba = " ".join(x for x, _ in cur + [(w, ej)])
            if cur and d.textlength(prueba, font=ft) > ancho:
                lin.append(cur)
                cur = []
            cur.append((w, ej))
        lin.append(cur)
        res.append(lin)
    return res


def tarjeta(parrafos, u, activo, alto_max):
    """Tarjeta con la plantilla. `activo`: parrafo que se esta leyendo
    (los anteriores en azul, los siguientes en gris; -1 = todos en azul)."""
    d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for tam in range(54, 37, -2):
        ft = A.F("Medium", tam)
        paso = int(tam * 1.32)
        lay = maqueta(parrafos, ft, CW - 2 * PAD - 20, d0)
        alto = 96 + 40 + sum(len(l) * paso for l in lay) + 30 * (len(lay) - 1) + 40 + 60
        if alto <= alto_max:
            break
    im = Image.new("RGBA", (CW, int(alto)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, CW - 1, alto - 1), 34, fill=C.BLANCO)
    d.rounded_rectangle((0, 0, CW - 1, 96), 34, fill=C.FONDO_FILA)
    d.rectangle((0, 60, CW - 1, 96), fill=C.FONDO_FILA)
    # icono de copiar: dos hojas
    d.rounded_rectangle((PAD, 30, PAD + 26, 62), 5, outline=C.GRIS, width=4)
    d.rounded_rectangle((PAD + 10, 22, PAD + 36, 54), 5, fill=C.FONDO_FILA, outline=C.GRIS, width=4)
    d.text((PAD + 56, 48), u["cab"], font=A.F("SemiBold", 32), fill=C.GRIS, anchor="lm")
    y = 96 + 40
    esp = d.textlength(" ", font=ft)
    for i, lin in enumerate(lay):
        color = C.AZUL if (activo < 0 or i <= activo) else (190, 195, 205)
        y0 = y
        for l in lin:
            x = PAD + 20
            base = y + ft.getmetrics()[0] + (paso - tam) / 2
            # fondo amarillo de los ejemplos (palabras seguidas, un solo trozo)
            trozos, cx = [], x
            for w, ej in l:
                wl = d.textlength(w, font=ft)
                if ej:
                    we = d.textlength(ej, font=ft)
                    if trozos and trozos[-1][1] >= cx - esp - 1:
                        trozos[-1][1] = cx + we
                    else:
                        trozos.append([cx, cx + we])
                cx += wl + esp
            for a, b in trozos:
                fondo = C.AMARILLO if (activo < 0 or i <= activo) else (250, 236, 190)
                d.rounded_rectangle((a - 8, y + paso * 0.1, b + 8, y + paso * 0.92), 10, fill=fondo)
            for w, ej in l:
                d.text((x, base), w, font=ft, fill=color, anchor="ls")
                x += d.textlength(w, font=ft) + esp
            y += paso
        if i == activo:
            d.rounded_rectangle((PAD - 16, y0 + 6, PAD - 6, y - 6), 5, fill=C.AMARILLO)
        y += 30
    y += 10
    d.text((PAD, y + 26), u["leyenda"], font=A.F("SemiBold", 28), fill=C.GRIS, anchor="lm")
    d.rounded_rectangle((PAD + d.textlength(u["leyenda"], font=A.F("SemiBold", 28)) + 16, y + 10,
                         PAD + d.textlength(u["leyenda"], font=A.F("SemiBold", 28)) + 56, y + 42), 8, fill=C.AMARILLO)
    return im


def hacer(v, idi, salida, rev, tmp):
    c, u = v[idi], UI[idi]
    pant = [p if isinstance(p, str) else p[0] for p in c["parrafos"]]
    vozp = [re.sub(r"[{}]", "", p) if isinstance(p, str) else p[1] for p in c["parrafos"]]
    tramos = [c["gancho"]] + vozp + [c["consejo"]]
    vz = A.voz(salida.parent.name + "_" + v["id"], idi, tramos, tmp)
    np_ = len(pant)
    pas = A.pastilla(u["pas"], 34)
    tit = A.titulo(c["titulo"], 900, 620, 112, 64, max_lineas=5, centrado=True, mayus=False)
    K_T = 0.5
    y_t2 = 150 + pas.height + 26
    top_card = y_t2 + tit.height * K_T + 40
    cap = A.pastilla(u["captura"], 44, fondo=C.AMARILLO)
    alto_max = 1500 - top_card - cap.height - 40
    estados = [tarjeta(pant, u, i, alto_max) for i in range(np_)] + [tarjeta(pant, u, -1, alto_max)]
    card_h = estados[0].height
    y_cap = top_card + card_h + 36
    t_sube = vz["tramos"][1]["inicio"] - 0.5
    t_cons = vz["tramos"][-1]["inicio"]
    t_final = vz["tramos"][-1]["fin"] + 0.3
    dur = t_final + 2.8
    final = A.tarjeta_final(idi, c["final"])
    fondo = Image.new("RGB", (A.W, A.H), A.AZUL)
    y_pas1 = (A.H - 430 - tit.height - pas.height - 40) / 2 + 30
    y_t1 = y_pas1 + pas.height + 40

    def fotograma(t):
        im = fondo.copy()
        s = A.eo(A.tramo(t, t_sube, 0.5))
        A.pega(im, pas, (A.W - pas.width) / 2, y_pas1 + (150 - y_pas1) * s)
        k = 1 + (K_T - 1) * s
        A.pega(im, tit, (A.W - tit.width * k) / 2, y_t1 + (y_t2 - y_t1) * s, k=k)
        if t >= t_sube:
            # parrafo que se esta leyendo
            act = -1 if t >= t_cons else max(0, max(i for i in range(np_) if vz["tramos"][i + 1]["inicio"] - 0.1 <= t)
                                            if any(vz["tramos"][i + 1]["inicio"] - 0.1 <= t for i in range(np_)) else 0)
            card = estados[act]
            e = A.eo(A.tramo(t, t_sube + 0.15, 0.45))
            A.pega(im, card, (A.W - CW) / 2, top_card + 120 * (1 - e), a=e)
        if t >= t_cons:
            e = A.tramo(t, t_cons, 0.35)
            puls = 1 + 0.04 * abs(((t - t_cons) * 1.6) % 2 - 1) if e >= 1 else A.rebote(e)
            A.pega(im, cap, (A.W - cap.width) / 2, y_cap, k=puls, centro=True)
        return A.entra_final(im, final, t, t_final)

    ts = [x["inicio"] for x in vz["tramos"]]
    marcas = [0.0, ts[0] + 1.2] + [x + 1.2 for x in ts[1:]] + [t_final + 1.0]
    A.graba(fotograma, dur, salida, vz["wav"], rev, marcas[:8])


def publicar(v, ruta):
    A.publicar(ruta, f"Plantilla para copiar · {A.limpio(v['es']['titulo'])}",
               {i: PIE[i] for i in ("es", "ca")},
               aviso="los nombres y datos en amarillo son ejemplos para cambiar.")
