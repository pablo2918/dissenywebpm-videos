"""Pruebas de estilos con video de archivo (Pexels), idea sacada de
MoneyPrinterTurbo. Solo castellano de momento: es una prueba para comparar.
`buscar`: lo que se busca en Pexels (en ingles, que da mas resultados).
"""

VIDEOS = [
    # Estilo 1: video de archivo a pantalla completa + voz + subtitulos grandes
    {"id": "se_va_sin_decirlo", "estilo": "completo",
     "es": {"titulo": "Tu cliente se fue *y no te dijo por qué*",
            "tramos": [
                ("Tu cliente se fue a la competencia y no te dijo por qué. Te lo digo yo.", "woman looking at phone"),
                ("Te buscó en el móvil y no encontró tu teléfono a la vista.", "scrolling smartphone"),
                ("Quiso ver precios y solo ponía «consultar».", "confused woman phone"),
                ("Miró tus reseñas y no había ninguna reciente.", "reading phone cafe"),
                ("Y la web de al lado se entendía a la primera.", "happy customer smartphone"),
                ("Arreglarlo es más fácil de lo que crees. Escríbeme por WhatsApp.", "small business owner shop")],
            "final": "¿Lo arreglamos?"}},
    # Estilo 2: «Mito o verdad» con video de fondo (mismas preguntas que el 06)
    {"id": "mito_con_fondo", "estilo": "mito", "mito": 6,
     "buscar": ["shop owner phone", "city street night", "restaurant review phone"]},
    # Estilo 3: pantalla partida: video arriba, tarjetas abajo, con voz
    {"id": "tres_cosas", "estilo": "partido",
     "es": {"titulo": "3 cosas que tu web *tiene que tener*",
            "gancho": ("Tres cosas que tu web tiene que tener, sí o sí.", "laptop website design"),
            "puntos": [
                ("Qué haces y dónde", "Arriba del todo, qué haces y dónde. Sin rodeos.", "shop front street"),
                ("Un botón para escribirte", "Un botón para escribirte por WhatsApp con un toque.", "texting smartphone"),
                ("Fotos reales", "Fotos reales de tu trabajo, no de catálogo.", "craftsman working")],
            "cierre": ("¿La tuya las tiene? Escríbeme por WhatsApp.", "person smiling phone"),
            "final": "¿La tuya las tiene?"}},
]
