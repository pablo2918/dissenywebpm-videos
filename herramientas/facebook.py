#!/usr/bin/env python3
"""Publicación de Facebook de un tema: UNA imagen-resumen (se entiende sin
abrir nada: título + los 5 puntos) y el texto de la publicación.

En Facebook un carrusel orgánico sale como mosaico recortado; por eso ahí va
esta imagen sola (y el vídeo como Reel). Instagram sigue con el carrusel.

    python3 herramientas/facebook.py 32_turistas      (los dos idiomas)
Deja: salida/<tema>/<idioma>/facebook.png y salida/<tema>/FACEBOOK.md
"""
import json
import re
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import carrusel as C  # noqa: E402

RAIZ = C.RAIZ
TXT = {
    "es": {"titulo": "Castellano", "cta": "Escríbeme por WhatsApp", "lista": "Lo que tiene que tener:"},
    "ca": {"titulo": "Català", "cta": "Escriu-me per WhatsApp", "lista": "El que ha de tenir:"},
}


def limpio(t):
    return re.sub(r"\s+", " ", t.replace("//", " ").replace("*", "")).strip()


def imagen(c):
    W, M = C.W, C.MARGEN
    im = C.lienzo(C.AZUL)
    d = C.D(im)
    d.text((M, 110), C.etiqueta(c), C.f("SemiBold", 26), C.GRIS_CLARO, anchor="lm")
    fp = C.f("ExtraBold", 32)
    pw = d.tl(c["pastilla"].upper(), fp) + 60
    d.rect((M, 160, M + pw, 226), fill=C.AMARILLO, r=33)
    d.text((M + 30, 194), c["pastilla"].upper(), fp, C.AZUL, anchor="lm")
    font, lin, tam = C.ajusta_titulo(c["portada"], "Black", 96, 56, W - 2 * M, 300, 3, d, interlinea=1.04)
    y = C.escribe_titulo(d, M, 262, font, lin, tam, C.BLANCO, interlinea=1.04) + 44
    # los 5 puntos: tarjetas blancas con numero amarillo
    # la letra mas grande con la que caben las 5 filas holgadas hasta el pie
    titulos = [limpio(lam["titulo"]) for lam in c["laminas"]]
    for tam_f in (44, 40, 36, 32, 29):
        ft = C.f("ExtraBold", tam_f)
        lh = tam_f * 1.12
        filas = [C.equilibra(t, ft, W - 2 * M - 150, d) for t in titulos]
        altos = [max(tam_f * 2.2, 2 * tam_f * 0.75 + lh * len(l)) for l in filas]
        hueco = 16
        if sum(altos) + 4 * hueco <= 1135 - y:
            break
    for i, (lineas, h) in enumerate(zip(filas, altos)):
        d.rect((M, y, W - M, y + h), fill=C.BLANCO, r=24)
        cy = y + h / 2
        d.ellipse((M + 24, cy - 32, M + 88, cy + 32), fill=C.AMARILLO)
        d.text((M + 56, cy + 2), str(i + 1), C.f("Black", 38), C.AZUL, anchor="mm")
        ly = cy - lh * (len(lineas) - 1) / 2
        for l in lineas:
            d.text((M + 120, ly), l, ft, C.AZUL, anchor="lm")
            ly += lh
        y += h + hueco
    # pie: logo + WhatsApp
    logo = Image.open(RAIZ / "logo" / "logo.png").convert("RGBA")
    lw = 150
    lh = lw * logo.height / logo.width
    logo = logo.resize((int(lw * C.S), int(lh * C.S)), Image.LANCZOS)
    py = 1220
    im.paste(logo, (int(M * C.S), int((py - lh / 2) * C.S)), logo)
    fc = C.f("ExtraBold", 34)
    cta = TXT[c["idioma"]]["cta"]
    cw = d.tl(cta, fc) + 70
    C.boton(d, (W - M - cw, py - 46, W - M, py + 2), cta, fc, C.AMARILLO, C.AZUL)
    d.text((W - M - cw / 2, py + 34), C.TELEFONO, C.f("ExtraBold", 32), C.AMARILLO, anchor="mm")
    return im


def hashtags(tema, idi):
    p = RAIZ / "salida" / tema / "PUBLICAR.md"
    if not p.exists():
        return ""
    bloques = re.findall(r"^#\w.*$", p.read_text(encoding="utf-8"), re.M)
    if not bloques:
        return ""
    linea = bloques[0] if idi == "es" or len(bloques) < 2 else bloques[1]
    # publico de toda Espana: fuera etiquetas de Girona
    return " ".join(h for h in linea.split() if "girona" not in h.lower() and "costabrava" not in h.lower())


def texto(c, tema):
    idi = c["idioma"]
    g = limpio(c["gancho"]["texto"])
    puntos = "\n".join(f"{i + 1}️⃣ {limpio(l["titulo"])}. {l["nota"]}" for i, l in enumerate(c["laminas"]))
    # si el cierre ya invita a escribir, no repetir «Escríbeme por WhatsApp»
    ya = any(w in c["cierre"].lower() for w in ("whatsapp", "escr"))
    cta = f"WhatsApp: {C.TELEFONO}" if ya else f"{TXT[idi]['cta']}: {C.TELEFONO}"
    return (f"{g}\n\n{puntos}\n\n{c['cierre']}. 👉 {cta}\n"
            f"📌 {c['guardar']}\n\n{hashtags(tema, idi)}").strip()


def main():
    tema = sys.argv[1]
    md = [f"# Facebook · {tema}", "",
          "Publica **una sola imagen** (`<idioma>/facebook.png`) con este texto. "
          "El vídeo del tema, súbelo a Facebook como **Reel** (otro día). "
          "El carrusel de 7 láminas, solo en Instagram.", ""]
    for idi in ("es", "ca"):
        ruta = RAIZ / "carruseles" / f"{tema}_{idi}.json"
        c = json.loads(ruta.read_text(encoding="utf-8"))
        C.usa_banco(tema)
        C.guarda(imagen(c), RAIZ / "salida" / tema / idi / "facebook.png")
        md += [f"## {TXT[idi]['titulo']}", "", texto(c, tema), ""]
    (RAIZ / "salida" / tema / "FACEBOOK.md").write_text("\n".join(md), encoding="utf-8")
    print("->", tema)


if __name__ == "__main__":
    main()
