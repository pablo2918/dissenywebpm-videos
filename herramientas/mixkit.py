"""Videos de archivo de Mixkit (gratis, sin clave). Solo se usan clips con la
«Stock Video Free License» (uso comercial permitido, sin atribucion); cada clip
elegido se comprobo en la pagina de Mixkit. Cache en .tmp/mixkit/."""
import urllib.error
import urllib.request
from pathlib import Path

CACHE = Path(__file__).resolve().parent.parent / ".tmp" / "mixkit"


def clip(id_):
    CACHE.mkdir(parents=True, exist_ok=True)
    dest = CACHE / f"{id_}.mp4"
    if not dest.exists():
        for calidad in ("2160", "1080", "720"):
            req = urllib.request.Request(f"https://assets.mixkit.co/videos/{id_}/{id_}-{calidad}.mp4",
                                         headers={"User-Agent": "Mozilla/5.0", "Referer": "https://mixkit.co/"})
            try:
                dest.write_bytes(urllib.request.urlopen(req, timeout=180).read())
                break
            except urllib.error.HTTPError:
                continue
    return dest
