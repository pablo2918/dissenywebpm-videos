#!/usr/bin/env python3
"""Banco de fotos reales por sector para las maquetas de los carruseles.

Saca fotogramas de clips de Mixkit con «Stock Video Free License» (uso
comercial, sin atribución): busca por etiqueta, comprueba la licencia de cada
clip en su página, baja la versión 720p y guarda 2 fotogramas.

    python3 herramientas/banco_fotos.py candidatos [sector ...]
        -> .tmp/banco/<sector>/<id>_<n>.jpg + hoja de contacto para elegir a ojo
    python3 herramientas/banco_fotos.py elige <sector> <id_n> <id_n> ...
        -> copia las elegidas a fotos/<sector>/ (las que usa carrusel.py)

Las fotos elegidas y su clip de origen quedan anotadas en fotos/FUENTES.md.
"""
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parent.parent
TMP = RAIZ / ".tmp" / "banco"
FOTOS = RAIZ / "fotos"
UA = {"User-Agent": "Mozilla/5.0", "Referer": "https://mixkit.co/"}

# sector -> etiquetas de Mixkit donde buscar
SECTORES = {
    "dentista": ["dentist"], "reformas": ["renovation", "construction-worker"], "rural": ["country-house", "cabin"],
    "gimnasio": ["gym"], "oficina": ["office"], "estetica": ["spa", "manicure"], "peluqueria": ["hairdresser", "barber"],
    "restaurante": ["restaurant", "chef"], "fisio": ["massage", "physiotherapy"], "taller": ["mechanic", "car-repair"],
    "tienda": ["store", "shop"], "veterinario": ["veterinarian", "vet"], "academia": ["classroom", "student"],
    "inmobiliaria": ["apartment", "real-estate"], "fotografo": ["photographer", "wedding"], "autoescuela": ["driving"],
    "floristeria": ["florist", "flowers"], "psicologo": ["therapy", "psychologist"], "pasteleria": ["cake", "bakery"],
    "abogado": ["lawyer", "business-meeting"], "perros": ["dog-grooming", "dog"], "farmacia": ["pharmacy"],
    "fontaneria": ["plumber"], "cafe": ["coffee-shop", "cafe"], "interiores": ["bathroom", "kitchen"], "ferreteria": ["tools", "hardware-store", "carpenter"],
}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def clips_de(etiqueta, maximo=8):
    try:
        h = get(f"https://mixkit.co/free-stock-video/{etiqueta}/").decode("utf-8", "ignore")
    except Exception:
        return []
    slugs = list(dict.fromkeys(re.findall(r'href="/free-stock-video/([a-z0-9-]+-(\d+))/"', h)))
    return slugs[:maximo]


def licencia_ok(slug):
    try:
        h = get(f"https://mixkit.co/free-stock-video/{slug}/").decode("utf-8", "ignore")
    except Exception:
        return False
    return bool(re.search(r'"license":"https://mixkit\.co/license/#videoFree"', h))


def candidatos(sectores):
    for s in sectores:
        dest = TMP / s
        dest.mkdir(parents=True, exist_ok=True)
        vistos = set()
        for et in SECTORES[s]:
            for slug, id_ in clips_de(et):
                if id_ in vistos or len(vistos) >= 8:
                    continue
                if not licencia_ok(slug):
                    continue
                vistos.add(id_)
                mp4 = TMP / f"{id_}.mp4"
                if not mp4.exists():
                    try:
                        mp4.write_bytes(get(f"https://assets.mixkit.co/videos/{id_}/{id_}-720.mp4"))
                    except Exception:
                        continue
                for n, t in enumerate(("25%", "70%")):
                    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                                         "-of", "csv=p=0", str(mp4)]).decode() or 5)
                    ss = dur * float(t[:-1]) / 100
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.2f}", "-i", str(mp4), "-frames:v", "1",
                                    str(dest / f"{id_}_{n}.jpg")], check=False)
                (dest / f"{id_}.txt").write_text(slug)
        hoja(dest)
        print(s, len(vistos), "clips")


def hoja(carpeta):
    fs = sorted(carpeta.glob("*.jpg"))
    if not fs:
        return
    w, h = 300, 169
    cols = 4
    c = Image.new("RGB", (cols * (w + 8), ((len(fs) + cols - 1) // cols) * (h + 30)), "white")
    d = ImageDraw.Draw(c)
    for i, f in enumerate(fs):
        im = Image.open(f).convert("RGB")
        im.thumbnail((w, h))
        x, y = (i % cols) * (w + 8), (i // cols) * (h + 30)
        c.paste(im, (x, y))
        d.text((x + 4, y + h + 4), f.stem, fill="black")
    c.save(TMP / f"hoja_{carpeta.name}.jpg", quality=80)


def elige(sector, ids):
    dest = FOTOS / sector
    dest.mkdir(parents=True, exist_ok=True)
    fuentes = FOTOS / "FUENTES.md"
    lineas = fuentes.read_text(encoding="utf-8").splitlines() if fuentes.exists() else [
        "# Fotos del banco (fotogramas de Mixkit, «Stock Video Free License»)", ""]
    for i, x in enumerate(ids):
        carpeta, x = (x.split("/") if "/" in x else (sector, x))
        src = TMP / carpeta / f"{x}.jpg"
        im = Image.open(src).convert("RGB")
        im.thumbnail((1280, 1280))
        im.save(dest / f"{i}.jpg", quality=86)
        slug = (TMP / carpeta / f"{x.split('_')[0]}.txt").read_text()
        lineas.append(f"- {sector}/{i}.jpg ← https://mixkit.co/free-stock-video/{slug}/")
    fuentes.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(sector, len(ids), "fotos")


if __name__ == "__main__":
    if sys.argv[1] == "candidatos":
        candidatos(sys.argv[2:] or list(SECTORES))
    elif sys.argv[1] == "elige":
        elige(sys.argv[2], sys.argv[3:])
    else:
        print(json.dumps(SECTORES, indent=1))
