# TRASPASO — todo lo necesario para seguir en otro chat

> **Pablo**, en un chat nuevo de Claude Code solo tienes que decir:
> «Clona el repo privado `pablo2918/dissenywebpm-videos` (si no está ya),
> lee `TRASPASO.md` y `CLAUDE.md`, prepara el ordenador y sigue donde lo
> dejamos». Si al clonar se abre el navegador para entrar en GitHub, acepta:
> es lo único que puede tocarte hacer a ti.

---

## 0. Claude: lo primero en cada chat nuevo (hazlo tú, sin pedírselo a Pablo)
1. Si no está el repo: `git clone https://github.com/pablo2918/dissenywebpm-videos`
   y trabaja dentro. Rama: `main` (se sube directo a `main`, repo privado).
2. Lanza **`python herramientas/instalar.py`** (en Windows `python`, en Mac/Linux
   `python3`). Instala todo lo que falte y termina con «TODO LISTO» tras
   renderizar un fotograma de prueba. Si dice que falta ffmpeg o Node, lo
   instala con winget/brew; puede pedir cerrar y abrir la terminal y
   relanzarlo. Es idempotente: se puede lanzar siempre.
3. Lee `CLAUDE.md` (reglas del negocio y del contenido: mandan siempre) y
   `estudio/ESTUDIO.md` (qué hace que un vídeo funcione).
4. Plugins de Claude Code que usamos: **Remotion** (skills de Remotion) y
   **watch-video** (ver vídeos). Pablo los instaló en claude.ai; si en local no
   aparecen, instálalos con `/plugin` (marketplace de Anthropic). No son
   imprescindibles: el proyecto ya tiene todo el código.
5. Habla con Pablo en castellano, sin tecnicismos, con comparaciones de la
   vida real. No le hagas configurar nada que puedas hacer tú.
6. Al avanzar, actualiza este archivo («Diario», arriba lo último) y haz
   commit + push. Nunca subas `.env`.

## 1. Estado (15-10-2026)
- **Carruseles** temas 03–61, castellano y catalán: hechos y mejorados
  (portada con maqueta, fotos reales por sector). En `salida/<tema>/<idi>/carrusel/`.
  Solo para Instagram.
- **Facebook**: una imagen-resumen + texto por tema (`salida/<tema>/<idi>/facebook.png`,
  `salida/<tema>/FACEBOOK.md`). Entregado a Pablo ordenado (01, 02…).
- **Vídeos viejos** (motor Python, voz Azure): temas 03–61 y formatos
  busqueda, mito (20), plantilla, bienmal, montaje, pregunta, archivo. Se
  rehacen con el motor nuevo y la voz de Pablo cuando él diga.
- **Motor nuevo (Remotion)**: 3 pilotos que a Pablo le encantaron, sobre todo
  el antes/después («una barbaridad»). **Los vídeos nuevos tienen que salir
  igual que estos** → receta exacta en la sección 3.
- **Voz de Pablo**: la está clonando con VoiceStudio (IA en local). En cuanto
  tenga audios, sección 4. Probado el 15-10-2026 con un audio de prueba:
  100 % de palabras alineadas, vídeo idéntico al original.

### Lo siguiente (por orden, cuando Pablo lo pida)
1. Rehacer los 3 pilotos con su voz (sección 4) y hacerlos en catalán.
2. Más vídeos con el motor nuevo, sobre todo estilo **antes/después con webs
   grabadas de verdad**. Ideas ya habladas: «Busco X en [ciudad]» (ciudades de
   toda España), web en 48 h en cámara rápida, antes/después con barrido,
   «POV: eres un cliente…», mito con «¿Cuánto sabes de SEO?».
3. Pasar los temas 03–61 a vídeo con el motor nuevo y su voz.
4. Temas nuevos de carrusel: proponerlos antes (la lista de ideas está agotada).

---

