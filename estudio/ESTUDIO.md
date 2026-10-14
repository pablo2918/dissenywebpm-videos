# Estudio de vídeos que funcionan (14-10-2026)

## Cómo se hizo (para repetirlo)
- YouTube bloquea descargar vídeo desde la nube («confirma que no eres un bot»)
  y TikTok pide iniciar sesión. Lo que SÍ se puede bajar sin cuenta:
  - **subtítulos automáticos con tiempo por palabra** (`--write-auto-subs`),
  - **storyboard** (`-f sb0`: una miniatura por segundo; basta para ver el
    ritmo de cortes y qué sale en pantalla).
- Scripts: `estudio/coge.sh <ids>` (baja subtítulos + storyboard + info),
  `estudio/saca.py` (saca las imágenes del .mhtml), `estudio/analiza.py`
  (palabras/segundo, qué dice en 0–3 s y 3–8 s, hoja de miniaturas).
- Lista de shorts de un canal con visitas: 
  `yt-dlp --flat-playlist --print "%(view_count)s|%(url)s|%(title)s" "https://www.youtube.com/@CANAL/shorts"`
  → comparar los MÁS vistos con los MENOS vistos del mismo canal (mismo
  creador, mismo público: lo que cambia es el vídeo).
- Buscar en YouTube por palabras devuelve sobre todo anuncios pagados (Wix,
  GoDaddy…): no sirven para aprender. Mejor ir canal por canal.
- En el ordenador de Pablo (sin bloqueo) se puede usar el plugin
  watch-video con el vídeo entero.

## Vídeos estudiados (hojas en `estudio/hojas/`)
| Vídeo | Visitas | Qué es |
|---|---|---|
| Luis R. Silva «Cómo crear una página web para negocio» (6yrAoqVn_QA) | 2,5 M | Cara + capturas de pantalla, en español, MISMO nicho |
| Luis R. Silva «Cómo hacer una web en 2026» (rjlKSXLs8xs) | 903 k | Cara + rótulos grandes «DOMINIO», «HOSTING» |
| Luis R. Silva «Tu sitio web profesional listo» (naS13Uz0QLA) | 181 k | Pregunta directa al negocio |
| Luis R. Silva «Antes de crear un sitio web» (Daz4XYAI34o) | 22 k | Empieza «Adrián pregunta…» |
| Luis R. Silva «Rediseño web en vivo» (jxoZnZdzkDM) | 447 | Empieza «Yo quisiera ayudarte, David…» |
| Alex Hormozi «Why do my employees leave?» (XvCcbm9kxuY) | 2 M | Pregunta real de una dueña de salón, rótulo rojo arriba |
| Vilma Núñez «¿Por qué tu negocio digital no despega?» (wXIWB3rs2iw) | 1,1 M | Escenario + planos de recurso (dinero, persona pensando) |
| Flux «Creative 3D website» (JaCVPmyDf6s) | 169 k | Pantalla partida: cara arriba, web abajo |
| Flux «This portfolio isn't good enough» (K_XaPafYR6c) | 34 k | Revisión de una web: cara arriba, web abajo |
| Sterling Sky (SEO local) «Postcard verification MIA» (VYYguw2whnE) | 20 k | Experto en Maps, noticia de Google, imágenes-metáfora |
| Lokuma «Rebuilt a pizza truck's website» (cRfFpBDTE_Y) | 46 k | Antes/después de una web, sin cara (es anuncio) |
| The Futur «Talk about money first» · Kevin Powell «border-radius» | 152 k · 249 k | Opinión fuerte · truco en pantalla |

## Lo que aprendemos (y qué cambia en nuestros vídeos)
1. **Se habla desde el fotograma 0.** Todos empiezan a hablar antes de 0,5 s.
   Nada de entrada lenta ni logo al principio.
2. **La primera frase habla del problema o del dinero DEL QUE MIRA, no del creador.**
   - 2,5 M: «Debes saber esto **antes de pagarle a alguien** por hacer la página web de tu negocio».
   - 903 k: «**Ojo**: una página web que te ayuda a conseguir clientes necesita…».
   - 181 k: «¿Tu negocio todavía no tiene un sitio web profesional?».
   - 22 k: «Adrián pregunta…» · 447: «Yo quisiera ayudarte, David…» → mismo
     creador, mismo tema, pero la frase va de otro → se hunde.
   - Otros que funcionan: autoridad («El mismísimo CEO de Google dijo…»),
     situación reconocible («Si usas tu ficha de Google últimamente, habrás
     notado que…»), opinión fuerte («Sinceramente, no puedes tener una web así en 2026»).
3. **Ritmo de voz: 2,7–3,6 palabras por segundo** (rápido, sin pausas).
4. **Algo cambia en pantalla cada 2–4 s**: cara → captura → rótulo → cara.
   Los rótulos de palabra clave salen ARRIBA, grandes, cuando se nombra la
   cosa («DOMINIO», «HOSTING», «SPAM», «ABSENT»).
5. **Subtítulos de 1–3 palabras**, en el centro, siempre.
6. **Imágenes-metáfora**: el experto de Maps pone una chincheta de «SPAM» sobre
   un mapa, una montaña de papel cuando dice «papel»… Lo dicho se VE.
7. **Pantalla partida** (arriba quien habla, abajo la web que se revisa) es el
   formato de «revisión de webs» que funciona.
8. **Pregunta de cliente real como título** (rótulo rojo con la pregunta
   entre comillas, Hormozi) = gancho escrito que se entiende sin sonido.
9. **Temas que tiran**: dinero y miedo a que te timen («antes de pagar»),
   novedades de Google (con fuente real), «lo que nadie te dice».
10. **Casi todos los que funcionan llevan cara**. Lo sin cara que tiene muchas
    visitas en esta muestra es publicidad pagada. → Con la voz clonada de Pablo
    se gana naturalidad; si algún día graba 5–10 clips cortos de su cara
    (señalando, asintiendo, mirando el móvil) se pueden reutilizar en muchos
    vídeos. NO pedírselo: solo proponerlo si sale el tema.

## Qué aplicar en los vídeos nuevos (motor Remotion)
- Gancho: primera frase sobre el problema/dinero del que mira + rótulo
  grande desde el fotograma 0 + voz desde el fotograma 0.
- Cambio visual cada 2–4 s; rótulos de palabra clave arriba; efecto de
  sonido en cada cambio (whoosh, pop, clic).
- Imagen REAL de pantalla: grabar webs de ejemplo (y dissenywebpm.com) con
  Playwright haciendo scroll en un móvil, en vez de clips de archivo genéricos.
- Formatos piloto: (1) antes/después de una web con grabación real de
  pantalla, (2) pregunta de cliente con rótulo rojo y respuesta con
  gráficos, (3) mito o verdad 2.0 con «¿Cuánto sabes de SEO?» y marcador.
- Ojo: Pablo ya publicó «pregunta esto antes de pagar» (su 20): el gancho
  «antes de pagar» se puede usar, pero con contenido distinto.
