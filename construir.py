#!/usr/bin/env python3
"""Genera index.html (árbol de hojas de roble). Edita CONTENIDO y ejecuta: python3 construir.py
Sin dependencias, sin JavaScript en la web: todo el efecto es SVG + CSS."""
from pathlib import Path
from html import escape
import graficos

PEND = '<small class="pendiente">por completar</small>'
LAT, LON = "42.6889", "-4.2271"   # de la web anterior (incrustado de Windy: 42.6889148, -4.2271223)
MAPA = f'<a href="https://www.openstreetmap.org/?mlat={LAT}&amp;mlon={LON}#map=14/{LAT}/{LON}" rel="noopener">Mapa (OpenStreetMap)</a>'
def tg(canal, texto): return f'<a href="https://t.me/{canal}" rel="noopener">{texto}</a>'
# (id, nombre de la hoja-menú, [(título, texto HTML)])  Contenido de la web anterior (web-rebolledo.pages.dev); verificar datos antes de publicar.
CONTENIDO = [
    ("rutas", "Rutas", [("Las Fuerzas de la Tierra", 'Peña Mesa · ~13,2 km · moderada · +384 m. <a href="https://es.wikiloc.com/rutas-senderismo/las-fuerzas-de-la-tierra-126481753" rel="noopener">Wikiloc</a>'),
                        ("Las Tuerces y la Horadada", "Formas kársticas esculpidas por el agua y el viento. Fácil/media."),
                        ("Valdelucio y las Loras", "Circular y moderada: valles, páramo y aves de las cortadas."),
                        ("Circuito románico", 'Rebolledo y su entorno, a pie o en coche. <a href="https://www.rebolledodelatorre.es/rutas" rel="noopener">Web municipal</a>')]),
    ("astro", "Astro-turismo", [("Geoparque Las Loras", "Cielo oscuro dentro del Geoparque Mundial de la UNESCO."),
                                ("Observatorios", '<a href="https://www.astroburgos.org/agenda/" rel="noopener">Agenda Astroburgos</a> · <a href="https://astrodemanda.blogspot.com/" rel="noopener">AstroDemanda</a>'),
                                ("Orientar el telescopio", "@ASTRO"),
                                ("A qué altura mirar", "@G:altura|Todo lo del cielo se mide en grados sobre el horizonte. Con el brazo estirado, un puño cerrado son unos 10°, la mano abierta unos 20° y el dedo meñique, 1°. Desde Rebolledo la Polar queda siempre a unos 42,7°."),
                                ("El camino del Sol", "@SOL"),
                                ("Orión, el cielo de invierno", "@G:orion|El Cinturón (tres estrellas en fila) es la guía: hacia abajo a la izquierda señala Sirio, la más brillante del cielo, y hacia arriba a la derecha Aldebarán. Desde aquí el Cinturón llega a unos %d° de altura, de diciembre a febrero al anochecer." % round(90 - abs(graficos.LAT - -1.2))),
                                ("El Triángulo de Verano", "@G:triangulo|Vega, Deneb y Altair, de julio a octubre al anochecer. Vega y Deneb pasan casi por encima de la cabeza (unos %d° y %d°); Altair llega a unos %d°. La Vía Láctea los cruza." % (round(90 - abs(graficos.LAT - 38.78)), round(90 - abs(graficos.LAT - 45.28)), round(90 - abs(graficos.LAT - 8.87)))),
                                ("Qué sale por dónde", "@G:panorama|Desde un punto con el horizonte despejado: el Sol, la Polar y tres objetivos, por rumbo y altura. Cada lugar real tiene su propio horizonte (árboles, casas, lomas): busca uno despejado al norte para la Polar y al sur para el cielo de invierno."),
                                ("Fases de la Luna", "@G:lunas|Para el cielo profundo, mejor cerca de la Luna nueva; con la Luna llena, el protagonista es ella, hasta con prismáticos. Creciente: se ve por la tarde; menguante: de madrugada."),
                                ("Lluvias de estrellas", "@LLUVIA"),
                                ("Dónde observar desde Rebolledo", "@PUNTOS"),
                                ("Mirar con respeto", "@G:respeto|Sin luces ni ruido: el cielo es de todos y el descanso también. " + PEND)]),
    ("patrimonio", "Patrimonio", [("Iglesia románica", 'San Julián y Santa Basilisa: una de las galerías porticadas más bellas del románico castellano, firmada por Juan de Piasca en 1186, y una pila bautismal de 1195. La torre de la iglesia es renacentista. <a href="https://www.turismocastillayleon.com/es/patrimonio-cultura/iglesias-ermitas/iglesia-san-julian-santa-basilisa" rel="noopener">Turismo de Castilla y León</a>'),
                                  ("La torre-castillo", 'Dos torres esbeltas se alzan sobre el caserío: la de la iglesia y la del castillo medieval que perteneció a la familia Lasso de la Vega. <a href="https://www.terranostrum.es/turismo/burgos/sedano-y-las-loras/iglesia-de-san-julian-y-santa-basilisa-rebolledo-de-la-torre" rel="noopener">Terra Nostrum</a>'),
                                  ("Costumbres", 'Las fiestas patronales de San Julián y Santa Basilisa se celebran en torno al 9 de enero. <a href="https://www.festivalesdeespana.com/festival/fiestas-san-julian-santa-basilisa-rebolledo-de-la-torre" rel="noopener">Festivales de España</a> ' + PEND)]),
    ("eventos", "Eventos", [("El eclipse en la plaza", "Gafas especiales, silencio al cubrirse el Sol y aplausos: una tarde que el pueblo recuerda."),
                            ("Próximo evento", "Aquí se anunciará. " + PEND)]),
    ("comunidad", "Comunidad", [("Canales de Telegram", tg("Rebolledodelatorre", "Pueblo") + " · " + tg("rutasrebolledodelatorre", "Rutas") + " · " + tg("rebolledodelatorrehuerta", "Huerta") + " · " + tg("Rebolledodelatorreenlaces", "Enlaces")),
                                ("Tus fotos", '<a href="colabora.html">Cómo colaborar</a> o por Telegram: <a href="https://t.me/rebolledodelatorre_bot" rel="noopener">@rebolledodelatorre_bot</a>'),
                                ("Galería", '<a href="galeria.html">Ver las fotos</a>')]),
    ("visitar", "Visitar", [("Cómo llegar", "Provincia de Burgos. " + MAPA),
                            ("El tiempo", '<a href="https://windy.com/' + LAT + '/' + LON + '" rel="noopener">Windy</a> (se abre en otra página)'),
                            ("Contacto", '<a href="mailto:teleclubrebolledo@gmail.com">teleclubrebolledo@gmail.com</a>')]),
]

