"""Formato «La búsqueda en directo» (con voz). Ver planes/plan_busqueda.py."""
import math

from PIL import Image, ImageDraw

import anima as A
from plan_busqueda import PIE

C = A.C
PWM, PHM = 600, 1090
Y_MOVIL = 150
SW = PWM - 28
PAD = 26
CW = SW - 2 * PAD
CAB = 150                          # cabecera fija con la caja de busqueda
FICHA_H = 252
MAPA_H = 200
AZUL_ENLACE = (26, 92, 200)
UI = {"es": {"llamar": "Llamar", "ruta": "Cómo llegar", "web": "Web", "tu": "TÚ", "sin_fotos": "Sin fotos",
             "abierto": ("Abierto",), "cerrado": ("Cerrado", "Sin")},
      "ca": {"llamar": "Trucar", "ruta": "Com arribar-hi", "web": "Web", "tu": "TU", "sin_fotos": "Sense fotos",
             "abierto": ("Obert",), "cerrado": ("Tancat", "Sense")}}


def ficha(f, u):
    """Sprite de una ficha y la caja de cada boton (en coordenadas de la ficha)."""
    nombre, nota, n, linea, botones, foto, tu = f
    botones_cajas = {}
    d0 = C.D(Image.new("RGBA", (10, 10)))
    ftb = C.f("Bold", 25)
    x = PAD
    for b in botones:
        w = d0.tl(u[b], ftb) + 44
        botones_cajas[b] = (x, 178, x + w, 232)
        x += w + 12

    def dib(im, d):
        ancho_txt = CW - (150 if foto else 0)
        tam = 36
        while d.tl(nombre, C.f("Bold", tam)) > ancho_txt - (78 if tu else 0) and tam > 24:
            tam -= 1
        fn = C.f("Bold", tam)
        d.text((PAD, 42), nombre, fn, AZUL_ENLACE, anchor="lm")
        if tu:
            xt = PAD + d.tl(nombre, fn) + 12
            ft = C.f("ExtraBold", 22)
            tw = d.tl(u["tu"], ft) + 26
            d.rect((xt, 25, xt + tw, 59), fill=C.AMARILLO, r=17)
            d.text((xt + tw / 2, 42), u["tu"], ft, C.AZUL, anchor="mm")
        fs = C.f("SemiBold", 28)
        d.text((PAD, 92), nota, fs, C.GRIS, anchor="lm")
        C.estrellas(d, PAD + d.tl(nota, fs) + 12, 80, 5, 24)
        d.text((PAD + d.tl(nota, fs) + 156, 92), f"({n})", C.f("Medium", 26), C.GRIS, anchor="lm")
        # tipo · estado (el estado, de color); si no cabe, solo el estado
        fl = C.f("Medium", 27)
        fe = C.f("SemiBold", 27)
        tipo, estado = linea.split(" · ", 1) if " · " in linea else ("", linea)
        if tipo and d.tl(tipo + " · ", fl) + d.tl(estado, fe) > ancho_txt:
            tipo = ""
        col = C.VERDE if estado.startswith(u["abierto"]) else (C.ROJO if estado.startswith(u["cerrado"]) else C.VERDE)
        while d.tl(estado, fe) > ancho_txt and fe.size > 18 * C.S:
            fe = C.f("SemiBold", fe.size / C.S - 1)
        x = PAD
        if tipo:
            d.text((x, 138), tipo + " · ", fl, C.GRIS, anchor="lm")
            x += d.tl(tipo + " · ", fl)
        d.text((x, 138), estado, fe, col, anchor="lm")
        for b, (x0, y0, x1, y1) in botones_cajas.items():
            d.rect((x0, y0, x1, y1), outline=C.LINEA, r=23, width=2)
            d.text(((x0 + x1) / 2, (y0 + y1) / 2), u[b], ftb, AZUL_ENLACE, anchor="mm")
        if foto is True:
            C.pega_foto(im, (SW - PAD - 134, 22), 134, 134, sum(map(ord, nombre)) % 6, 16)
        elif foto == "hueco":
            d.rect((SW - PAD - 134, 22, SW - PAD, 156), fill=(236, 238, 242), r=16)
            d.text((SW - PAD - 67, 89), u["sin_fotos"], C.f("SemiBold", 20), C.GRIS, anchor="mm")
        d.line((0, FICHA_H - 1, SW, FICHA_H - 1), C.LINEA, 2)
    return A.sprite(SW, FICHA_H, dib), botones_cajas