## 2. Mapa del proyecto
| Qué | Dónde |
|---|---|
| Reglas del negocio y del contenido | `CLAUDE.md` |
| Estudio de vídeos que funcionan | `estudio/ESTUDIO.md` (+ hojas en `estudio/hojas/`) |
| Motor nuevo de vídeo (Remotion) | `remotion/` (código en `remotion/src/`) |
| Guiones de los vídeos nuevos | `remotion/guiones/<id>.json` |
| Preparar voz + datos + render | `herramientas/remo.py` |
| Voces de Pablo | `voces/<id>_<idioma>.mp3` (ver `voces/LEEME.md`) |
| Efectos de sonido | `herramientas/sonidos.py` → `remotion/public/sfx/` |
| Capturas de webs (para el móvil del vídeo) | `remotion/scripts/captura_web.mjs` |
| Webs de ejemplo inventadas | `webs_ejemplo/` |
| Carruseles (láminas) | `herramientas/carrusel.py`, textos en `carruseles/<tema>_<idi>.json` |
| Banco de fotos reales por sector | `fotos/<sector>/`, origen en `fotos/FUENTES.md`, `herramientas/banco_fotos.py` |
| Facebook | `herramientas/facebook.py`, `herramientas/paquete_facebook.py` |
| Motor viejo (vídeos con voz Azure, formatos) | `herramientas/hacer.py`, `formato.py`, `anima.py`, `voz.py`… |
| Todo lo entregable | `salida/` |
| Instalar todo | `herramientas/instalar.py` |

---

## 3. RECETA EXACTA de los vídeos nuevos (para que salgan igual)
El aspecto sale del código de `remotion/src/`: **no lo cambies** salvo que
Pablo pida algo. Para un vídeo nuevo se escribe un guion y, si es un formato
nuevo, una composición reutilizando las piezas de `remotion/src/comun/`.

### 3.1 Cómo se hace un vídeo (pasos)
1. **Guion** `remotion/guiones/<id>.json` (copiar uno de los 3 pilotos):
   - `id`, `idioma` (`es`/`ca`), `composicion` (`AntesDespues`, `Pregunta`, `Mito`),
     `aviso` (si hay datos/negocios de ejemplo).
   - `escenas`: lista con `tipo` (lo que dibuja), `voz` (la frase que se dice),
     y según el tipo `titulo`, `frase`, `rotulos` [`{"en": palabra, "texto": "RÓTULO", "color": "rojo|verde|blanco"}`]
     (el rótulo salta cuando se dice esa palabra), `pausa` (segundos de
     silencio tras la frase, p. ej. 3,2 para la cuenta atrás del mito).
   - La última escena es `cta` con `frase` (cierre con *resaltado*).
   - Catalán: copiar el guion a `remotion/guiones/<id>_ca.json` con
     `"idioma": "ca"` y el mismo `id`; traducir `voz`, `titulo`, `frase`,
     `rotulos` (sale en `salida/remotion/<id>/ca/`).
2. **Voz y render** (desde la raíz del repo):
   - Con la voz de Pablo: `python herramientas/remo.py remotion/guiones/<id>.json --audio voces/<id>_es.mp3`
   - Provisional sin su voz (Azure, necesita clave en la nube o `.env`):
     `python herramientas/remo.py remotion/guiones/<id>.json`
   - Deja `salida/remotion/<id>/<idioma>/video.mp4` + `guion_voz.txt` (texto
     que Pablo pasa a VoiceStudio) y la hoja `.tmp/revision/remotion/<id>_<idi>.jpg`.
   - `--solo-datos` = no renderiza (para ver en `cd remotion && npx remotion studio`).
3. **Revisar SIEMPRE antes de entregar**: la hoja de 12 fotogramas y, si
   algo dudoso, fotogramas sueltos (`ffmpeg -ss <s> -i video.mp4 -frames:v 1 x.png`).
   Nada cortado ni solapado, ninguna palabra sola en una línea, fotograma 0
   con el gancho ya visible.
4. **`PUBLICAR.md`** en `salida/remotion/<id>/` (texto, hashtags, aviso).
5. Commit + push, y entregar a Pablo (sección 6).

### 3.2 Estilo (ya está en el código; esto es para no romperlo)
- Vertical **1080×1920, 30 fps**, H.264; audio normalizado a **−16 LUFS**
  (lo hace `remo.py` con `loudnorm`).
- Colores: azul `#090f20`/`#14203f` (fondo con brillo que se mueve y rejilla
  de puntos), amarillo `#fbbe01`, rojo `#d63031`, verde `#25a35c`.
  Letra Montserrat (Black/ExtraBold) de `remotion/public/marca/`. Logo en
  `remotion/public/marca/logo.png`.
