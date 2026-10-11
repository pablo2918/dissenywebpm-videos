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

## Temas que Pablo YA tiene hechos (no repetir)
Del chat anterior, hechos y publicados por él con sus propias herramientas:
01 Maps (no sales en Google Maps) · 02 SEO web (no sales arriba) · 04 antes
de darte un precio · 05 carta en PDF · 06 así te pierde un cliente · 07
Instagram no es tu web · 08 por qué no te piden hora · 10 se nota que tu web es
vieja · 20 pregunta esto antes de pagar · 22 web hecha con prisa · 25 demo en
48 h · 26 tarjeta NFC · 27 publicar en Maps. El 19 (¿de quién es tu web?) está
aparcado: va contra su modelo.
Hechos aquí: 03 señales · 09 así trabajo · 12 clínica · 13 reformas · 14 casa
rural · 15 gimnasio · 17 asesoría · 18 estética · 23 lo que mira un cliente ·
28 «Bienvenidos» · 29 web en el móvil · 30 taller · 31 tienda de barrio.
Preparados SIN generar (ver `planes/PLAN_30.md`): 32–61, 30 temas listos para
`hacer.py`. Con esto, la lista de ideas de `ideas_carruseles.md` está agotada. Descartadas:
21 (va contra su modelo) y 24 (se pisa con su 01). Temas nuevos: proponer antes.
Ojo: 23 se parece a 08/01 y 29 a 10 → publicarlos separados en el tiempo.

## Herramientas (python3; Pillow, numpy)
**Un tema entero, los dos idiomas:** `python3 herramientas/hacer.py <tema>`
(necesita `carruseles/<tema>_es.json` y `_ca.json` con `guion` de 7 tramos:
gancho, 5 puntos y cierre). Deja todo en `salida/<tema>/<idioma>/` y hojas
de revisión en `.tmp/revision/` — MIRARLAS siempre antes de entregar.
Por partes: `carrusel.py` (láminas + gancho), `voz.py` (voz Azure: es Tristan
HD, ca Enric, +20 %, elegidas por Pablo; el tramo entero de una vez),
`voz_video.py` (vídeo 1080x1920, subtítulos = guion tal cual, -16 LUFS).
Maquetas: ficha, lista, galeria, resenas, movil_boton, antes_despues, zonas,
pasos, chat, web, movil (variantes zoom/telefono/blanco/juntos/formulario).
Hacer los temas de 2 en 2 (4 vídeos) para poder revisarlo todo a ojo.

### Gancho (los 3 primeros segundos)
Cada carrusel nuevo lleva en su JSON un bloque `gancho` (pastilla, texto con
`*resaltado*`, maqueta). `carrusel.py` lo dibuja a pantalla completa en
`salida/<tema>/<idioma>/gancho.png` (solo para el vídeo, no es una lámina del carrusel)
y `voz_video.py` lo usa en lugar de la portada para el primer tramo del guion,
sin subtítulos. El primer tramo del guion es la frase del gancho.
Ganchos que funcionan: algo que el que mira puede comprobar en su negocio YA
(«Coge el móvil y abre tu web. Ahora.», «Si tu web empieza con «Bienvenidos»…»),
con el problema dibujado. Nunca cifras inventadas.

### Subtítulos
Montserrat Black, contorno negro grueso, sombra, y la palabra que se está
diciendo en amarillo (karaoke). Frases cortas dichas deprisa van enteras.

Azure: la clave la inyecta el entorno de la nube (secreto de red con la
cabecera `Ocp-Apim-Subscription-Key` para swedencentral.tts.speech.microsoft.com).
El script nunca la ve. En local se lee de `AZURE_SPEECH_KEY` en `.env`
(que no se sube nunca).

## Redes
Carrusel (sin voz, música desde la app) para Instagram/Facebook; vídeo con
voz para Reels, TikTok y YouTube Shorts. Mismo tema: días distintos. Medir
WhatsApps, no likes.