LEADS = {"rutas": "Itinerarios del entorno, dentro del Geoparque Mundial de la UNESCO Las Loras.",
         "astro": "Cielo oscuro para mirar con calma, sin luces ni prisas. Desliza hacia los lados.",
         "patrimonio": "Su iglesia, su torre y las costumbres que siguen vivas.",
         "eventos": "Lo que se vive en el pueblo, contado por quienes lo viven.",
         "comunidad": "Canales de Telegram, fotos de vecinas y vecinos, y cómo sumarse.",
         "visitar": "Cómo llegar, el tiempo y cómo escribirnos."}

# Curvatura de lóbulos de roble como único motivo: borde festoneado (máscara), línea que crece y rama de fondo.
def rama_fondo():
    return ('<svg class="rama-fondo" viewBox="0 0 120 1000" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            '<path class="tallo" pathLength="1" d="M70 1000C96 930 40 880 66 820S104 720 62 650 28 560 70 480 96 380 56 300 38 210 74 140 80 60 62 0"/>'
            '<path class="ramita r1" pathLength="1" d="M64 830C40 810 22 812 8 790"/>'
            '<path class="ramita r2" pathLength="1" d="M70 480C94 462 108 466 118 444"/>'
            '<path class="ramita r3" pathLength="1" d="M56 300C34 288 22 292 10 270"/>'
            '<path class="ramita r4" pathLength="1" d="M74 140C94 126 106 132 116 112"/>'
            '</svg>')

ASTRO_GUIA = (
    '<ol class="guia"><li><strong>Encuentra la Polar.</strong> Une Merak y Dubhe, las dos estrellas del borde del Carro, y prolonga esa línea unas cinco veces su distancia.</li>'
    '<li><strong>Inclina la montura.</strong> Desde Rebolledo la Polar está a unos %.1f° sobre el horizonte norte: ese es el ángulo del eje polar.</li>'
    '<li><strong>Objetivo de la noche: el Doble Cúmulo de Perseo,</strong> entre Casiopea y Perseo. Desde aquí nunca se pone (de unos 10° en su punto más bajo a unos 76° en el más alto) y se ve como una mancha; con prismáticos o un telescopio de campo amplio se separa en dos cúmulos.</li>'
    '<li><strong>Cuida la vista.</strong> Luz roja y unos 20 minutos para que los ojos se acostumbren a la oscuridad.</li></ol>'
    '<p class="nota">Esquemas orientativos, con posiciones redondeadas: para orientarse a ojo, no para apuntar con precisión. Comprueba la altura con una app de planetario.</p>') % graficos.LAT

