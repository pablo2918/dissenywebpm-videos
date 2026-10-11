#!/usr/bin/env python3
"""Hace los videos de los formatos animados, en los dos idiomas.

Uso:  python3 herramientas/formato.py mito            (los 5 del formato)
      python3 herramientas/formato.py mito 2 4        (solo el 2 y el 4)
      python3 herramientas/formato.py mito 2 --idi es (solo castellano)

Formatos: busqueda, mito, plantilla, bienmal, montaje, pregunta.
El texto de cada video esta en planes/plan_<formato>.py; el dibujo, en
herramientas/f_<formato>.py.
Deja: salida/formatos/<formato>/<NN_nombre>/<es|ca>/video.mp4 y PUBLICAR.md,
y hojas de revision en .tmp/revision/formatos/ (MIRARLAS antes de entregar).
"""
import argparse
import importlib
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))
sys.path.insert(0, str(RAIZ / "planes"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("formato")
    ap.add_argument("numeros", nargs="*", type=int)
    ap.add_argument("--idi", choices=["es", "ca"])
    a = ap.parse_args()
    motor = importlib.import_module(f"f_{a.formato}")
    datos = importlib.import_module(f"plan_{a.formato}")
    for n, v in enumerate(datos.VIDEOS, 1):
        if a.numeros and n not in a.numeros:
            continue
        nombre = f"{n:02d}_{v['id']}"
        base = RAIZ / "salida" / "formatos" / a.formato / nombre
        for idi in ([a.idi] if a.idi else ["es", "ca"]):
            rev = RAIZ / ".tmp" / "revision" / "formatos" / f"{a.formato}_{nombre}_{idi}.png"
            motor.hacer(v, idi, base / idi / "video.mp4", rev, RAIZ / ".tmp" / "formatos" / f"{a.formato}_{nombre}_{idi}")
        motor.publicar(v, base / "PUBLICAR.md")


if __name__ == "__main__":
    main()
