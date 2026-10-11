"""Formato «Una web montándose sola»: CON voz y subtitulos.
Un movil en el que la web se va construyendo: cada paso de la voz anade una
pieza (y la marca en amarillo). Negocios inventados («Fulanito»).
pasos: (etiqueta del paso, lo que dice la voz, pieza)
Piezas: portada, boton, lista, fotos, donde, resenas, zonas.
"""


def portada(t, s, foto=0):
    return {"tipo": "portada", "titulo": t, "sub": s, "foto": foto}


def boton(t):
    return {"tipo": "boton", "texto": t}


def lista(t, filas):
    return {"tipo": "lista", "titulo": t, "filas": filas}


def fotos(t, et):
    return {"tipo": "fotos", "titulo": t, "etiquetas": et}


def donde(t, dir_, horas):
    return {"tipo": "donde", "titulo": t, "direccion": dir_, "horas": horas}


def resenas(t, nota, texto, nombre):
    return {"tipo": "resenas", "titulo": t, "nota": nota, "texto": texto, "nombre": nombre}


def zonas(t, z):
    return {"tipo": "zonas", "titulo": t, "zonas": z}


VIDEOS = [
    {"id": "restaurante",
     "es": {"negocio": "Can Fulanito", "dominio": "canfulanito.com",
            "titulo": "Así se monta una web que *trae clientes*",
            "gancho": "Así se monta una web que trae clientes. Paso a paso.",
            "pasos": [
                ("Qué y dónde", "Arriba del todo, qué eres y dónde: cocina de mercado en Girona.",
                 portada("Cocina de mercado en Girona", "Menú de mediodía y carta de temporada.")),
                ("El botón", "Justo debajo, un botón para reservar por WhatsApp. Sin buscarlo.",
                 boton("Reserva por WhatsApp")),
                ("La carta", "La carta, escrita en la web. Se lee en el móvil sin descargar nada.",
                 lista("La carta", [("Croquetas de la casa", "8 €"), ("Arroz de temporada", "16 €"),
                                    ("Crema catalana", "6 €")])),
                ("Fotos", "Fotos de verdad: los platos y el comedor.",
                 fotos("El restaurante", ["Platos", "Comedor", "Terraza", "Cocina"])),
                ("Dónde y cuándo", "Y al final, dónde estás y a qué hora abres.",
                 donde("Dónde estamos", "Carrer Major, 12 · Girona", ["Mar–Dom · 13:00–16:00", "Vie–Sáb · 20:00–23:00"]))],
            "cierre": "¿Quieres la tuya? Escríbeme por WhatsApp.",
            "final": "¿Montamos la de tu restaurante?"},
     "ca": {"negocio": "Can Fulanito", "dominio": "canfulanito.cat",
            "titulo": "Així es munta una web que *porta clients*",
            "gancho": "Així es munta una web que porta clients. Pas a pas.",
            "pasos": [
                ("Què i on", "A dalt de tot, què ets i on: cuina de mercat a Girona.",
                 portada("Cuina de mercat a Girona", "Menú de migdia i carta de temporada.")),
                ("El botó", "Just a sota, un botó per reservar per WhatsApp. Sense buscar-lo.",
                 boton("Reserva per WhatsApp")),
                ("La carta", "La carta, escrita a la web. Es llegeix al mòbil sense descarregar res.",
                 lista("La carta", [("Croquetes de la casa", "8 €"), ("Arròs de temporada", "16 €"),
                                    ("Crema catalana", "6 €")])),
                ("Fotos", "Fotos de veritat: els plats i el menjador.",
                 fotos("El restaurant", ["Plats", "Menjador", "Terrassa", "Cuina"])),
                ("On i quan", "I al final, on ets i a quina hora obres.",
                 donde("On som", "Carrer Major, 12 · Girona", ["Dt–Dg · 13:00–16:00", "Dv–Ds · 20:00–23:00"]))],
            "cierre": "Vols la teva? Escriu-me per WhatsApp.",
            "final": "Muntem la del teu restaurant?"}},
    {"id": "electricista",
     "es": {"negocio": "Electricidad Fulanito", "dominio": "electricidadfulanito.com",
            "titulo": "La web de un *electricista*, pieza a pieza",
            "gancho": "Te monto la web de un electricista delante de ti. Mira.",
            "pasos": [
                ("Qué y dónde", "Primero, qué haces y dónde: electricista en Girona.",
                 portada("Electricista en Girona", "Averías, boletines e instalaciones.", 1)),
                ("El botón", "Un botón grande para escribirte. Quien tiene una avería no quiere buscar.",
                 boton("Escríbenos por WhatsApp")),
                ("Servicios", "Qué trabajos haces, en una lista que se entiende.",
                 lista("Servicios", [("Averías y urgencias", ""), ("Boletines eléctricos", ""),
                                     ("Instalaciones nuevas", "")])),
                ("Zonas", "Los pueblos donde trabajas. Así te encuentran los de tu zona.",
                 zonas("Trabajamos en", ["Girona", "Salt", "Sarrià", "Celrà", "Quart"])),
                ("Reseñas", "Y lo que dicen tus clientes, que vende más que cualquier frase.",
                 resenas("Opiniones", "4,9", "Vino el mismo día y lo dejó todo perfecto.", "Anna R."))],
            "cierre": "¿Hacemos la tuya? Escríbeme por WhatsApp.",
            "final": "¿Hacemos la de tu negocio?"},
     "ca": {"negocio": "Electricitat Fulanito", "dominio": "electricitatfulanito.cat",
            "titulo": "La web d'un *electricista*, peça a peça",
            "gancho": "Et munto la web d'un electricista davant teu. Mira.",
            "pasos": [
                ("Què i on", "Primer, què fas i on: electricista a Girona.",
                 portada("Electricista a Girona", "Avaries, butlletins i instal·lacions.", 1)),
                ("El botó", "Un botó gran per escriure't. Qui té una avaria no vol buscar.",
                 boton("Escriu-nos per WhatsApp")),
                ("Serveis", "Quines feines fas, en una llista que s'entén.",
                 lista("Serveis", [("Avaries i urgències", ""), ("Butlletins elèctrics", ""),
                                   ("Instal·lacions noves", "")])),
                ("Zones", "Els pobles on treballes. Així et troben els de la teva zona.",
                 zonas("Treballem a", ["Girona", "Salt", "Sarrià", "Celrà", "Quart"])),
                ("Ressenyes", "I el que diuen els teus clients, que ven més que qualsevol frase.",
                 resenas("Opinions", "4,9", "Va venir el mateix dia i ho va deixar tot perfecte.", "Anna R."))],
            "cierre": "Fem la teva? Escriu-me per WhatsApp.",
            "final": "Fem la del teu negoci?"}},
    {"id": "peluqueria",
     "es": {"negocio": "Peluquería Fulanito", "dominio": "peluqueriafulanito.com",
            "titulo": "Una web de *peluquería* que llena la agenda",
            "gancho": "Una web de peluquería que llena la agenda. Pieza a pieza.",
            "pasos": [
                ("Qué y dónde", "Arriba: peluquería en Salt. Sin «Bienvenidos», al grano.",
                 portada("Peluquería en Salt", "Cortes, color y peinados.", 3)),
                ("Precios", "Precios orientativos. Quien sabe lo que cuesta, se anima antes.",
                 lista("Precios", [("Corte", "desde 15 €"), ("Color", "desde 35 €"), ("Peinado", "desde 20 €")])),
                ("Trabajos", "Fotos de tus trabajos. Es lo que más miran.",
                 fotos("Nuestros trabajos", ["Corte", "Color", "Mechas", "Peinado"])),
                ("Reseñas", "Las opiniones de tus clientas, para dar confianza.",
                 resenas("Opiniones", "4,8", "Me encanta cómo me deja el pelo. Muy atentas.", "Laia M.")),
                ("El botón", "Y un botón para pedir hora por WhatsApp. Que no se te escape nadie.",
                 boton("Pide hora por WhatsApp"))],
            "cierre": "¿Te monto la tuya? Escríbeme por WhatsApp.",
            "final": "¿Te monto la de tu peluquería?"},
     "ca": {"negocio": "Perruqueria Fulanito", "dominio": "perruqueriafulanito.cat",
            "titulo": "Una web de *perruqueria* que omple l'agenda",
            "gancho": "Una web de perruqueria que omple l'agenda. Peça a peça.",
            "pasos": [
                ("Què i on", "A dalt: perruqueria a Salt. Sense «Benvinguts», al gra.",
                 portada("Perruqueria a Salt", "Talls, color i pentinats.", 3)),
                ("Preus", "Preus orientatius. Qui sap què costa, s'anima abans.",
                 lista("Preus", [("Tall", "des de 15 €"), ("Color", "des de 35 €"), ("Pentinat", "des de 20 €")])),
                ("Feines", "Fotos de les teves feines. És el que més miren.",
                 fotos("Les nostres feines", ["Tall", "Color", "Metxes", "Pentinat"])),
                ("Ressenyes", "Les opinions de les teves clientes, per donar confiança.",
                 resenas("Opinions", "4,8", "M'encanta com em deixa els cabells. Molt atentes.", "Laia M.")),
                ("El botó", "I un botó per demanar hora per WhatsApp. Que no se t'escapi ningú.",
                 boton("Demana hora per WhatsApp"))],
            "cierre": "Et munto la teva? Escriu-me per WhatsApp.",
            "final": "Et munto la de la teva perruqueria?"}},
    {"id": "yoga",
     "es": {"negocio": "Yoga Fulanito", "dominio": "yogafulanito.com",
            "titulo": "Lo que necesita la web de un *centro de yoga*",
            "gancho": "Lo que necesita la web de un centro de yoga. Ni más, ni menos.",
            "pasos": [
                ("Qué y dónde", "Qué ofreces y dónde: yoga en el centro de Girona.",
                 portada("Yoga en el centro de Girona", "Grupos reducidos, todos los niveles.", 4)),
                ("Horarios", "Los horarios de las clases, claros. Es lo primero que preguntan.",
                 lista("Clases", [("Lunes y miércoles", "19:00"), ("Martes y jueves", "9:30"), ("Sábado", "10:00")])),
                ("Precios", "Cuánto cuesta. Sin tener que escribir para saberlo.",
                 lista("Tarifas", [("Clase suelta", "12 €"), ("Bono 10 clases", "100 €")])),
                ("Dónde", "Dónde estáis, con el mapa, para llegar sin perderse.",
                 donde("Dónde estamos", "Plaça del Vi, 3 · Girona", ["Lun–Sáb"])),
                ("El botón", "Y un botón para reservar plaza por WhatsApp.",
                 boton("Reserva tu plaza por WhatsApp"))],
            "cierre": "¿Hacemos la tuya? Escríbeme por WhatsApp.",
            "final": "¿Hacemos la de tu centro?"},
     "ca": {"negocio": "Ioga Fulanito", "dominio": "iogafulanito.cat",
            "titulo": "El que necessita la web d'un *centre de ioga*",
            "gancho": "El que necessita la web d'un centre de ioga. Ni més, ni menys.",
            "pasos": [
                ("Què i on", "Què ofereixes i on: ioga al centre de Girona.",
                 portada("Ioga al centre de Girona", "Grups reduïts, tots els nivells.", 4)),
                ("Horaris", "Els horaris de les classes, clars. És el primer que pregunten.",
                 lista("Classes", [("Dilluns i dimecres", "19:00"), ("Dimarts i dijous", "9:30"), ("Dissabte", "10:00")])),
                ("Preus", "Quant costa. Sense haver d'escriure per saber-ho.",
                 lista("Tarifes", [("Classe solta", "12 €"), ("Bo 10 classes", "100 €")])),
                ("On", "On sou, amb el mapa, per arribar-hi sense perdre's.",
                 donde("On som", "Plaça del Vi, 3 · Girona", ["Dl–Ds"])),
                ("El botó", "I un botó per reservar plaça per WhatsApp.",
                 boton("Reserva la teva plaça per WhatsApp"))],
            "cierre": "Fem la teva? Escriu-me per WhatsApp.",
            "final": "Fem la del teu centre?"}},
    {"id": "carniceria",
     "es": {"negocio": "Carnicería Fulanito", "dominio": "carniceriafulanito.com",
            "titulo": "Una web para una *tienda de barrio*, sin complicaciones",
            "gancho": "Una web para una tienda de barrio. Sencilla y que funciona.",
            "pasos": [
                ("Qué y dónde", "Qué vendes y dónde: carnicería en el barrio de Santa Eugènia.",
                 portada("Carnicería en Santa Eugènia", "Carne de proximidad y elaborados de la casa.", 5)),
                ("Productos", "Fotos de lo que tienes en el mostrador.",
                 fotos("En el mostrador", ["Ternera", "Cerdo", "Pollo", "Elaborados"])),
                ("Encargos", "Un botón para hacer encargos por WhatsApp. Llegan y lo tienen listo.",
                 boton("Haz tu encargo por WhatsApp")),
                ("Horario", "El horario, bien visible. Nadie quiere encontrarse la persiana bajada.",
                 donde("Horario", "Carrer de Santa Eugènia, 40 · Girona", ["Lun–Vie · 8:00–14:00 y 17:00–20:00", "Sáb · 8:00–14:00"])),
                ("Reseñas", "Y lo que dicen tus clientes de toda la vida.",
                 resenas("Opiniones", "4,9", "Producto buenísimo y siempre con una sonrisa.", "Montse P."))],
            "cierre": "¿Te monto la tuya? Escríbeme por WhatsApp.",
            "final": "¿Te monto la de tu tienda?"},
     "ca": {"negocio": "Carnisseria Fulanito", "dominio": "carnisseriafulanito.cat",
            "titulo": "Una web per a una *botiga de barri*, sense complicacions",
            "gancho": "Una web per a una botiga de barri. Senzilla i que funciona.",
            "pasos": [
                ("Què i on", "Què vens i on: carnisseria al barri de Santa Eugènia.",
                 portada("Carnisseria a Santa Eugènia", "Carn de proximitat i elaborats de la casa.", 5)),
                ("Productes", "Fotos del que tens al taulell.",
                 fotos("Al taulell", ["Vedella", "Porc", "Pollastre", "Elaborats"])),
                ("Encàrrecs", "Un botó per fer encàrrecs per WhatsApp. Arriben i ho tenen a punt.",
                 boton("Fes el teu encàrrec per WhatsApp")),
                ("Horari", "L'horari, ben visible. Ningú no vol trobar-se la persiana abaixada.",
                 donde("Horari", "Carrer de Santa Eugènia, 40 · Girona", ["Dl–Dv · 8:00–14:00 i 17:00–20:00", "Ds · 8:00–14:00"])),
                ("Ressenyes", "I el que diuen els teus clients de tota la vida.",
                 resenas("Opinions", "4,9", "Producte boníssim i sempre amb un somriure.", "Montse P."))],
            "cierre": "Et munto la teva? Escriu-me per WhatsApp.",
            "final": "Et munto la de la teva botiga?"}},
]

PIE = {
    "es": ("Así se monta una web que trae clientes, pieza a pieza 👇\n\n"
           "Te hago una demo gratis de la tuya en 48 h. Escríbeme por WhatsApp: 641 27 74 95",
           "#paginaweb #negocioslocales #girona #diseñoweb #webparanegocios"),
    "ca": ("Així es munta una web que porta clients, peça a peça 👇\n\n"
           "Et faig una demo gratis de la teva en 48 h. Escriu-me per WhatsApp: 641 27 74 95",
           "#paginaweb #comerçlocal #girona #dissenyweb #webpernegocis"),
}
