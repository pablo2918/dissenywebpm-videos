# TRASPASO — estado del proyecto para seguir en otro chat

> Pablo: si pasas a un Claude Code normal (en tu ordenador), dile al empezar:
> «Lee `TRASPASO.md` y `CLAUDE.md` y sigue donde lo dejamos».
> Este archivo se actualiza a medida que se trabaja (lo último, arriba en
> «Diario»). `CLAUDE.md` tiene las reglas fijas del negocio y del contenido.

## Cómo seguir en local (Claude Code en tu ordenador)
1. Clonar el repo privado: `git clone https://github.com/pablo2918/dissenywebpm-videos`
2. Instalar: Python 3 con `pip install pillow numpy`, `ffmpeg`, y Node 20+
   (para Remotion: `cd remotion && npm install`, ver «Motor nuevo»).
3. Voz Azure (la de las pruebas): en local se lee `AZURE_SPEECH_KEY` de un
   `.env` en la raíz (no se sube nunca). Cuando esté la voz de Pablo
   (VoiceStudio), ya no hará falta.
4. Plugins de Claude Code que usamos: **Remotion**, **watch-video** y
   **video-shotcraft** (instalados por Pablo el 14-10-2026 en claude.ai).

## Qué hay hecho (resumen)
- Carruseles + vídeo con voz: temas 03–61 (ver `CLAUDE.md` y `planes/PLAN_30.md`).
- Formatos animados (motor Python propio, `herramientas/formato.py`):
  busqueda, mito (20), plantilla, bienmal, montaje, pregunta — es y ca.
- Pruebas de vídeo de archivo (Mixkit) en 3 estilos: `formato.py archivo`.
- Todo lo entregable está en `salida/` (cada vídeo con su `PUBLICAR.md`).

## Voz de Pablo (APARCADO, decisión 14-10-2026)
- Pablo clonará su voz con **VoiceStudio** (repo de GitHub, IA en local).
- Flujo previsto: Claude deja el texto de cada vídeo en un archivo
  (`guion_voz.txt` junto al vídeo) → Pablo lo pasa a VoiceStudio → sube el
  audio → Claude lo transcribe (marcas de tiempo por palabra) y monta el
  vídeo encima. Más adelante, quizá acceso al otro ordenador para hacerlo
  todo automático.
- Mientras tanto, las pruebas usan la voz Azure como provisional.

## Plan en marcha: vídeos con más gancho (pedido 14-10-2026)
Pablo quiere vídeos con más gancho, más naturales y de tipos distintos.
1. [x] Estudio de vídeos que funcionan → **`estudio/ESTUDIO.md`** (leerlo:
       conclusiones y cómo repetir el estudio; desde la nube YouTube solo
       deja bajar subtítulos y storyboard).
2. [~] Motor nuevo con Remotion en `remotion/` (proyecto creado, renderiza
       en la nube con el Chromium de /opt/pw-browsers, ver remotion.config.ts).
3. [x] 3 vídeos piloto (solo castellano, voz Azure provisional), en
       `salida/remotion/<id>/` con PUBLICAR.md y es/guion_voz.txt:
       - Piloto 1 «antes/después» (`antes_despues`, composición `AntesDespues`):
         panadería inventada de Valladolid, web vieja vs nueva grabadas de verdad.
       - Piloto 2 «pregunta de cliente» (`pregunta_maps`, `Pregunta`): rótulo
         rojo con la pregunta arriba; Maps animado; relevancia/distancia/prominencia.
       - Piloto 3 «mito o verdad 2.0» (`mito_seo`, `Mito`): gancho «¿Cuánto
         sabes de SEO?», marcador de 3, tic-tac (pausa de 3,2 s en la voz con
         `"pausa"` en la escena), sello y explicación.
4. [x] Pablo (14-10): le encantaron los 3, sobre todo el antes/después de la
       panadería («una barbaridad»). Pidió bajar un 15 % los efectos: hecho
       con `VOLUMEN_EFECTOS = 0.85` en `remotion/src/comun/marca.ts` (todos los
       efectos pasan por `<Sfx>` de `comun/Sfx.tsx`); los 3 pilotos rehechos.
