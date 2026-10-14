#!/usr/bin/env python3
"""Busca y descarga videos de archivo de Pexels (gratis, uso comercial
permitido, sin atribucion obligatoria). Guarda cache en .tmp/pexels/ y anota
autor y enlace de cada clip (por si se quiere citar).

La clave la pone el entorno de la nube (secreto de red con la cabecera
`Authorization` para api.pexels.com); en local, PEXELS_API_KEY en .env.

Uso:  python3 herramientas/pexels.py "small shop owner phone" [--n 3]
"""
import argparse
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CACHE = RAIZ / ".tmp" / "pexels"


def _get(url, json_=True):
    cab = {"User-Agent": "dissenywebpm-videos"}
    if os.environ.get("PEXELS_API_KEY") and "api.pexels.com" in url:
        cab["Authorization"] = os.environ["PEXELS_API_KEY"]
    with urllib.request.urlopen(urllib.request.Request(url, headers=cab), timeout=90) as r:
        d = r.read()
    return json.loads(d) if json_ else d


def busca(consulta, n=3, min_dur=5, max_dur=30):
    """Clips verticales (o que se puedan recortar a vertical) en HD."""
    q = urllib.parse.urlencode({"query": consulta, "orientation": "portrait", "size": "medium", "per_page": 30})
    res = _get(f"https://api.pexels.com/videos/search?{q}")
    out = []
    for v in res.get("videos", []):
        if not (min_dur <= v["duration"] <= max_dur):
            continue
        # el fichero mas pequeno que sea al menos 1080 de ancho (vertical)
        fs = sorted((f for f in v["video_files"] if f.get("width") and f["width"] >= 1000
                     and f["height"] > f["width"] and f.get("file_type") == "video/mp4"),
                    key=lambda f: f["width"])
        if not fs:
            continue
        out.append({"id": v["id"], "url": fs[0]["link"], "dur": v["duration"],
                    "autor": v["user"]["name"], "pagina": v["url"]})
        if len(out) >= n:
            break
    return out


def descarga(clip):
    CACHE.mkdir(parents=True, exist_ok=True)
    dest = CACHE / f"{clip['id']}.mp4"
    if not dest.exists():
        dest.write_bytes(_get(clip["url"], json_=False))
        (CACHE / f"{clip['id']}.json").write_text(json.dumps(clip, ensure_ascii=False))
    return dest


def clips(consulta, n=1):
    return [descarga(c) for c in busca(consulta, n)]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("consulta")
    ap.add_argument("--n", type=int, default=3)
    a = ap.parse_args()
    for c in busca(a.consulta, a.n):
        print(c["id"], c["dur"], "s ·", c["autor"], "·", descarga(c))