LLUVIAS_TXT = ('<ul class="guia">' + "".join(f"<li><strong>{n}</strong> · máximo hacia el {d} de {['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'][m-1]} · radiante en {c}</li>" for n, m, d, c in graficos.LLUVIAS) + "</ul>"
    '<p class="nota">Fechas aproximadas del máximo (varían un día de un año a otro). Las Perseidas, con su radiante muy al norte, no se ponen nunca desde Rebolledo: el punto del que parecen salir queda siempre sobre el horizonte. Mejor lejos de las luces y sin Luna llena.</p>')

def _puntos_txt():
    li = ""
    for let, nom, x, y, rumbo, que in graficos.PUNTOS_PUBLICOS:
        lat, lon, d = graficos.coordenadas_punto(x, y)
        li += (f'<li><strong>{let} · {nom}</strong> (mira al {rumbo}; a unos {round(d, -1):.0f} m del casco). {que} '
               f'<a href="https://www.openstreetmap.org/?mlat={lat:.5f}&amp;mlon={lon:.5f}#map=17/{lat:.5f}/{lon:.5f}" rel="noopener">Ver en el mapa</a></li>')
    return (f'<ol class="guia" style="list-style:none;padding:0">{li}</ol>'
            '<p class="nota"><strong>Candidatos por confirmar.</strong> Salen de mirar una vista de satélite, no de haber pisado el sitio: faltan comprobar el acceso, las luces de las granjas y el horizonte real. '
            'Mira desde caminos públicos y sin pisar cultivos ni fincas. ¿Conoces un sitio mejor? Cuéntalo en <a href="colabora.html">Colabora</a>.</p>')

def _sol_txt(filas):
    li = "".join(f"<li><strong>{n}.</strong> Sale hacia {az:.0f}° (desde el norte) y se pone hacia {360-az:.0f}°; sube a {alt:.0f}° al mediodía y el día dura unas {int(d)} h {round((d % 1) * 60):02d} min.</li>" for n, alt, az, d, _ in filas)
    return f'<ol class="guia" style="list-style:none;padding:0">{li}</ol><p class="nota">Cálculo geométrico para la latitud de Rebolledo (sin refracción: el día real dura unos minutos más). 90° = este, 180° = sur, 270° = oeste.</p>'

def tarjeta(ident, titulo, texto):
    if texto == "@ASTRO":
        return (f'<article class="tarjeta ancha" id="{ident}"><div class="figuras">{graficos.carta_polar()}{graficos.montura()}</div>'
                f'<div class="texto"><h3>{escape(titulo)}</h3><details><summary>Ver los pasos</summary>{ASTRO_GUIA}</details></div></article>')
    if texto == "@PUNTOS":
        return (f'<article class="tarjeta ancha" id="{ident}"><div class="figuras una" style="background:#e6edd2">{graficos.plano_observacion()}</div>'
                f'<div class="texto"><h3>{escape(titulo)}</h3><details open><summary>Tres puntos candidatos</summary>{_puntos_txt()}</details></div></article>')
    if texto == "@SOL":
        svg, filas = graficos.camino_sol()
        return (f'<article class="tarjeta ancha" id="{ident}"><div class="figuras una">{svg}</div>'
                f'<div class="texto"><h3>{escape(titulo)}</h3><details><summary>Ver los datos</summary>{_sol_txt(filas)}</details></div></article>')
    if texto == "@LLUVIA":
        return (f'<article class="tarjeta ancha" id="{ident}"><div class="figuras una">{graficos.rueda_lluvias()}</div>'
                f'<div class="texto"><h3>{escape(titulo)}</h3><details><summary>Ver las fechas</summary>{LLUVIAS_TXT}</details></div></article>')
    if texto.startswith("@G:"):
        nombre, texto = texto[3:].split("|", 1)
        g = {"altura": graficos.altura_ladder, "orion": graficos.orion, "triangulo": graficos.triangulo_verano,
             "lunas": graficos.lunas, "respeto": graficos.respeto, "panorama": graficos.panorama_abierto}[nombre]
    else:
        g = graficos.GRAFICOS.get(ident)
    fig = f'<figure>{g()}</figure>' if g else ""
    return f'<article class="tarjeta" id="{ident}">{fig}<div class="texto"><h3>{escape(titulo)}</h3><p>{texto}</p></div></article>'

