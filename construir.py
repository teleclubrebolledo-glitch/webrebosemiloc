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

SIMBOLO = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <defs>
    <symbol id="hoja" viewBox="-38 -2 76 116" preserveAspectRatio="none">
      <g id="mitad"><path class="f" d="M0 100C7 97 12 94 13 89C24 90 34 84 30 77C27 73 20 74 15 72C27 71 36 63 31 56C28 52 20 53 15 51C27 49 35 41 28 35C26 31 19 32 13 30C23 28 27 20 20 14C16 10 8 8 0 0Z"/><path class="v" d="M0 92L18 83M0 74L20 63M0 54L18 43M0 36L13 25"/></g>
      <use href="#mitad" transform="scale(-1 1)"/>
      <path class="v" d="M0 112V6"/>
    </symbol>
  </defs>
</svg>'''


def hoja(clase, interior):
    return f'<div class="{clase}"><svg viewBox="-38 -2 76 116" preserveAspectRatio="none" aria-hidden="true" focusable="false"><use href="#hoja" x="-38" y="-2" width="76" height="116"/></svg>{interior}</div>'


def rama(i, ident, nombre, subs):
    lado = "izq" if i % 2 == 0 else "der"
    ramita = '<svg class="ramita" viewBox="0 0 100 30" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path pathLength="1" d="M0 28C30 28 50 6 100 4"/></svg>'
    ramita_sub = '<svg class="ramita" viewBox="0 0 100 30" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path pathLength="1" d="M0 4C40 4 62 28 100 28"/></svg>'
    menu = hoja("hoja-menu", f'<span class="nombre">{escape(nombre)}</span>')
    lado_html = f'<span class="lado">{ramita}{menu}</span>'
    hijos = ""
    for j, (titulo, texto) in enumerate(subs):
        l2 = lado if j % 2 == 0 else ("der" if lado == "izq" else "izq")
        hijos += (f'<article class="sub {l2}" style="--i:{j}">{ramita_sub}'
                  + hoja("hoja-sub", f'<div class="texto"><h3>{escape(titulo)}</h3><p>{texto}</p></div>') + '</article>\n        ')
    return (f'    <details class="rama {lado}" name="menu" id="{ident}">\n      <summary>{lado_html}</summary>\n'
            f'      <div class="brote">\n        {hijos}</div>\n    </details>\n')


def main():
    ramas = "".join(rama(i, *c) for i, c in enumerate(CONTENIDO))
    pagina = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rebolledo de la Torre · Naturaleza, historia y estrellas</title>
<meta name="description" content="Página comunitaria no oficial sobre Rebolledo de la Torre (Burgos): naturaleza, historia, cielo nocturno y cómo visitarlo.">
<link rel="stylesheet" href="css/estilo.css">
<link rel="stylesheet" href="css/arbol.css">
</head>
<body>
{SIMBOLO}
<a class="salto" href="#contenido">Saltar al contenido</a>
<header class="cabecera">
  <div class="envoltorio">
    <div class="marca"><strong>Rebolledo de la Torre</strong><span>Naturaleza, historia y estrellas</span></div>
  </div>
</header>

<main id="contenido" class="envoltorio">
  <div class="portada">
    <h1>Un pueblo, su campo y su cielo</h1>
    <p>Página comunitaria dedicada a Rebolledo de la Torre. Toca una hoja para ver cómo crece la rama.</p>
    <p class="aviso"><strong>Importante:</strong> esta web es un proyecto comunitario y <strong>no es la web oficial del Ayuntamiento</strong>. Para trámites, avisos oficiales o información municipal, consulte al Ayuntamiento (<a href="https://www.rebolledodelatorre.es" rel="noopener">rebolledodelatorre.es</a>).</p>
  </div>

  <figure class="portada-video">
    <video controls muted loop playsinline preload="none" poster="media/cielo-nocturno.jpg" aria-label="Cielo nocturno sobre Rebolledo de la Torre (vídeo sin sonido)">
      <source src="media/cielo-nocturno.mp4" type="video/mp4">
      Tu navegador no puede reproducir el vídeo.
    </video>
    <figcaption>Cielo nocturno sobre Rebolledo · vídeo sin sonido, con permiso de su autor</figcaption>
  </figure>

  <nav class="arbol" aria-label="Secciones">
{ramas}  </nav>
</main>

<footer>
  <div class="envoltorio">
    <p>Proyecto comunitario sin ánimo de lucro. Esta web no usa cookies, no usa servicios de analítica ni publicidad y no recoge datos personales.</p>
    <ul>
      <li><a href="colabora.html">Colabora con tus fotos</a></li>
      <li><a href="aviso-legal.html">Aviso legal</a></li>
      <li><a href="privacidad.html">Privacidad y cookies</a></li>
      <li><a href="accesibilidad.html">Accesibilidad</a></li>
    </ul>
  </div>
</footer>
</body>
</html>
'''
    Path(__file__).with_name("index.html").write_text(pagina)
    print("index.html generado")


if __name__ == "__main__":
    main()
