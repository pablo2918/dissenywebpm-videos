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

def q(v, es, ca):
    return (v, {"es": es, "ca": ca})


F_FICHA = {"es": "¿Te dejo la ficha de Google bien montada?", "ca": "Et deixo la fitxa de Google ben muntada?"}
F_WEB = {"es": "¿Quieres una web bien hecha desde el principio?", "ca": "Vols una web ben feta des del principi?"}
F_RES = {"es": "¿Quieres más reseñas y una ficha que dé confianza?", "ca": "Vols més ressenyes i una fitxa que doni confiança?"}

# 06–20: mas dificiles (cosas que mucha gente cree al reves). Solo hechos comprobables.
VIDEOS += [
    {"id": "nombre_distancia_estrellas", "final": F_FICHA, "preguntas": [
        q(M, ("Poner tu pueblo en el nombre de la ficha te ayuda a salir.", "Va contra las normas de Google: te la pueden suspender."),
             ("Posar el teu poble al nom de la fitxa t'ajuda a sortir.", "Va contra les normes de Google: te la poden suspendre.")),
        q(V, ("En Google Maps, la distancia influye en quién sale primero.", "Google mira relevancia, distancia y popularidad."),
             ("A Google Maps, la distància influeix en qui surt primer.", "Google mira rellevància, distància i popularitat.")),
        q(V, ("Las reseñas con solo estrellas, sin texto, también cuentan.", "Suman a tu nota, aunque con texto convencen más."),
             ("Les ressenyes només amb estrelles, sense text, també compten.", "Sumen a la teva nota, tot i que amb text convencen més."))]},
    {"id": "cafe_movil_cookies", "final": F_WEB, "preguntas": [
        q(M, ("Regalar un café a cambio de una reseña está permitido.", "Google prohíbe dar nada a cambio de reseñas."),
             ("Regalar un cafè a canvi d'una ressenya està permès.", "Google prohibeix donar res a canvi de ressenyes.")),
        q(V, ("Google mira primero cómo se ve tu web en el móvil.", "Usa la versión de móvil para colocarte."),
             ("Google mira primer com es veu la teva web al mòbil.", "Fa servir la versió de mòbil per col·locar-te.")),
        q(M, ("Toda web tiene que llevar el cartel de cookies.", "Solo si usa cookies que no son imprescindibles."),
             ("Tota web ha de portar el cartell de galetes.", "Només si fa servir galetes que no són imprescindibles."))]},
    {"id": "borrar_https_whatsapp", "final": F_WEB, "preguntas": [
        q(M, ("Si una reseña mala no te gusta, puedes borrarla.", "Solo se quita si incumple las normas de Google."),
             ("Si una ressenya dolenta no t'agrada, la pots esborrar.", "Només es treu si incompleix les normes de Google.")),
        q(V, ("Una web con https cuenta más para Google que una sin él.", "Google lo tiene en cuenta, y sin él el navegador avisa."),
             ("Una web amb https compta més per a Google que una sense.", "Google ho té en compte, i sense el navegador avisa.")),
        q(M, ("Para poner un botón de WhatsApp en tu web necesitas WhatsApp Business.", "Funciona también con el WhatsApp normal."),
             ("Per posar un botó de WhatsApp a la web necessites WhatsApp Business.", "També funciona amb el WhatsApp normal."))]},
    {"id": "categoria_aviso_traducir", "final": F_FICHA, "preguntas": [
        q(M, ("En tu ficha de Google solo puedes elegir una categoría.", "Hay una principal y puedes añadir otras."),
             ("A la fitxa de Google només pots triar una categoria.", "N'hi ha una de principal i en pots afegir d'altres.")),
        q(V, ("La web de un negocio tiene que llevar aviso legal.", "Lo pide la ley: quién eres y cómo contactarte."),
             ("La web d'un negoci ha de portar avís legal.", "Ho demana la llei: qui ets i com contactar-te.")),
        q(V, ("Google puede traducir tus reseñas a otros idiomas.", "Un turista las lee en el suyo."),
             ("Google pot traduir les teves ressenyes a altres idiomes.", "Un turista les llegeix en el seu."))]},
    {"id": "repetir_respuesta_categoria", "final": F_RES, "preguntas": [
        q(M, ("Repetir mucho “fontanero Girona” en tu web te sube en Google.", "Google lo detecta y te puede bajar."),
             ("Repetir molt “lampista Girona” a la web et puja a Google.", "Google ho detecta i et pot baixar.")),
        q(V, ("La categoría de tu ficha influye en cuándo sales.", "Google la usa para saber a qué te dedicas."),
             ("La categoria de la fitxa influeix en quan surts.", "Google la fa servir per saber a què et dediques.")),
        q(M, ("Si respondes a una reseña, el cliente no se entera.", "Google le avisa de que has contestado."),
             ("Si respons una ressenya, el client no se n'assabenta.", "Google l'avisa que has respost."))]},
    {"id": "domicilio_pedir_cat", "final": F_FICHA, "preguntas": [
        q(M, ("Si trabajas a domicilio y sin local, no puedes tener ficha de Google.", "Sí puedes: ocultas la dirección y pones tus zonas."),
             ("Si treballes a domicili i sense local, no pots tenir fitxa de Google.", "Sí que pots: amagues l'adreça i poses les teves zones.")),
        q(V, ("Pedir reseñas a tus clientes está permitido.", "Lo que no se puede es dar algo a cambio."),
             ("Demanar ressenyes als teus clients està permès.", "El que no es pot és donar res a canvi.")),
        q(M, ("Un dominio .cat sale peor en Google que un .com.", "Google los trata igual: cuenta lo que pone la web."),
             ("Un domini .cat surt pitjor a Google que un .com.", "Google els tracta igual: compta el que diu la web."))]},
    {"id": "gratis_fotos_blog", "final": F_WEB, "preguntas": [
        q(M, ("Salir en Google Maps cuesta dinero.", "La ficha es gratis; lo que cuenta es tenerla bien hecha."),
             ("Sortir a Google Maps costa diners.", "La fitxa és gratis; el que compta és tenir-la ben feta.")),
        q(V, ("Las fotos que suben tus clientes también salen en tu ficha.", "Por eso conviene que haya buenas fotos tuyas."),
             ("Les fotos que pugen els clients també surten a la teva fitxa.", "Per això convé que n'hi hagi de bones teves.")),
        q(M, ("Para salir en Google, tu web necesita un blog.", "Una web local puede salir bien sin blog."),
             ("Per sortir a Google, la teva web necessita un blog.", "Una web local pot sortir bé sense blog."))]},
    {"id": "dia_siguiente_festivos_formulario", "final": F_WEB, "preguntas": [
        q(M, ("Una web nueva sale en Google al día siguiente.", "Google puede tardar días o semanas en colocarla."),
             ("Una web nova surt a Google l'endemà.", "Google pot trigar dies o setmanes a col·locar-la.")),
        q(V, ("En la ficha de Google puedes poner otro horario para los festivos.", "Se llaman horarios especiales."),
             ("A la fitxa de Google pots posar un altre horari per als festius.", "Es diuen horaris especials.")),
        q(M, ("Un formulario de contacto no tiene nada que ver con la ley.", "Recoges datos: hay que informar de la privacidad."),
             ("Un formulari de contacte no té res a veure amb la llei.", "Reculls dades: cal informar de la privacitat."))]},
    {"id": "seguidores_sugerencias_nfc", "final": F_FICHA, "preguntas": [
        q(M, ("Tener muchos seguidores en Instagram te sube en Google.", "Google no usa tus seguidores para ordenar webs."),
             ("Tenir molts seguidors a Instagram et puja a Google.", "Google no fa servir els seguidors per ordenar webs.")),
        q(V, ("Otras personas pueden sugerir cambios en tu ficha de Google.", "Por eso conviene revisarla de vez en cuando."),
             ("Altres persones poden suggerir canvis a la teva fitxa de Google.", "Per això convé revisar-la de tant en tant.")),
        q(M, ("Para leer una tarjeta NFC hay que instalar una app.", "La mayoría de móviles actuales la leen sin nada."),
             ("Per llegir una targeta NFC cal instal·lar una app.", "La majoria de mòbils actuals la llegeixen sense res."))]},
    {"id": "enlaces_abierto_sinweb", "final": F_FICHA, "preguntas": [
        q(M, ("Comprar enlaces hacia tu web te ayuda a subir en Google.", "Va contra sus normas y te puede penalizar."),
             ("Comprar enllaços cap a la teva web t'ajuda a pujar a Google.", "Va contra les seves normes i et pot penalitzar.")),
        q(V, ("Si buscan “abierto ahora”, Google mira el horario de tu ficha.", "Sin horario, puedes quedarte fuera."),
             ("Si busquen “obert ara”, Google mira l'horari de la fitxa.", "Sense horari, et pots quedar fora.")),
        q(M, ("Sin web no puedes tener ficha de Google.", "Puedes, pero con web el cliente ve mucho más."),
             ("Sense web no pots tenir fitxa de Google.", "Sí que pots, però amb web el client veu molt més."))]},
    {"id": "cuenta_descripcion_media", "final": F_RES, "preguntas": [
        q(M, ("Se pueden dejar reseñas en Google sin tener cuenta.", "Hace falta una cuenta de Google."),
             ("Es poden deixar ressenyes a Google sense tenir compte.", "Cal un compte de Google.")),
        q(V, ("A Google le ayuda que tus fotos lleven una descripción.", "Así sabe qué sale en cada foto."),
             ("A Google l'ajuda que les fotos portin una descripció.", "Així sap què surt a cada foto.")),
        q(M, ("Las estrellas de tu ficha las pone Google a su gusto.", "Son la media de tus reseñas publicadas."),
             ("Les estrelles de la fitxa les posa Google al seu gust.", "Són la mitjana de les ressenyes publicades."))]},
    {"id": "cambiar_nombre_misma_lenta", "final": F_WEB, "preguntas": [
        q(M, ("Cambiar a menudo el nombre de tu ficha te ayuda a posicionar.", "Puede hacer que Google te pida verificarla otra vez."),
             ("Canviar sovint el nom de la fitxa t'ajuda a posicionar.", "Pot fer que Google et demani verificar-la una altra vegada.")),
        q(V, ("Tu ficha de Google es la misma en el buscador y en Maps.", "Una sola ficha: sale en los dos sitios."),
             ("La teva fitxa de Google és la mateixa al cercador i a Maps.", "Una sola fitxa: surt als dos llocs.")),
        q(V, ("Una web lenta puede salir más abajo en Google.", "La velocidad es una de las cosas que mira."),
             ("Una web lenta pot sortir més avall a Google.", "La velocitat és una de les coses que mira."))]},
    {"id": "copiar_responder_golpe", "final": F_RES, "preguntas": [
        q(M, ("Copiar los textos de otra web no tiene ningún problema.", "Tienen derechos y Google lo ve como copia."),
             ("Copiar els textos d'una altra web no té cap problema.", "Tenen drets i Google ho veu com a còpia.")),
        q(V, ("Responder a las reseñas puede ayudarte en Google.", "Google lo recomienda a los negocios."),
             ("Respondre les ressenyes et pot ajudar a Google.", "Google ho recomana als negocis.")),
        q(V, ("Muchas reseñas de golpe pueden hacer sospechar a Google.", "Puede filtrarlas si no parecen naturales."),
             ("Moltes ressenyes de cop poden fer sospitar Google.", "Les pot filtrar si no semblen naturals."))]},
    {"id": "horarios_titulo_editar", "final": F_RES, "preguntas": [
        q(M, ("Si el horario de tu web y el de tu ficha no coinciden, no pasa nada.", "Confundes al cliente y a Google."),
             ("Si l'horari de la web i el de la fitxa no coincideixen, no passa res.", "Confons el client i Google.")),
        q(V, ("El título de la página es de lo primero que lee Google.", "Ahí tiene que ir qué haces y dónde."),
             ("El títol de la pàgina és del primer que llegeix Google.", "Hi ha d'anar què fas i on.")),
        q(V, ("Un cliente puede cambiar su reseña mala por una buena.", "Si lo arreglas, él mismo puede editarla."),
             ("Un client pot canviar la seva ressenya dolenta per una de bona.", "Si ho arregles, ell mateix la pot editar."))]},
    {"id": "fotos_google_codigo_publicar", "final": F_WEB, "preguntas": [
        q(M, ("Puedes usar cualquier foto que encuentres en Google.", "Casi todas tienen derechos de autor."),
             ("Pots fer servir qualsevol foto que trobis a Google.", "Gairebé totes tenen drets d'autor.")),
        q(V, ("Una web hecha a código puede ser más rápida que una de plantilla.", "Lleva solo lo necesario, sin peso de más."),
             ("Una web feta a codi pot ser més ràpida que una de plantilla.", "Porta només el necessari, sense pes de més.")),
        q(V, ("En tu ficha de Google puedes publicar novedades, como en una red social.", "Se llaman publicaciones y salen en tu ficha."),
             ("A la fitxa de Google pots publicar novetats, com en una xarxa social.", "Es diuen publicacions i surten a la fitxa."))]},
]


PIE = {
    "es": ("¿Mito o verdad? Tres preguntas: dime en comentarios cuántas has acertado 👇\n\n"
           "¿Quieres una web clara para tu negocio? Escríbeme por WhatsApp: 641 27 74 95",
           "#mitooverdad #paginaweb #negocioslocales #girona #diseñoweb"),
    "ca": ("Mite o veritat? Tres preguntes: digues-me als comentaris quantes n'has encertat 👇\n\n"
           "Vols una web clara per al teu negoci? Escriu-me per WhatsApp: 641 27 74 95",
           "#miteoveritat #paginaweb #comerçlocal #girona #dissenyweb"),
}