- **Gancho desde el fotograma 0**: la primera escena NO lleva fundido de
  entrada; se habla desde el segundo 0.
- **Algo cambia cada 2–4 s**: cambio de escena con zoom+desenfoque corto y
  «whoosh»; zooms de cámara (`Camara`) a lo que se dice; rótulos de palabra
  clave arriba con «pop» cuando se nombra la cosa.
- **Subtítulos**: 1–3 palabras, mayúsculas, Montserrat Black 88 px, contorno
  negro, la palabra que suena en amarillo; máx. 15 letras por línea (corta
  antes de una palabra que no cabe). En el gancho y en el cierre no hay
  subtítulos si el texto ya está en pantalla.
- **Imagen real**: webs dentro de un móvil (`Movil`) con capturas reales
  hechas con `captura_web.mjs` (ancho 390, ×2,5) y scroll; marcos de color
  sobre lo que importa (`Marco`), dedo que toca con clic (`Toque`), sellos
  ✓/✗ (`Sello`).
- **Efectos de sonido** propios (sintetizados, sin derechos) en
  `remotion/public/sfx/`, siempre con `<Sfx nombre=... volumen=...>`;
  **volumen general 0,85** (`VOLUMEN_EFECTOS` en `comun/marca.ts`: Pablo pidió
  −15 %). Whoosh 0,35 · pop 0,55 · clic 0,8 · acierto 0,5 · fallo 0,6 · tictac 0,7.
- **Cierre** (`Final`): logo, frase con *resaltado*, botón amarillo «Escríbeme
  por WhatsApp» que late, 641 27 74 95 y dissenywebpm.com; rótulos «DEMO
  GRATIS EN 48 H» / «TODA ESPAÑA» cuando se dicen.
- Guion: primera frase sobre el problema o el dinero del que mira (nunca
  sobre Pablo); frases cortas; nada de cifras inventadas; negocios de
  ejemplo inventados y avisados; ciudades de toda España; «estés donde estés».

### 3.3 Los 3 formatos que ya existen
- **AntesDespues** (`remotion/src/AntesDespues.tsx`, guion `antes_despues.json`):
  gancho con buscador escribiendo + dos móviles «1» y «2» → web vieja con
  zooms (letra diminuta, «Bienvenidos», sin teléfono) → pie de página → web
  nueva (qué y dónde, toque al botón de WhatsApp) → scroll → «Mismo pan» con
  ✗/✓ → cierre. Webs en `webs_ejemplo/panaderia/{vieja,nueva}/index.html`,
  capturas + cajas (`.json`) en `remotion/public/antes_despues/`. Para otro
  negocio: hacer dos webs de ejemplo nuevas, capturarlas con los selectores
  a marcar y ajustar las coordenadas CSS que usa la composición.
- **Pregunta** (`Pregunta.tsx`, `pregunta_maps.json`): pregunta de cliente en
  rótulo rojo fijo arriba (se entiende sin sonido) + lista de Maps animada +
  tarjetas; datos de Google con fuente real.
- **Mito** (`Mito.tsx`, `mito_seo.json`): «¿Cuánto sabes de SEO?», marcador
  de 3 arriba, frase + dibujo, botones MITO/VERDAD, cuenta atrás con tic-tac
  (`"pausa": 3.2`), sello ¡MITO!/¡VERDAD! con sonido y explicación (`"pausa": 0.9`
  en las respuestas), resultado y cierre. Preguntas sacadas de
  `planes/plan_mito.py` (ya comprobadas).
- Formato nuevo = nueva composición en `remotion/src/<Nombre>.tsx` con las
  piezas de `comun/` y registrarla en `remotion/src/Root.tsx` (con un
  `datos.json` de ejemplo de `remotion/public/<id>_es/`).

---

## 4. La voz de Pablo (VoiceStudio)
1. Pablo pasa a VoiceStudio el texto de `salida/remotion/<id>/<idioma>/guion_voz.txt`
   **entero, de principio a fin, en un solo audio** (cualquier formato: mp3,
   wav, m4a). No hace falta que deje pausas: `remo.py` las mete donde toca.
2. El audio va a `voces/<id>_<idioma>.mp3` (si te lo pasa por el chat, guárdalo
   tú ahí).