def seccion(i, ident, nombre, subs):
    BANNER = ' banner' if ident == 'astro' else ''
    tarjetas = "\n      ".join(tarjeta(f"{ident}-{j+1}", t, x) for j, (t, x) in enumerate(subs))
    rama = '<svg class="trazo" viewBox="0 0 240 24" aria-hidden="true" focusable="false"><path pathLength="1" d="M2 18C30 18 40 4 70 8S110 22 140 14 190 2 238 10"/></svg>'
    return (f'  <section class="banda b{i % 2}" id="{ident}" style="--z:{40-i}" aria-labelledby="h-{ident}">\n'
            f'    <div class="envoltorio">\n      <h2 id="h-{ident}">{escape(nombre)}</h2>{rama}\n'
            f'      <p class="lead">{LEADS[ident]}</p>\n      <div class="rejilla{BANNER}">\n      {tarjetas}\n      </div>\n    </div>\n  </section>\n')

def menu(ident, nombre, subs):
    enlaces = "".join(f'<a href="#{ident}-{j+1}">{escape(t)}</a>' for j, (t, _) in enumerate(subs))
    return (f'<li><details name="m"><summary>{escape(nombre)}</summary><div class="sub">'
            f'<svg viewBox="0 0 12 100" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path pathLength="1" d="M6 0C0 25 12 40 6 60S4 90 6 100"/></svg>'
            f'<a href="#{ident}">Ver todo</a>{enlaces}</div></details></li>')

def main():
    nav = "".join(menu(*c) for c in CONTENIDO)
    secciones = "".join(seccion(i, *c) for i, c in enumerate(CONTENIDO))
    pagina = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rebolledo de la Torre · Naturaleza, historia y estrellas</title>
<meta name="description" content="Página comunitaria no oficial sobre Rebolledo de la Torre (Burgos): rutas, cielo nocturno, patrimonio y comunidad.">
<meta name="theme-color" content="#2e5a2b">
<link rel="stylesheet" href="css/estilo.css">
<link rel="stylesheet" href="css/roble.css">
</head>
<body>
<a class="salto" href="#contenido">Saltar al contenido</a>
{rama_fondo()}
<header class="barra">
  <a class="marca" href="#inicio"><strong>Rebolledo de la Torre</strong></a>
  <nav aria-label="Principal"><ul>{nav}</ul></nav>
</header>

<main id="contenido">
  <section class="portada" id="inicio" style="--z:50">
    <video autoplay muted loop playsinline controls preload="auto" poster="media/cielo-nocturno.jpg" aria-label="Cielo nocturno sobre Rebolledo de la Torre (vídeo sin sonido)">
      <source src="media/cielo-nocturno.mp4" type="video/mp4">
    </video>
    <div class="portada-texto">
      <h1>Rebolledo de la Torre</h1>
      <p>Naturaleza, historia y estrellas</p>
    </div>
  </section>
  <p class="aviso envoltorio"><strong>Importante:</strong> esta web es un proyecto comunitario y <strong>no es la web oficial del Ayuntamiento</strong>. Para trámites, avisos oficiales o información municipal, consulte al Ayuntamiento (<a href="https://www.rebolledodelatorre.es" rel="noopener">rebolledodelatorre.es</a>).</p>
{secciones}</main>

<footer class="pie">
  <div class="envoltorio">
    <p>Proyecto comunitario sin ánimo de lucro. Sin cookies, sin analítica, sin publicidad y sin recoger datos personales. Vídeo de portada con permiso de su autor.</p>
    <ul>
      <li><a href="colabora.html">Colabora con tus fotos</a></li>
      <li><a href="galeria.html">Galería</a></li>
      <li><a href="aviso-legal.html">Aviso legal</a></li>
      <li><a href="privacidad.html">Privacidad y cookies</a></li>
      <li><a href="accesibilidad.html">Accesibilidad</a></li>
    </ul>
  </div>
</footer>
</body>
</html>
"""
    Path(__file__).with_name("index.html").write_text(pagina)
    print("index.html generado")


if __name__ == "__main__":
    main()