5. [x] Carruseles mejorados (los 86, es y ca): ver «Carruseles mejorados» en
       CLAUDE.md (portada con maqueta, fotos reales por sector, antes/después
       con la misma foto, nota más grande, sin «Girona»).
6. [ ] SIGUIENTE (cuando Pablo tenga su voz con VoiceStudio): rehacer los
       vídeos con su voz y hacer más vídeos (sobre todo del estilo
       antes/después con webs grabadas de verdad) y la versión en catalán
       (copiar el guion con `"idioma": "ca"`). Voz: VoiceStudio → `--audio`.

### Cómo funciona el motor nuevo (Remotion)
- Guion: `remotion/guiones/<id>.json` (escenas con `tipo`, `voz`, `rotulos`
  que saltan cuando se dice una palabra `en`).
- `python3 herramientas/remo.py remotion/guiones/<id>.json` → voz → datos.json
  en `remotion/public/<id>_<idioma>/` → render → `salida/remotion/<id>/<idioma>/`
  (video.mp4 + guion_voz.txt). Con `--audio voz.wav` usa la voz de Pablo
  (la transcribe con faster-whisper). Con `--solo-datos` no renderiza
  (para mirar en `cd remotion && npx remotion studio`).
- Piezas comunes en `remotion/src/comun/`: Subtitulos (1–3 palabras,
  karaoke), Rotulo(s) (palabra clave arriba con «pop»), Movil (captura real
  de una web con scroll y capa para marcar cosas), Camara (zoom entre
  puntos), Fondo, Final (cierre con WhatsApp), Texto (*resaltado*).
- Efectos de sonido propios en `remotion/public/sfx/` (los genera
  `herramientas/sonidos.py`: whoosh, pop, clic, acierto, fallo, tictac).
- Capturas de webs: `cd remotion && node scripts/captura_web.mjs <html|url>
  <salida.png> 390 "selector1,selector2"` (también guarda la caja de cada
  selector para marcarla en el vídeo). Webs de ejemplo en `webs_ejemplo/`.
- Revisar SIEMPRE fotogramas antes de entregar (hoja en
  `.tmp/revision/remotion/`). Lecciones: el fotograma 0 ya debe enseñar el
  gancho (sin fundido de entrada); los subtítulos cortan antes de una
  palabra que no cabe (máx. 15 letras por línea).
Ideas a aplicar: gancho en el segundo 0 (frase en pantalla + voz), cambio
visual cada 1,5–3 s, efectos de sonido (whoosh, pop, clic), imagen real
(grabar dissenywebpm.com en un móvil con Playwright) en vez de archivo
genérico, mito con «¿Cuánto sabes de SEO?» y marcador de aciertos, formatos
«Busco X en [ciudad]», «web en 48 h en cámara rápida», antes/después con
barrido, «POV: eres un cliente…». Ciudades de toda España.

## Diario (lo último arriba)
- **14-10-2026** · Facebook corregido: imagen-resumen + texto por tema
  (`herramientas/facebook.py`, 43 temas es/ca); carrusel solo para Instagram.
- **14-10-2026** · Efectos −15 % y pilotos rehechos. Carruseles: banco de
  fotos reales (24 sectores, 124 fotos), portada nueva, antes/después con la
  misma foto; los 86 regenerados y revisados uno a uno.
- **14-10-2026** · Pilotos 2 y 3 hechos y revisados. Entregados los 3 a Pablo.
- **14-10-2026** · Piloto 1 (antes/después, panadería inventada de
  Valladolid) hecho y revisado. Render: ~3 min por vídeo de 37 s en la nube.
- **14-10-2026** · Estudio hecho (`estudio/ESTUDIO.md`). Proyecto Remotion
  creado en `remotion/` (render probado). Siguiente: 3 pilotos.
- **14-10-2026** · Creado este archivo. Pablo instaló Remotion, watch-video y
  video-shotcraft. Empezando el paso 1 (estudio de vídeos).