3. `python herramientas/remo.py remotion/guiones/<id>.json --audio voces/<id>_es.mp3`
   transcribe con faster-whisper (modelo `small`, CPU), alinea cada palabra
   con el guion (si la IA dice «cuarenta y ocho» por «48» lo reparte sin
   descuadrar) y monta el vídeo. Mira la línea «X % coinciden con el guion»:
   **≥ 90 % = bien**; si sale «OJO», el audio no es de ese guion.
4. Si algún día hay acceso al ordenador de VoiceStudio, automatizar el paso 1.

---

## 5. Carruseles, Facebook y fotos
- Láminas de un tema: `python herramientas/carrusel.py carruseles/<tema>_<idi>.json`
  (no toca la voz). Hoja de revisión: `python herramientas/hoja.py salida/<tema>/<idi>/carrusel <salida.jpg> 300`.
- Detalles del diseño mejorado: «Carruseles mejorados» en `CLAUDE.md`.
- Fotos: cada tema usa su sector (`SECTOR` en `carrusel.py`). Para un sector
  nuevo: `python herramientas/banco_fotos.py candidatos <sector>` (añadirlo
  antes a `SECTORES` con etiquetas de Mixkit), mirar `.tmp/banco/hoja_<sector>.jpg`
  y elegir a ojo con `... elige <sector> <id_n> ...`. Solo Mixkit con
  «Stock Video Free License» (el script lo comprueba). Pexels: no dan claves.
- Facebook de un tema: `python herramientas/facebook.py <tema>`; paquete
  ordenado para Pablo: `python herramientas/paquete_facebook.py <carpeta>`.

## 6. Entregar a Pablo
- Pablo trabaja desde el móvil. En la app de Claude (nube) los archivos se
  envían con un límite de **30 MB por archivo**: ZIPs sin comprimir (`zip -0`)
  partidos en trozos < 30 MB, ordenados y con nombres claros (01, 02…),
  nunca un montón de carpetas sin orden.
- En local: decirle la ruta exacta de la carpeta.
- Explicarle siempre qué hacer con lo entregado, en 3–4 pasos.

## 7. Trampas conocidas
- Desde la nube, YouTube no deja bajar vídeos y TikTok pide sesión (en el
  estudio se usaron subtítulos + storyboard: ver `estudio/ESTUDIO.md`). En
  local sí funciona watch-video con el vídeo entero.
- Render Remotion: ~2–3 min por vídeo de 40 s. En la nube usa el Chromium de
  `/opt/pw-browsers` (lo decide `remotion.config.ts` solo).
- `faster-whisper`: el audio se decodifica con ffmpeg en `remo.py` (la
  librería `av` de algunas versiones falla al abrir archivos).
- El repo pesa >1 GB (vídeos en `salida/`): clonar tarda.
- Voz Azure: en la nube la clave la inyecta el entorno; en local va en
  `.env` (`AZURE_SPEECH_KEY=...`, nunca se sube). Con la voz de Pablo no hace falta.

---

## Diario (lo último arriba)
- **15-10-2026** · Traspaso rehecho completo. `herramientas/instalar.py`
  (instalación automática + prueba), `requirements.txt`, carpeta `voces/`.
  Sincronización con voz propia mejorada (alineación palabra a palabra) y
  probada de punta a punta: 100 % de palabras, vídeo idéntico.
- **14-10-2026** · Facebook corregido: imagen-resumen + texto por tema
  (`herramientas/facebook.py`, 43 temas es/ca); carrusel solo para Instagram.
  Paquete ordenado (01, 02… imagen + .txt) entregado en ZIP por idioma.
- **14-10-2026** · Efectos −15 % y pilotos rehechos. Carruseles: banco de
  fotos reales (24 sectores, 124 fotos), portada nueva, antes/después con la
  misma foto; los 86 regenerados y revisados uno a uno.
- **14-10-2026** · Pilotos 2 y 3 hechos y revisados. Entregados los 3 a Pablo.
- **14-10-2026** · Piloto 1 (antes/después, panadería inventada de
  Valladolid) hecho y revisado.
- **14-10-2026** · Estudio hecho (`estudio/ESTUDIO.md`). Proyecto Remotion
  creado en `remotion/`.
- **14-10-2026** · Pablo instaló Remotion, watch-video y video-shotcraft.
