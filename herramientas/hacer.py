#!/usr/bin/env python3
"""Hace un tema entero en los dos idiomas: laminas, gancho, voz y video.
Deja tambien hojas de revision en .tmp/revision/ para MIRARLAS antes de entregar.

Uso:  python3 herramientas/hacer.py 30_taller [31_tienda ...]
Necesita carruseles/<tema>_<es|ca>.json (con "guion" de 7 tramos).
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
H = RAIZ / "herramientas"
REV = RAIZ / ".tmp" / "revision"


def py(*args):
    subprocess.run([sys.executable, *map(str, args)], check=True, cwd=RAIZ)


def revision(tema, idi):
    base = RAIZ / "salida" / tema / idi
    REV.mkdir(parents=True, exist_ok=True)
    py(H / "hoja.py", base / "carrusel", REV / f"{tema}_{idi}_laminas.png", 480)
    sys.path.insert(0, str(H))
    import voz_video as vv
    d = json.loads((RAIZ / ".tmp" / f"{tema}_{idi}.json").read_text())
    bl = vv.bloques([p for p in d["palabras"] if p["tramo"] > 0])
    ts = [0.05] + [b[min(1, len(b) - 1)]["inicio"] + 0.05 for b in bl[::max(1, len(bl) // 6)]][:6] + [d["duracion"] + 0.8]
    ims = []
    for t in ts:
        f = REV / "f.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", base / "video.mp4",
                        "-frames:v", "1", f], check=True)
        ims.append(Image.open(f).resize((360, 640)))
    hoja = Image.new("RGB", (360 * 4, 640 * 2), "white")
    for i, im in enumerate(ims[:8]):
        hoja.paste(im, ((i % 4) * 360, (i // 4) * 640))
    hoja.save(REV / f"{tema}_{idi}_video.png")


def main():
    for tema in sys.argv[1:]:
        for idi in ("es", "ca"):
            cid = f"{tema}_{idi}"
            c = json.loads((RAIZ / "carruseles" / f"{cid}.json").read_text())
            guion = RAIZ / "guiones" / f"{cid}.txt"
            guion.write_text("\n\n".join(c["guion"]) + "\n", encoding="utf-8")
            py(H / "carrusel.py", RAIZ / "carruseles" / f"{cid}.json")
            py(H / "voz.py", guion, "--idioma", idi, "--salida", RAIZ / ".tmp" / cid)
            base = RAIZ / "salida" / tema / idi
            py(H / "voz_video.py", RAIZ / ".tmp" / cid, "--carpeta", base / "carrusel",
               "--salida", base / "video.mp4")
            revision(tema, idi)
            print(f"OK {cid}")


if __name__ == "__main__":
    main()
