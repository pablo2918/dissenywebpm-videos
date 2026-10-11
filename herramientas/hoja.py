#!/usr/bin/env python3
"""Hoja de contacto: las 7 laminas de un carrusel en una imagen (4x2)."""
import sys
from pathlib import Path
from PIL import Image
c = Path(sys.argv[1]); out = Path(sys.argv[2])
fs = sorted(c.glob("*.png")); w = int(sys.argv[3]) if len(sys.argv) > 3 else 480
h = int(w * 1.25)
hoja = Image.new("RGB", (w * 4 + 50, h * 2 + 30), (200, 200, 200))
for i, f in enumerate(fs):
    hoja.paste(Image.open(f).resize((w, h), Image.LANCZOS), (10 + (i % 4) * (w + 10), 10 + (i // 4) * (h + 10)))
hoja.save(out)
