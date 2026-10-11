"""Atajos para escribir temas: cada funcion devuelve una maqueta para carrusel.py."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
COMUN = {"etiqueta": "Disseny Web PM · Girona", "de": "de 5"}
IDI = {"es": {"desliza": "Desliza →", "cta": "Escríbeme por WhatsApp"},
       "ca": {"desliza": "Llisca →", "cta": "Escriu-me per WhatsApp"}}


def L(t, n, m):
    return {"titulo": t, "nota": n, "maqueta": m}


def lista(tit, filas, cas=False, **kw):
    return {"tipo": "lista", "titulo": tit, "filas": filas, "casillas": cas, **kw}


def gal(tit, et, pie):
    return {"tipo": "galeria", "titulo": tit, "etiquetas": et, "pie": pie}


def chat(*g):
    return {"tipo": "chat", "globos": [{"de": d, "fotos": True} if t == "FOTOS" else {"de": d, "texto": t} for d, t in g]}


def ficha(filas, val="4,7", **kw):
    return {"tipo": "ficha", "valoracion": val, "filas": filas, **kw}


def web(t, s, menu, **kw):
    return {"tipo": "web", "titulo": t, "subtitulo": s, "menu": menu, "foto": kw.pop("foto", 0), **kw}


def mb(tit, txt, b):
    return {"tipo": "movil_boton", "titular": tit, "texto": txt, "boton": b}


def zon(t, z):
    return {"tipo": "zonas", "titulo": t, "zonas": z}


def pasos(t, p, s=1):
    return {"tipo": "pasos", "titulo": t, "pasos": p, "senalado": s}


def res(rt, r):
    return {"tipo": "resenas", "respuesta_titulo": rt, "resenas": r}


def ad(a, d, pie):
    return {"tipo": "antes_despues", "antes": a, "despues": d, "pie": pie}


def movil(variante, **kw):
    return {"tipo": "movil", "variante": variante, **kw}


def K(m, k=1.3):
    m = dict(m)
    m["k"] = k
    return m


def tema(id_, idi, **c):
    """Guarda carruseles/<id_>.json comprobando la forma."""
    d = {**COMUN, **IDI[idi], "id": id_, "idioma": idi, **c}
    assert len(d["laminas"]) == 5, id_
    assert len(d["guion"]) == 7, id_
    for k in ("negocio", "dominio", "pastilla", "portada", "gancho", "cierre", "guardar", "hashtags", "aviso"):
        assert k in d, (id_, k)
    (RAIZ / "carruseles" / f"{id_}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    return d
