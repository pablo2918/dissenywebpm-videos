"""Formato «Mito o verdad»: SIN voz (la musica se pone desde la app).
3 preguntas por video. Cada una: la frase, 3 s para pensar, la respuesta y
UNA linea corta con el porque.
Cada pregunta: (verdad, {"es": (frase, porque), "ca": (frase, porque)})
"""

V, M = True, False

VIDEOS = [
    {"id": "texto_pueblo_resenas",
     "final": {"es": "¿Quieres una web que se entienda a la primera?",
               "ca": "Vols una web que s'entengui a la primera?"},
     "preguntas": [
         (M, {"es": ("Cuanto más texto tenga mi web, mejor.", "En el móvil, nadie lee párrafos largos."),
              "ca": ("Com més text tingui la meva web, millor.", "Al mòbil, ningú llegeix paràgrafs llargs.")}),
         (V, {"es": ("Tu web tiene que decir en qué pueblo estás.", "Quien busca, busca cerca."),
              "ca": ("La teva web ha de dir a quin poble ets.", "Qui busca, busca a prop.")}),
         (M, {"es": ("Responder a las reseñas no sirve de nada.", "Las respuestas las leen tus próximos clientes."),
              "ca": ("Respondre les ressenyes no serveix de res.", "Les respostes les llegeixen els teus pròxims clients.")})]},
    {"id": "bonita_precios_jovenes",
     "final": {"es": "¿Quieres una web clara y que venda?",
               "ca": "Vols una web clara i que vengui?"},
     "preguntas": [
         (M, {"es": ("Una web bonita ya vende sola.", "Sin teléfono a la vista, no te llaman."),
              "ca": ("Una web bonica ja ven sola.", "Sense telèfon a la vista, no et truquen.")}),
         (V, {"es": ("Poner precios orientativos ayuda a vender.", "Quien sabe lo que cuesta, se anima antes."),
              "ca": ("Posar preus orientatius ajuda a vendre.", "Qui sap què costa, s'anima abans.")}),
         (M, {"es": ("Las webs solo las miran los jóvenes.", "Gente de todas las edades busca en el móvil."),
              "ca": ("Les webs només les miren els joves.", "Gent de totes les edats busca al mòbil.")})]},
    {"id": "pagina_bienvenidos_whatsapp",
     "final": {"es": "¿Quieres una web sencilla y que funcione?",
               "ca": "Vols una web senzilla i que funcioni?"},
     "preguntas": [
         (V, {"es": ("Mejor una página clara que diez vacías.", "Lo vacío da sensación de abandono."),
              "ca": ("Millor una pàgina clara que deu de buides.", "El que és buit fa sensació d'abandonament.")}),
         (M, {"es": ("Empezar con “Bienvenidos” queda más cercano.", "Mejor decir qué haces y dónde."),
              "ca": ("Començar amb “Benvinguts” és més proper.", "Millor dir què fas i on.")}),
         (V, {"es": ("Un botón de WhatsApp es mejor que un formulario largo.", "Un toque y te escriben. Sin rellenar nada."),
              "ca": ("Un botó de WhatsApp és millor que un formulari llarg.", "Un toc i t'escriuen. Sense omplir res.")})]},
    {"id": "musica_horario_informatica",
     "final": {"es": "¿Quieres una web sin complicarte?",
               "ca": "Vols una web sense complicar-te?"},
     "preguntas": [
         (M, {"es": ("Música y animaciones hacen tu web más profesional.", "Solo la hacen más lenta en el móvil."),
              "ca": ("Música i animacions fan la teva web més professional.", "Només la fan més lenta al mòbil.")}),
         (V, {"es": ("El horario de tu ficha de Google tiene que estar bien.", "Si pone «cerrado», no vienen."),
              "ca": ("L'horari de la teva fitxa de Google ha d'estar bé.", "Si hi posa «tancat», no vénen.")}),
         (M, {"es": ("Para tener web hay que saber de informática.", "Me cuentas tu negocio y yo me encargo."),
              "ca": ("Per tenir web s'ha de saber d'informàtica.", "M'expliques el teu negoci i jo me n'encarrego.")})]},
    {"id": "fotos_idiomas_cambios",
     "final": {"es": "¿Hacemos la web de tu negocio?",
               "ca": "Fem la web del teu negoci?"},
     "preguntas": [
         (V, {"es": ("Las fotos de tu móvil pueden valer para tu web.", "Con buena luz, mejor que las de catálogo."),
              "ca": ("Les fotos del teu mòbil poden servir per a la web.", "Amb bona llum, millor que les de catàleg.")}),
         (M, {"es": ("Una web hay que tocarla cada semana.", "Bien hecha, con un cambio al mes basta."),
              "ca": ("Una web s'ha de tocar cada setmana.", "Ben feta, amb un canvi al mes n'hi ha prou.")}),
         (V, {"es": ("Una web en catalán y castellano llega a más gente.", "Cada cliente la lee en su idioma."),
              "ca": ("Una web en català i castellà arriba a més gent.", "Cada client la llegeix en el seu idioma.")})]},
]

PIE = {
    "es": ("¿Mito o verdad? Tres preguntas: dime en comentarios cuántas has acertado 👇\n\n"
           "¿Quieres una web clara para tu negocio? Escríbeme por WhatsApp: 641 27 74 95",
           "#mitooverdad #paginaweb #negocioslocales #girona #diseñoweb"),
    "ca": ("Mite o veritat? Tres preguntes: digues-me als comentaris quantes n'has encertat 👇\n\n"
           "Vols una web clara per al teu negoci? Escriu-me per WhatsApp: 641 27 74 95",
           "#miteoveritat #paginaweb #comerçlocal #girona #dissenyweb"),
}
