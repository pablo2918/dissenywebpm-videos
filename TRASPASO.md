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
3. [ ] 3 vídeos piloto en estilos distintos para comparar con los actuales.
Ideas a aplicar: gancho en el segundo 0 (frase en pantalla + voz), cambio
visual cada 1,5–3 s, efectos de sonido (whoosh, pop, clic), imagen real
(grabar dissenywebpm.com en un móvil con Playwright) en vez de archivo
genérico, mito con «¿Cuánto sabes de SEO?» y marcador de aciertos, formatos
«Busco X en [ciudad]», «web en 48 h en cámara rápida», antes/después con
barrido, «POV: eres un cliente…». Ciudades de toda España.

## Diario (lo último arriba)
- **14-10-2026** · Estudio hecho (`estudio/ESTUDIO.md`). Proyecto Remotion
  creado en `remotion/` (render probado). Siguiente: 3 pilotos.
- **14-10-2026** · Creado este archivo. Pablo instaló Remotion, watch-video y
  video-shotcraft. Empezando el paso 1 (estudio de vídeos).
