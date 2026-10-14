"""Pruebas de estilos con video de archivo (Pexels), idea sacada de
MoneyPrinterTurbo. Solo castellano de momento: es una prueba para comparar.
Cada plano es un numero de clip de Mixkit (elegido a ojo, licencia gratuita)
o un texto para buscar en Pexels (si algun dia hay clave).
"""

VIDEOS = [
    # Estilo 1: video de archivo a pantalla completa + voz + subtitulos grandes
    {"id": "se_va_sin_decirlo", "estilo": "completo",
     "es": {"titulo": "Tu cliente se fue *y no te dijo por qué*",
            "tramos": [
                ("Tu cliente se fue a la competencia y no te dijo por qué. Te lo digo yo.", 43270),
                ("Te buscó en el móvil y no encontró tu teléfono a la vista.", 4915),
                ("Quiso ver precios y solo ponía «consultar».", 144),
                ("Miró tus reseñas y no había ninguna reciente.", 49137),
                ("Y la web de al lado se entendía a la primera.", 39782),
                ("Arreglarlo es más fácil de lo que crees. Escríbeme por WhatsApp.", 43241)],
            "final": "¿Lo arreglamos?"}},
    # Estilo 2: «Mito o verdad» con video de fondo (mismas preguntas que el 06)
    {"id": "mito_con_fondo", "estilo": "mito", "mito": 6,
     "buscar": [4672, 4231, 15914]},
    # Estilo 3: pantalla partida: video arriba, tarjetas abajo, con voz
    {"id": "tres_cosas", "estilo": "partido",
     "es": {"titulo": "3 cosas que tu web *tiene que tener*",
            "gancho": ("Tres cosas que tu web tiene que tener, sí o sí.", 1781),
            "puntos": [
                ("Qué haces y dónde", "Arriba del todo, qué haces y dónde. Sin rodeos.", 29050),
                ("Un botón para escribirte", "Un botón para escribirte por WhatsApp con un toque.", 41165),
                ("Fotos reales", "Fotos reales de tu trabajo, no de catálogo.", 39500)],
            "cierre": ("¿La tuya las tiene? Escríbeme por WhatsApp.", 4805),
            "final": "¿La tuya las tiene?"}},
]
