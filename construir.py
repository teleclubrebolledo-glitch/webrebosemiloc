#!/usr/bin/env python3
"""Genera index.html (árbol de hojas de roble). Edita CONTENIDO y ejecuta: python3 construir.py
Sin dependencias, sin JavaScript en la web: todo el efecto es SVG + CSS."""
from pathlib import Path
from html import escape

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
                                ("Mirar con respeto", "Sin luces ni ruido: el cielo es de todos y el descanso también. " + PEND)]),
    ("patrimonio", "Patrimonio", [("Iglesia románica", "San Julián y Santa Basilisa, con galería porticada del siglo XII. " + PEND),
                                  ("La torre-castillo", "Emblema del pueblo y de su nombre. " + PEND),
                                  ("Costumbres", "Fiestas y tradiciones. " + PEND)]),
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
         "astro": "Cielo oscuro para mirar con calma, sin luces ni prisas.",
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

def tarjeta(ident, titulo, texto):
    return f'<article class="tarjeta" id="{ident}"><h3>{escape(titulo)}</h3><p>{texto}</p></article>'

def seccion(i, ident, nombre, subs):
    tarjetas = "\n      ".join(tarjeta(f"{ident}-{j+1}", t, x) for j, (t, x) in enumerate(subs))
    rama = '<svg class="trazo" viewBox="0 0 240 24" aria-hidden="true" focusable="false"><path pathLength="1" d="M2 18C30 18 40 4 70 8S110 22 140 14 190 2 238 10"/></svg>'
    return (f'  <section class="banda b{i % 2}" id="{ident}" style="--z:{40-i}" aria-labelledby="h-{ident}">\n'
            f'    <div class="envoltorio">\n      <h2 id="h-{ident}">{escape(nombre)}</h2>{rama}\n'
            f'      <p class="lead">{LEADS[ident]}</p>\n      <div class="rejilla">\n      {tarjetas}\n      </div>\n    </div>\n  </section>\n')

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
    <video controls muted loop playsinline preload="none" poster="media/cielo-nocturno.jpg" aria-label="Cielo nocturno sobre Rebolledo de la Torre (vídeo sin sonido)">
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
