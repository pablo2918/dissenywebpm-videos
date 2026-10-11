"""Formato «Una web montándose sola» (con voz). Ver planes/plan_montaje.py."""
from PIL import Image, ImageDraw

import anima as A
from plan_montaje import PIE

C = A.C
PWM, PHM = 600, 1090              # movil
Y_MOVIL = 150
SW = PWM - 28                     # ancho de pantalla
PAD = 28
CW = SW - 2 * PAD                 # ancho del contenido
BARRA = 96                        # barra de direccion


def _alto_texto(txt, peso, tam, ancho, paso):
    d = C.D(Image.new("RGBA", (10, 10)))
    return len(C.parte(txt, C.f(peso, tam), ancho, d)) * paso


def p_portada(m, ctx):
    lt = _alto_texto(m["titulo"], "ExtraBold", 46, CW, 54)
    ls = _alto_texto(m["sub"], "Medium", 27, CW, 36)
    h = 70 + 250 + 26 + lt + 12 + ls + 10

    def dib(im, d):
        d.text((PAD, 30), ctx["negocio"], C.f("ExtraBold", 27), C.AZUL, anchor="lm")
        for k in range(3):
            d.rect((SW - PAD - 36, 18 + k * 11, SW - PAD, 22 + k * 11), fill=C.AZUL, r=2)
        C.pega_foto(im, (PAD, 70), CW, 250, m.get("foto", 0), 18)
        y = 70 + 250 + 26
        for l in C.parte(m["titulo"], C.f("ExtraBold", 46), CW, d):
            d.text((PAD, y), l, C.f("ExtraBold", 46), C.AZUL)
            y += 54
        y += 12
        for l in C.parte(m["sub"], C.f("Medium", 27), CW, d):
            d.text((PAD, y), l, C.f("Medium", 27), C.GRIS)
            y += 36
    return A.sprite(SW, h, dib)


def p_boton(m, ctx):
    def dib(im, d):
        d.rect((PAD, 8, SW - PAD, 100), fill=C.VERDE, r=46)
        C.icono_whatsapp(d, PAD + 52, 54, 22, fondo=(30, 140, 78))
        tam = 31
        while d.tl(m["texto"], C.f("Bold", tam)) > CW - 120 and tam > 20:
            tam -= 1
        d.text((PAD + 88, 54), m["texto"], C.f("Bold", tam), C.BLANCO, anchor="lm")
    return A.sprite(SW, 108, dib)


def p_lista(m, ctx):
    h = 64 + 66 * len(m["filas"])

    def dib(im, d):
        d.text((PAD, 24), m["titulo"], C.f("Bold", 34), C.AZUL, anchor="lm")
        y = 64
        for i, (et, val) in enumerate(m["filas"]):
            cy = y + 33
            fe, fv = C.cabe_fila(d, et, val, "SemiBold", "Bold", 28, 28, CW)
            d.text((PAD, cy), et, fe, C.AZUL, anchor="lm")
            if val:
                d.text((SW - PAD, cy), val, fv, C.AZUL, anchor="rm")
            else:
                d.ellipse((SW - PAD - 30, cy - 15, SW - PAD, cy + 15), fill=C.AMARILLO)
                d.line((SW - PAD - 23, cy, SW - PAD - 17, cy + 7, SW - PAD - 7, cy - 6), fill=C.AZUL, width=4)
            if i < len(m["filas"]) - 1:
                d.line((PAD, y + 66, SW - PAD, y + 66), C.LINEA, 2)
            y += 66
    return A.sprite(SW, h, dib)