def mapa(n):
    def dib(im, d):
        d.rect((0, 0, SW, MAPA_H), fill=(233, 240, 228))
        d.rect((330, 0, 420, MAPA_H), fill=(214, 230, 245))
        for xy in ((0, 70, SW, 96), (130, 0, 210, MAPA_H), (440, 0, 500, MAPA_H)):
            d.line(xy, C.BLANCO, 10)
        pins = [(120, 60), (300, 130), (470, 70), (230, 150)]
        for i, (px, py) in enumerate(pins[:n]):
            d.ellipse((px - 20, py - 46, px + 20, py - 6), fill=C.ROJO)
            d.poly([(px - 14, py - 18), (px + 14, py - 18), (px, py + 4)], fill=C.ROJO)
            d.text((px, py - 26), str(i + 1), C.f("Bold", 18), C.BLANCO, anchor="mm")
        d.line((0, MAPA_H - 1, SW, MAPA_H - 1), C.LINEA, 2)
    return A.sprite(SW, MAPA_H, dib)


def cabecera():
    def dib(im, d):
        d.rect((0, 0, SW, CAB), fill=C.BLANCO)
        d.rect((PAD, 58, SW - PAD, 128), fill=C.BLANCO, outline=(210, 214, 222), r=35, width=3)
        cx, cy = PAD + 38, 92
        d.ellipse((cx - 13, cy - 13, cx + 9, cy + 9), outline=C.GRIS, width=4)
        d.line((cx + 6, cy + 6, cx + 16, cy + 16), C.GRIS, 5)
        d.line((0, CAB - 1, SW, CAB - 1), C.LINEA, 2)
    return A.sprite(SW, CAB, dib)


def etiqueta(txt, bien):
    return A.pastilla(txt, 30, fondo=C.VERDE if bien else C.ROJO, color=C.BLANCO)


def dedo():
    r = 38

    def dib(im, d):
        d.ellipse((4, 4, 2 * r + 4, 2 * r + 4), fill=(255, 255, 255, 170), outline=(120, 130, 150), width=4)
    return A.sprite(2 * r + 8, 2 * r + 8, dib)


