# Vídeos con voz (Azure) sobre las láminas de un carrusel

1. Guion en `guiones/<id>.txt`: tramos separados por una línea en blanco.
   Cada tramo va con una lámina. Los subtítulos salen del guion tal cual.
2. Voz (clave y región en AZURE_SPEECH_KEY / AZURE_SPEECH_REGION, o en `.env`):
       python3 herramientas/voz.py guiones/04_precio_ca.txt --idioma ca --salida .tmp/04_precio_ca
   Voces por defecto: ca-ES-EnricNeural / es-ES-Tristan:DragonHDLatestNeural, a 1,35x (cambiar con --voz).
   `--simulado` = audio mudo con tiempos estimados, SOLO para probar el montaje.
3. Vídeo:
       python3 herramientas/voz_video.py .tmp/04_precio_ca \
           --carpeta salida/carruseles/04_precio_ca \
           --laminas 1_portada,2_01,3_02,4_03,7_cierre \
           --salida salida/04_precio_ca_voz.mp4
   1080x1920, 30 fps, H.264 CRF 19 + AAC 128k 48 kHz. Lámina al 80 % arriba,
   subtítulos debajo (76 px, baja solo si no cabe), sin zoom, 1,6 s de cierre.
4. Revisar fotogramas antes de publicar.

Fuente: Montserrat (licencia OFL, en `fuentes/`). `.env` no se comparte nunca.