def p_fotos(m, ctx):
    fw, fh, g = (CW - 16) / 2, 170, 16
    h = 64 + 2 * fh + g

    def dib(im, d):
        d.text((PAD, 24), m["titulo"], C.f("Bold", 34), C.AZUL, anchor="lm")
        for k in range(4):
            x = PAD + (k % 2) * (fw + g)
            y = 64 + (k // 2) * (fh + g)
            C.pega_foto(im, (x, y), fw, fh, k + 1, 16)
            et = m["etiquetas"][k]
            ft = C.f("Bold", 20)
            tw = d.tl(et, ft)
            d.rect((x + 10, y + fh - 44, x + 30 + tw, y + fh - 10), fill=C.BLANCO, r=17)
            d.text((x + 20, y + fh - 27), et, ft, C.AZUL, anchor="lm")
    return A.sprite(SW, h, dib)


def p_donde(m, ctx):
    mh = 180
    h = 64 + mh + 24 + 44 + 40 * len(m["horas"])

    def dib(im, d):
        d.text((PAD, 24), m["titulo"], C.f("Bold", 34), C.AZUL, anchor="lm")
        y0 = 64
        d.rect((PAD, y0, SW - PAD, y0 + mh), fill=(233, 240, 228), r=18)
        d.rect((PAD + 300, y0, PAD + 380, y0 + mh), fill=(214, 230, 245))
        for xy in ((PAD, y0 + 70, SW - PAD, y0 + 95), (PAD + 120, y0, PAD + 200, y0 + mh)):
            d.line(xy, C.BLANCO, 10)
        px, py = SW / 2, y0 + mh / 2 + 10
        d.ellipse((px - 22, py - 52, px + 22, py - 8), fill=C.ROJO)
        d.poly([(px - 16, py - 20), (px + 16, py - 20), (px, py + 4)], fill=C.ROJO)
        d.ellipse((px - 9, py - 39, px + 9, py - 21), fill=C.BLANCO)
        y = y0 + mh + 24
        d.text((PAD, y + 20), m["direccion"], C.f("SemiBold", 26), C.AZUL, anchor="lm")
        y += 44
        for hr in m["horas"]:
            d.text((PAD, y + 18), hr, C.f("Medium", 25), C.GRIS, anchor="lm")
            y += 40
    return A.sprite(SW, h, dib)


def p_resenas(m, ctx):
    lt = _alto_texto("«" + m["texto"] + "»", "Medium", 27, CW - 48, 36)
    h = 64 + 74 + 20 + lt + 40 + 40

    def dib(im, d):
        d.text((PAD, 24), m["titulo"], C.f("Bold", 34), C.AZUL, anchor="lm")
        d.text((PAD, 64 + 37), m["nota"], C.f("ExtraBold", 58), C.AZUL, anchor="lm")
        C.estrellas(d, PAD + d.tl(m["nota"], C.f("ExtraBold", 58)) + 18, 64 + 22, 5, 30)
        y = 64 + 74 + 20
        d.rect((PAD, y - 6, SW - PAD, y + lt + 66), fill=C.FONDO_FILA, r=18)
        yy = y + 14
        for l in C.parte("«" + m["texto"] + "»", C.f("Medium", 27), CW - 48, d):
            d.text((PAD + 24, yy), l, C.f("Medium", 27), (60, 66, 80))
            yy += 36
        d.text((PAD + 24, yy + 22), "— " + m["nombre"], C.f("Bold", 24), C.AZUL, anchor="lm")
    return A.sprite(SW, h, dib)


def p_zonas(m, ctx):
    d0 = C.D(Image.new("RGBA", (10, 10)))
    ft = C.f("SemiBold", 28)
    filas, cx = 1, 0
    for z in m["zonas"]:
        tw = d0.tl(z, ft) + 44
        if cx and cx + tw > CW:
            filas += 1
            cx = 0
        cx += tw + 12
    h = 64 + filas * 70

    def dib(im, d):
        d.text((PAD, 24), m["titulo"], C.f("Bold", 34), C.AZUL, anchor="lm")
        x, y = PAD, 64
        for z in m["zonas"]:
            tw = d.tl(z, ft) + 44
            if x > PAD and x + tw > SW - PAD:
                x = PAD
                y += 70
            d.rect((x, y, x + tw, y + 56), fill=C.FONDO_FILA, outline=C.LINEA, r=28, width=2)
            d.text((x + tw / 2, y + 28), z, ft, C.AZUL, anchor="mm")
            x += tw + 12
    return A.sprite(SW, h, dib)


PIEZAS = {"portada": p_portada, "boton": p_boton, "lista": p_lista, "fotos": p_fotos,
          "donde": p_donde, "resenas": p_resenas, "zonas": p_zonas}


def barra(dominio, alto):
    def dib(im, d):
        d.rect((0, 0, SW, alto), fill=C.BLANCO)
        d.rect((PAD, 50, SW - PAD, 88), fill=C.FONDO_FILA, r=19)
        d.text((PAD + 22, 69), dominio, C.f("Medium", 20), C.GRIS, anchor="lm")
        d.line((0, alto - 1, SW, alto - 1), C.LINEA, 2)
    return A.sprite(SW, alto, dib)


def hacer(v, idi, salida, rev, tmp):
    c = v[idi]
    ctx = {"negocio": c["negocio"], "dominio": c["dominio"]}
    tramos = [c["gancho"]] + [p[1] for p in c["pasos"]] + [c["cierre"]]
    vz = A.voz(salida.parent.name + "_" + v["id"], idi, tramos, tmp)
    n = len(c["pasos"])
    subs = A.Subtitulos(vz["palabras"], quitar=(0, len(tramos) - 1))
    marco, mascara, caja = A.movil(PWM, PHM)
    sh = caja[3] - caja[1]
    piezas = [PIEZAS[p[2]["tipo"]](p[2], ctx) for p in c["pasos"]]
    ys, y = [], BARRA + 20
    for pz in piezas:
        ys.append(y)
        y += pz.height + 30
    visible = sh - BARRA
    scroll = [max(0, ys[i] + piezas[i].height + 40 - sh) for i in range(n)]
    etiquetas = [A.pastilla(f"{i + 1}/{n} · {p[0].upper()}", 34) for i, p in enumerate(c["pasos"])]
    br = barra(c["dominio"], BARRA)
    tit = A.titulo(c["titulo"], 920, 520, 116, 64, max_lineas=4, centrado=True)
    ini = [vz["tramos"][i + 1]["inicio"] for i in range(n)]
    t_sube = ini[0] - 0.55
    t_final = vz["tramos"][-1]["inicio"] - 0.15
    dur = vz["duracion"] + 1.4
    final = A.tarjeta_final(idi, c["final"])
    fondo = Image.new("RGB", (A.W, A.H), A.AZUL)
    x_m = (A.W - PWM) / 2
    y_m0 = 150 + tit.height + 90           # en el gancho el movil asoma por abajo
    y_t0 = 150

    def pantalla(t):
        scr = Image.new("RGB", (SW, sh), C.BLANCO)
        # pagina vacia: esqueleto gris que late hasta que sale la primera pieza
        a = 1 - A.tramo(t, ini[0] - 0.2, 0.3)
        if a > 0:
            dd = ImageDraw.Draw(scr)
            g = int(236 - 10 * abs((t * 1.4) % 2 - 1))
            col = tuple(int(255 - (255 - g) * a) for _ in range(3))
            y = BARRA + 30
            for w_, h_ in ((0.45, 34), (1, 250), (0.9, 46), (0.7, 46), (0.8, 26), (1, 92), (0.5, 34), (1, 40), (1, 40)):
                dd.rounded_rectangle((PAD, y, PAD + CW * w_, y + h_), 14, fill=col)
                y += h_ + 24
        # desplazamiento: el de la ultima pieza que ha salido
        sc = 0.0
        for i in range(n):
            e = A.eo(A.tramo(t, ini[i] - 0.15, 0.6))
            sc = sc + (scroll[i] - sc) * e
        for i, pz in enumerate(piezas):
            e = A.eo(A.tramo(t, ini[i], 0.45))
            if e <= 0:
                continue
            A.pega(scr, pz, 0, ys[i] - sc + 50 * (1 - e), a=e)
        # pieza actual marcada en amarillo
        act = max((i for i in range(n) if t >= ini[i]), default=-1)
        if act >= 0 and t < t_final:
            a = A.tramo(t, ini[act] + 0.3, 0.3)
            if a > 0:
                y0 = ys[act] - sc - 10
                ImageDraw.Draw(scr).rounded_rectangle((8, y0, SW - 8, y0 + piezas[act].height + 20), 22,
                                                      outline=C.AMARILLO, width=7)
        scr.paste(br, (0, 0), br)
        return scr

    def fotograma(t):
        im = fondo.copy()
        s = A.eo(A.tramo(t, t_sube, 0.55))
        A.pega(im, tit, (A.W - tit.width) / 2, y_t0 - 200 * s, a=1 - s)
        ym = y_m0 + (Y_MOVIL - y_m0) * s
        im.paste(pantalla(t), (int(x_m + caja[0]), int(ym + caja[1])), mascara)
        A.pega(im, marco, x_m, ym)
        act = max((i for i in range(n) if t >= ini[i] - 0.1), default=-1)
        if act >= 0:
            e = A.tramo(t, ini[act] - 0.1, 0.3)
            et = etiquetas[act]
            A.pega(im, et, (A.W - et.width) / 2, Y_MOVIL + PHM - et.height / 2 - 20, k=A.rebote(e), centro=True)
        subs.pinta(im, t)
        return A.entra_final(im, final, t, t_final)

    marcas = [0.0, t_sube - 0.3] + [x + 1.4 for x in ini] + [dur - 0.4]
    A.graba(fotograma, dur, salida, vz["wav"], rev, marcas[:8])


def publicar(v, ruta):
    A.publicar(ruta, f"Una web montándose · {v['es']['negocio']}",
               {i: PIE[i] for i in ("es", "ca")},
               aviso="el negocio, los precios, horarios y reseñas son de ejemplo (inventados).")
