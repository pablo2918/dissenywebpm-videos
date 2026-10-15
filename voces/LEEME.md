# Voces de Pablo (VoiceStudio)

Aquí van los audios con la voz clonada de Pablo, uno por vídeo e idioma,
con el nombre `<id>_<idioma>.<ext>` (p. ej. `antes_despues_es.mp3`).
Cada audio lee el `guion_voz.txt` de `salida/remotion/<id>/<idioma>/` entero,
de principio a fin. Luego: `python3 herramientas/remo.py remotion/guiones/<id>.json --audio voces/<id>_es.mp3`
