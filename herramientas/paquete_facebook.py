#!/usr/bin/env python3
"""Paquete de Facebook ORDENADO para el móvil de Pablo: una carpeta por
idioma y, dentro, cada publicación numerada en el orden de publicar:
«01 Título.png» + «01 Título.txt» (la imagen y el texto, uno al lado del otro).
Las de temporada van al final con la fecha en el nombre.

    python3 herramientas/paquete_facebook.py <carpeta_destino>
"""
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import facebook as FB  # noqa: E402

RAIZ = FB.RAIZ
# orden de planes/PLAN_30.md y después los temas anteriores, separando los
# que se parecen (23 de 08/01 y 29 de 10)
ORDEN = ["43_resena_mala", "33_veterinario", "56_sales", "41_abogado", "44_whatsapp", "40_pasteleria",
         "46_datos", "35_inmobiliaria", "47_fotos", "42_canina", "50_excusas", "39_psicologo",
         "59_preguntas", "37_autoescuela", "60_boca", "36_fotografo", "54_presupuesto", "53_mayores",
         "45_dominio", "55_web_y_ficha", "57_seguro", "48_web_nueva", "58_oferta", "61_legal",
         "49_bilingue", "03_senales", "12_clinica", "30_taller", "09_proceso", "13_reformas",
         "23_busca", "15_gimnasio", "17_asesoria", "14_rural", "18_estetica", "28_bienvenidos",
         "31_tienda", "29_movil"]
TEMPORADA = {"es": [("52_navidad", "principios de noviembre"), ("38_floristeria", "antes de San Valentín o Día de la Madre"),
                    ("32_turistas", "mayo-junio"), ("51_vacaciones", "mediados de julio"), ("34_academia", "finales de agosto")],
             "ca": [("52_navidad", "principis de novembre"), ("38_floristeria", "abans de Sant Jordi o el Dia de la Mare"),
                    ("32_turistas", "maig-juny"), ("51_vacaciones", "mitjans de juliol"), ("34_academia", "finals d'agost")]}
LEEME = {
    "es": ("CÓMO PUBLICAR EN FACEBOOK\n\n"
           "1. Abre la primera publicación que no hayas subido (empieza por la 01).\n"
           "2. En Facebook: Crear publicación → Foto → elige la imagen «NN Título.png».\n"
           "3. Abre «NN Título.txt», copia todo el texto y pégalo en la publicación.\n"
           "4. Publica. Una cada 2-3 días va bien.\n\n"
           "Las de la carpeta «temporada» solo en su fecha (está en el nombre).\n"
           "El vídeo del mismo tema súbelo como Reel otro día. El carrusel, solo en Instagram.\n"),
    "ca": ("COM PUBLICAR A FACEBOOK\n\n"
           "1. Obre la primera publicació que no hagis pujat (comença per la 01).\n"
           "2. A Facebook: Crea una publicació → Foto → tria la imatge «NN Títol.png».\n"
           "3. Obre «NN Títol.txt», copia tot el text i enganxa'l a la publicació.\n"
           "4. Publica. Una cada 2-3 dies va bé.\n\n"
           "Les de la carpeta «temporada» només a la seva data (és al nom).\n"
           "El vídeo del mateix tema puja'l com a Reel un altre dia. El carrusel, només a Instagram.\n"),
}


def nombre(c):
    t = FB.limpio(c["portada"]).replace("«", "").replace("»", "")
    t = re.sub(r'[\\/:*?"<>|¿?¡!.,]', "", t).strip()
    # corto por palabra entera, nunca a media palabra
    if len(t) > 42:
        t = t[:42].rsplit(" ", 1)[0]
    return t.strip()


def main():
    dest = Path(sys.argv[1])
    todos = sorted(p.name for p in (RAIZ / "salida").iterdir() if (p / "FACEBOOK.md").exists())
    estacionales = [t for t, _ in TEMPORADA["es"]]
    falta = [t for t in todos if t not in ORDEN and t not in estacionales]
    for idi, carpeta in (("es", "Facebook_CASTELLANO"), ("ca", "Facebook_CATALA")):
        base = dest / carpeta
        shutil.rmtree(base, ignore_errors=True)
        (base / "temporada").mkdir(parents=True)
        (base / "00 LEEME.txt").write_text(LEEME[idi], encoding="utf-8")
        lista = [(t, None) for t in ORDEN + falta] + TEMPORADA[idi]
        n = 0
        for tema, cuando in lista:
            c = json.loads((RAIZ / "carruseles" / f"{tema}_{idi}.json").read_text(encoding="utf-8"))
            if cuando:
                nom, sitio = f"{nombre(c)} ({cuando})", base / "temporada"
            else:
                n += 1
                nom, sitio = f"{n:02d} {nombre(c)}", base
            shutil.copy(RAIZ / "salida" / tema / idi / "facebook.png", sitio / f"{nom}.png")
            (sitio / f"{nom}.txt").write_text(FB.texto(c, tema) + "\n", encoding="utf-8")
        print(carpeta, n, "+", len(TEMPORADA[idi]), "de temporada")


if __name__ == "__main__":
    main()
