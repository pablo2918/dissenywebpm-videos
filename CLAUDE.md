# Disseny Web PM · carruseles y vídeos con voz (nube)

Pablo Rubiales — Disseny Web PM (webs a código y SEO local, Girona).
Teléfono 641 27 74 95 · dissenywebpm.com. Público: restaurantes, peluquerías,
oficios. Idiomas: castellano y catalán. Pablo no es técnico: explícale el
porqué con una comparación de la vida real, en castellano, sin florituras.

## Qué vende (manda sobre el contenido)
- Webs a código (sin gestor), alojadas en Cloudflare. Demo gratis en 48 h.
- Web desde 420 € + 15 €/mes (dominio, alojamiento y mantenimiento básico).
- Pack digitalización 580 € + 22 €/mes: web + ficha de Google Maps + tarjeta NFC.
- Pack SEO y Maps (mensual): **sin precio en el contenido**, presupuesto por WhatsApp.

**Nunca** sugerir que el cliente deba tener accesos técnicos/Cloudflare,
editar la web él mismo o preocuparse por pagar el alojamiento. Antes de
proponer un tema, comprobar que el consejo lo cumple la propia oferta.

## Reglas
- No inventar datos, cifras ni promesas. Si una maqueta usa datos de ejemplo,
  `PUBLICAR.md` lo dice en su «Aviso».
- Si Pablo da un texto, se usa tal cual (sin corregir).
- Revisar SIEMPRE los renders antes de entregar (hojas de contacto con
  `herramientas/hoja.py`, fotogramas del vídeo): nada cortado, solapado ni
  palabras sueltas colgando.
- CTA: «Escríbeme por WhatsApp» / «Escriu-me per WhatsApp».

## Herramientas (python3; Pillow, numpy)
1. `herramientas/carrusel.py carruseles/<id>.json` → 7 láminas 1440x1800 en
   `salida/carruseles/<id>/`. `*resaltado*`, `//` salto de línea. Maquetas:
   ficha, lista, galeria, resenas, movil_boton, antes_despues, zonas, pasos, chat.
2. `herramientas/voz.py guiones/<id>.txt --idioma es|ca --salida .tmp/<id>`
   → voz Azure (es: Tristan HD, ca: Enric; velocidad +35 %, elegidas por Pablo).
   Un tramo por lámina, separados por línea en blanco.
3. `herramientas/voz_video.py .tmp/<id> --carpeta salida/carruseles/<id> --salida salida/<id>_voz.mp4`
   → 1080x1920, subtítulos = guion tal cual, volumen -16 LUFS.

Azure: la clave la inyecta el entorno de la nube (secreto de red con la
cabecera `Ocp-Apim-Subscription-Key` para swedencentral.tts.speech.microsoft.com).
El script nunca la ve. En local se lee de `AZURE_SPEECH_KEY` en `.env`
(que no se sube nunca).

## Redes
Carrusel (sin voz, música desde la app) para Instagram/Facebook; vídeo con
voz para Reels, TikTok y YouTube Shorts. Mismo tema: días distintos. Medir
WhatsApps, no likes.
