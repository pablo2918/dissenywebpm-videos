#!/usr/bin/env python3
"""Deja el ordenador listo para hacer carruseles y vídeos. Se puede lanzar
tantas veces como haga falta: lo que ya está instalado se lo salta.

    python herramientas/instalar.py

Instala: paquetes de Python (requirements.txt), ffmpeg y Node si faltan
(winget en Windows, brew en Mac), las dependencias de Remotion, los
navegadores que usan Remotion y las capturas de webs, y el modelo de
transcripción (para sincronizar la voz de Pablo). Al final hace una prueba.
"""
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
REMO = RAIZ / "remotion"
SO = platform.system()  # Windows, Darwin, Linux
fallos = []


def paso(t):
    print(f"\n== {t}")


def corre(cmd, cwd=None, ok=True):
    print("  $", " ".join(cmd))
    r = subprocess.run(cmd, cwd=cwd, shell=(SO == "Windows"))
    if ok and r.returncode != 0:
        fallos.append(" ".join(cmd))
    return r.returncode == 0


def instala_programa(nombre, winget, brew):
    if shutil.which(nombre):
        print(f"  {nombre}: ya está")
        return
    if SO == "Windows" and shutil.which("winget"):
        corre(["winget", "install", "-e", "--id", winget, "--accept-source-agreements", "--accept-package-agreements"])
        print(f"  (cierra y vuelve a abrir la terminal para que se vea {nombre} y lanza otra vez este script)")
    elif SO == "Darwin" and shutil.which("brew"):
        corre(["brew", "install", brew])
    elif SO == "Linux" and shutil.which("apt-get"):
        corre(["sudo", "apt-get", "install", "-y", brew])
    else:
        fallos.append(f"instalar {nombre} a mano")


def main():
    paso("Python")
    if sys.version_info < (3, 10):
        fallos.append("Python 3.10 o más nuevo")
    corre([sys.executable, "-m", "pip", "install", "-q", "-r", str(RAIZ / "requirements.txt")])

    paso("ffmpeg y Node")
    instala_programa("ffmpeg", "Gyan.FFmpeg", "ffmpeg")
    instala_programa("node", "OpenJS.NodeJS.LTS", "node")

    if shutil.which("npm"):
        paso("Remotion (motor de vídeo)")
        corre(["npm", "install", "--no-audit", "--no-fund"], cwd=REMO)
        if not Path("/opt/pw-browsers").exists():  # en la nube ya vienen
            corre(["npx", "remotion", "browser", "ensure"], cwd=REMO)
            corre(["npx", "playwright-core", "install", "chromium"], cwd=REMO)

    paso("Modelo de transcripción (para la voz de Pablo; la primera vez baja ~500 MB)")
    try:
        from faster_whisper import WhisperModel
        WhisperModel("small", device="cpu", compute_type="int8")
        print("  listo")
    except Exception as e:  # noqa: BLE001
        fallos.append(f"modelo de transcripción: {e}")

    paso("Voz provisional Azure (opcional)")
    env = RAIZ / ".env"
    if os.environ.get("AZURE_SPEECH_KEY") or (env.exists() and "AZURE_SPEECH_KEY" in env.read_text()):
        print("  clave encontrada")
    else:
        print("  sin clave: no pasa nada si se usa la voz de Pablo (remo.py --audio).")

    if shutil.which("npx") and not fallos:
        paso("Prueba: un fotograma del vídeo de mito")
        prueba = RAIZ / ".tmp" / "prueba_instalacion.png"
        prueba.parent.mkdir(exist_ok=True)
        corre(["npx", "remotion", "still", "Mito", str(prueba), "--frame=10", "--log=error"], cwd=REMO)

    print("\n" + ("TODO LISTO." if not fallos else "FALTA:\n  - " + "\n  - ".join(fallos)))
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