def hacer(v, idi, salida, rev, tmp):
    c, u = v[idi], UI[idi]
    tramos = [c["gancho"]] + [p[0] for p in c["pasos"]] + [c["cierre"]]
    vz = A.voz(salida.parent.name + "_" + v["id"], idi, tramos, tmp)
    n = len(c["pasos"])
    subs = A.Subtitulos(vz["palabras"], quitar=(0, len(tramos) - 1))
    marco, mascara, caja = A.movil(PWM, PHM)
    sh = caja[3] - caja[1]
    fichas = [ficha(f, u) for f in c["fichas"]]
    bueno = ficha(c["bueno"], u)
    mp = mapa(len(fichas))
    cab = cabecera()
    dd = dedo()
    ini = [vz["tramos"][i + 1]["inicio"] for i in range(n)]
    fin = [vz["tramos"][i + 1]["fin"] for i in range(n)]
    acciones = [p[1] for p in c["pasos"]]
    i_tu = next((k for k, f in enumerate(c["fichas"]) if f[6]), None)
    # escritura: empieza con el tramo de «escribe» y dura lo que la frase
    i_esc = next(k for k, a in enumerate(acciones) if a[0] == "escribe")
    t_esc0 = ini[i_esc] + 0.2
    t_esc1 = min(fin[i_esc] - 0.2, t_esc0 + 0.075 * len(c["busca"]))
    t_res = t_esc1 + 0.25
    ys = [CAB + MAPA_H + k * FICHA_H for k in range(len(fichas))]
    alto_pag = CAB + MAPA_H + len(fichas) * FICHA_H + 260
    etis = {k: etiqueta(a[2] if a[0] == "senala" else a[1], a[3] if a[0] == "senala" else a[0] in ("arregla", "muestra"))
            for k, a in enumerate(acciones) if a[0] in ("senala", "baja", "arregla", "muestra")}
    tit = A.titulo(c["titulo"], 920, 520, 116, 64, max_lineas=4, centrado=True)
    t_sube = ini[0] - 0.55
    t_final = vz["tramos"][-1]["inicio"] - 0.15
    dur = vz["duracion"] + 1.4
    final = A.tarjeta_final(idi, c["final"])
    fondo = Image.new("RGB", (A.W, A.H), A.AZUL)
    x_m = (A.W - PWM) / 2
    y_m0 = 150 + tit.height + 90

    def activo(t):
        return max((k for k in range(n) if t >= ini[k] - 0.05), default=-1)

    def pantalla(t):
        scr = Image.new("RGB", (SW, sh), C.BLANCO)
        k = activo(t)
        # desplazamiento: «baja» lleva al final de la lista
        sc = 0.0
        for j, a in enumerate(acciones):
            if a[0] == "baja":
                sc = (alto_pag - sh) * A.eo(A.tramo(t, ini[j], 1.2))
        e = A.eo(A.tramo(t, t_res, 0.4))
        if e > 0:
            A.pega(scr, mp, 0, CAB - sc, a=e)
            for j, (sp, _) in enumerate(fichas):
                ej = A.eo(A.tramo(t, t_res + 0.08 * j, 0.4))
                spr = sp
                # tu ficha arreglada
                for q, a in enumerate(acciones):
                    if a[0] == "arregla" and j == i_tu and t >= ini[q]:
                        mezcla = A.tramo(t, ini[q] + 0.2, 0.4)
                        spr = Image.blend(sp, bueno[0], mezcla) if mezcla < 1 else bueno[0]
                A.pega(scr, spr, 0, ys[j] - sc + 40 * (1 - ej), a=ej)
            if any(a[0] == "baja" for a in acciones):
                d = ImageDraw.Draw(scr)
                yb = CAB + MAPA_H + len(fichas) * FICHA_H - sc + 50
                d.rounded_rectangle((PAD, yb, SW - PAD, yb + 60), 30, outline=C.LINEA, width=2)
                d.text((SW / 2, yb + 30), "Más resultados" if idi == "es" else "Més resultats",
                       font=A.F("SemiBold", 22), fill=AZUL_ENLACE, anchor="mm")
        # marca amarilla de la ficha que se senala
        if 0 <= k < n and t < t_final:
            a = acciones[k]
            j = a[1] if a[0] in ("senala", "toca") else (i_tu if a[0] == "arregla" else None)
            if j is not None:
                r = A.tramo(t, ini[k] + 0.15, 0.25)
                if r > 0:
                    y0 = ys[j] - sc + 6
                    col = C.VERDE if (a[0] == "arregla") else C.AMARILLO
                    # foco: lo demas se apaga un poco
                    velo = Image.new("RGBA", scr.size, (255, 255, 255, int(150 * r)))
                    ImageDraw.Draw(velo).rectangle((0, y0 - 6, SW, y0 + FICHA_H - 4), fill=(0, 0, 0, 0))
                    scr.paste(velo, (0, 0), velo)
                    ImageDraw.Draw(scr).rounded_rectangle((8, y0, SW - 8, y0 + FICHA_H - 10), 20, outline=col, width=7)
        # cabecera con lo que se va escribiendo
        scr.paste(cab, (0, 0), cab)
        d = ImageDraw.Draw(scr)
        nchar = int(len(c["busca"]) * A.tramo(t, t_esc0, t_esc1 - t_esc0)) if t >= t_esc0 else 0
        txt = c["busca"][:nchar]
        ft = A.F("Medium", 28)
        d.text((PAD + 70, 93), txt, font=ft, fill=C.AZUL, anchor="lm")
        if t < t_res and int(t * 2.5) % 2 == 0:
            cx = PAD + 72 + d.textlength(txt, font=ft)
            d.line((cx, 76, cx, 110), fill=AZUL_ENLACE, width=3)
        return scr, sc

    def fotograma(t):
        im = fondo.copy()
        s = A.eo(A.tramo(t, t_sube, 0.55))
        A.pega(im, tit, (A.W - tit.width) / 2, 150 - 200 * s, a=1 - s)
        ym = y_m0 + (Y_MOVIL - y_m0) * s
        scr, sc = pantalla(t)
        x_s, y_s = x_m + caja[0], ym + caja[1]
        im.paste(scr, (int(x_s), int(y_s)), mascara)
        A.pega(im, marco, x_m, ym)
        k = activo(t)
        if 0 <= k < n and t < t_final:
            a = acciones[k]
            if a[0] == "toca":
                j, b = a[1], a[2]
                bx0, by0, bx1, by1 = fichas[j][1][b]
                tx, ty = x_s + (bx0 + bx1) / 2, y_s + ys[j] - sc + (by0 + by1) / 2
                m = A.eo(A.tramo(t, ini[k] + 0.3, 0.6))
                fx, fy = tx + 220 * (1 - m), ty + 380 * (1 - m)
                toque = A.tramo(t, ini[k] + 0.95, 0.35)
                if 0 < toque < 1:
                    rr = 30 + 50 * toque
                    ImageDraw.Draw(im).ellipse((tx - rr, ty - rr, tx + rr, ty + rr), outline=C.AMARILLO, width=6)
                kd = 1 - 0.15 * math.sin(math.pi * toque)
                A.pega(im, dd, fx - dd.width / 2, fy - dd.height / 2, a=A.tramo(t, ini[k] + 0.2, 0.2), k=kd, centro=True)
            if k in etis:
                et = etis[k]
                e = A.tramo(t, ini[k] + 0.3, 0.3)
                if a[0] in ("senala", "arregla"):
                    j = a[1] if a[0] == "senala" else i_tu
                    yy = y_s + ys[j] - sc + FICHA_H - et.height / 2 - 4
                elif a[0] == "baja":
                    yy = y_s + sh - 260
                else:
                    yy = None
                if a[0] == "muestra":
                    # tu ficha, como deberia ser, encima de todo y en grande
                    sp = bueno[0]
                    kk = 1.45
                    ee = A.eo(A.tramo(t, ini[k] + 0.1, 0.45))
                    bx = (A.W - SW * kk) / 2
                    by = ym + PHM / 2 - FICHA_H * kk / 2 + 60 * (1 - ee)
                    marco_b = Image.new("RGBA", (int(SW * kk) + 24, int(FICHA_H * kk) + 24), (0, 0, 0, 0))
                    ImageDraw.Draw(marco_b).rounded_rectangle((0, 0, marco_b.width - 1, marco_b.height - 1), 30,
                                                               fill=C.BLANCO, outline=C.VERDE, width=8)
                    A.pega(im, marco_b, bx - 12, by - 12, a=ee)
                    A.pega(im, sp, bx, by, a=ee, k=kk)
                    yy = by + FICHA_H * kk + 6
                if yy is not None:
                    A.pega(im, et, (A.W - et.width) / 2, yy, k=A.rebote(e), centro=True)
        subs.pinta(im, t)
        return A.entra_final(im, final, t, t_final)

    marcas = [0.0, t_sube - 0.3] + [x + 1.3 for x in ini] + [dur - 0.4]
    A.graba(fotograma, dur, salida, vz["wav"], rev, marcas[:8])


def publicar(v, ruta):
    A.publicar(ruta, f"La búsqueda en directo · {A.limpio(v['es']['titulo'])}",
               {i: PIE[i] for i in ("es", "ca")},
               aviso="el buscador es una ilustración genérica; negocios, notas, reseñas y horarios son de ejemplo (inventados).")
