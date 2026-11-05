#!/usr/bin/env python3
"""Genera index.html (árbol de hojas de roble). Edita CONTENIDO y ejecuta: python3 construir.py
Sin dependencias, sin JavaScript en la web: todo el efecto es SVG + CSS."""
from pathlib import Path
from html import escape
import graficos, fichas, json, huerta_web

PEND = '<small class="pendiente">por completar</small>'
LAT, LON = "42.6889", "-4.2271"   # de la web anterior (incrustado de Windy: 42.6889148, -4.2271223)
MAPA = f'<a href="https://www.openstreetmap.org/?mlat={LAT}&amp;mlon={LON}#map=14/{LAT}/{LON}" rel="noopener">Mapa (OpenStreetMap)</a>'
def tg(canal, texto): return f'<a href="https://t.me/{canal}" rel="noopener">{texto}</a>'
# (id, nombre de la hoja-menú, [(título, texto HTML)])  Contenido de la web anterior (web-rebolledo.pages.dev); verificar datos antes de publicar.
CONTENIDO = [
    ("rutas", "Rutas", [("Peña Mesa", "@RUTA:pena-mesa"),
                        ("Cruz de Valdeverano", "@RUTA:cruz-valdeverano"),
                        ("Mirador del norte", "@RUTA:mirador-norte"),
                        ("Aporta tu ruta", "@APORTA"),
                        ("Las Fuerzas de la Tierra", 'Peña Mesa · ~13,2 km · moderada · +384 m. <a href="https://es.wikiloc.com/rutas-senderismo/las-fuerzas-de-la-tierra-126481753" rel="noopener">Wikiloc</a>'),
                        ("Las Tuerces y la Horadada", "Formas kársticas esculpidas por el agua y el viento. Fácil/media."),
                        ("Valdelucio y las Loras", "Circular y moderada: valles, páramo y aves de las cortadas."),
                        ("Circuito románico", 'Rebolledo y su entorno, a pie o en coche. <a href="https://www.rebolledodelatorre.es/rutas" rel="noopener">Web municipal</a>')]),
    ("astro", "Astro-turismo", [("Dónde observar desde Rebolledo", "@PUNTOS"),
                                ("Orientar el telescopio", "@ASTRO"),
                                ("Orión, el cielo de invierno", "@G:orion|El Cinturón (tres estrellas en fila) es la guía: hacia abajo a la izquierda señala Sirio, la más brillante del cielo, y hacia arriba a la derecha Aldebarán. Desde aquí el Cinturón llega a unos %d° de altura, de diciembre a febrero al anochecer." % round(90 - abs(graficos.LAT - -1.2))),
                                ("El Triángulo de Verano", "@G:triangulo|Vega, Deneb y Altair, de julio a octubre al anochecer. Vega y Deneb pasan casi por encima de la cabeza (unos %d° y %d°); Altair llega a unos %d°. La Vía Láctea los cruza." % (round(90 - abs(graficos.LAT - 38.78)), round(90 - abs(graficos.LAT - 45.28)), round(90 - abs(graficos.LAT - 8.87)))),
                                ("El camino del Sol", "@SOL"),
                                ("Geoparque Las Loras", "@G:geoparque|Cielo oscuro dentro del Geoparque Mundial de la UNESCO."),
                                ("Observatorios", "@G:observatorios|" + '<a href="https://www.astroburgos.org/agenda/" rel="noopener">Agenda Astroburgos</a> · <a href="https://astrodemanda.blogspot.com/" rel="noopener">AstroDemanda</a>'),
                                ("A qué altura mirar", "@G:altura|Todo lo del cielo se mide en grados sobre el horizonte. Con el brazo estirado, un puño cerrado son unos 10°, la mano abierta unos 20° y el dedo meñique, 1°. Desde Rebolledo la Polar queda siempre a unos 42,7°."),
                                ("Qué sale por dónde", "@G:panorama|Desde un punto con el horizonte despejado: el Sol, la Polar y tres objetivos, por rumbo y altura. Cada lugar real tiene su propio horizonte (árboles, casas, lomas): busca uno despejado al norte para la Polar y al sur para el cielo de invierno."),
                                ("Fases de la Luna", "@G:lunas|Para el cielo profundo, mejor cerca de la Luna nueva; con la Luna llena, el protagonista es ella, hasta con prismáticos. Creciente: se ve por la tarde; menguante: de madrugada."),
                                ("Lluvias de estrellas", "@LLUVIA"),
                                ("Mirar con respeto", "@G:respeto|Sin luces ni ruido: el cielo es de todos y el descanso también. " + PEND)]),

    ("patrimonio", "Patrimonio", [("Iglesia románica", 'San Julián y Santa Basilisa: una de las galerías porticadas más bellas del románico castellano, firmada por Juan de Piasca en 1186, y una pila bautismal de 1195. La torre de la iglesia es renacentista. <a href="https://www.turismocastillayleon.com/es/patrimonio-cultura/iglesias-ermitas/iglesia-san-julian-santa-basilisa" rel="noopener">Turismo de Castilla y León</a>'),
                                  ("La torre-castillo", 'Dos torres esbeltas se alzan sobre el caserío: la de la iglesia y la del castillo medieval que perteneció a la familia Lasso de la Vega. <a href="https://www.terranostrum.es/turismo/burgos/sedano-y-las-loras/iglesia-de-san-julian-y-santa-basilisa-rebolledo-de-la-torre" rel="noopener">Terra Nostrum</a>'),
                                  ("Fiestas del pueblo", "@FIESTAS"),
                                  ("Costumbres", 'Las fiestas patronales de San Julián y Santa Basilisa se celebran en torno al 9 de enero. <a href="https://www.festivalesdeespana.com/festival/fiestas-san-julian-santa-basilisa-rebolledo-de-la-torre" rel="noopener">Festivales de España</a> ' + PEND)]),
    ("eventos", "Eventos", [("El eclipse en la plaza", "Gafas especiales, silencio al cubrirse el Sol y aplausos: una tarde que el pueblo recuerda."),
                            ("Próximo evento", "Aquí se anunciará. " + PEND)]),
    ("comunidad", "Comunidad", [("Canales de Telegram", tg("Rebolledodelatorre", "Pueblo") + " · " + tg("rutasrebolledodelatorre", "Rutas") + " · " + tg("rebolledodelatorrehuerta", "Huerta") + " · " + tg("Rebolledodelatorreenlaces", "Enlaces")),
                                ("Tus fotos", '<a href="enviar-fotos.html">Cómo enviar tus fotos</a> por el bot de Telegram <a href="https://t.me/rebolledodelatorre_bot" rel="noopener">@rebolledodelatorre_bot</a>'),
                                ("Galería", '<a href="galeria.html">Ver las fotos</a>')]),
    ("visitar", "Visitar", [("Horario del Teleclub", "Horario: por confirmar con el propio Teleclub. " + PEND),
                            ("Horario de visitas a la iglesia", "Iglesia de San Julián y Santa Basilisa (siglo XII, pórtico románico). Para visitarla hay que avisar al teléfono <strong>616 440 648</strong> (dato de Turismo de Castilla y León, <em>por confirmar</em>). Horario fijo: por confirmar. Hay visitas guiadas al pórtico sobre todo en las fiestas patronales de enero."),
                            ("Horario del Ayuntamiento", "Calle Barrio Alto s/n. Teléfono <strong>947 572 303</strong> y web <a href=\"https://www.rebolledodelatorre.es\" rel=\"noopener\">rebolledodelatorre.es</a>. Horario de atención: por confirmar; consúltalo allí."),
                            ("Transporte a la demanda", "En Castilla y León funciona el transporte público «a la demanda»: no hay horario fijo, hay que pedir el viaje con antelación a la central de reservas de la Junta (hay un bono rural gratuito en muchas zonas). Las expediciones y el teléfono concretos de esta zona: por confirmar con el Ayuntamiento o la Junta."),
                            ("Cómo llegar", "Provincia de Burgos. " + MAPA),
                            ("El tiempo", '<a href="https://windy.com/' + LAT + '/' + LON + '" rel="noopener">Windy</a> (se abre en otra página)'),
                            ("Contacto", 'Escríbenos por el bot de Telegram <a href="https://t.me/rebolledodelatorre_bot" rel="noopener">@rebolledodelatorre_bot</a> (botón «Hablar con el equipo»).')]),
]

def _rutas_comunidad():
    ix = Path(__file__).with_name("datos-rutas") / "index.json"
    try: ids = json.loads(ix.read_text())
    except Exception: return []
    out = []
    for i in ids:
        try: out.append((fichas.cargar(i)["nombre"], "@RUTA:" + i))
        except Exception: pass
    return out
for _i, _c in enumerate(CONTENIDO):
    if _c[0] == "rutas":
        _l = list(_c[2]); _pos = next(k for k, (t, _) in enumerate(_l) if t == "Aporta tu ruta")
        _com = _rutas_comunidad(); APORTA_ID = f"rutas-{_pos + len(_com) + 1}"
        CONTENIDO[_i] = (_c[0], _c[1], _l[:_pos] + _com + _l[_pos:])

AVISOS = {}
def _recorta(t, n):
    t = t.strip()
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"
def _seccion_avisos():
    global AVISOS
    try: AVISOS = json.loads((Path(__file__).parent / "avisos" / "salida" / "avisos.json").read_text())
    except Exception: AVISOS = {"items": [], "actualizado": "", "estado_fuentes": {}}
    subs = [("Cómo funciona esta sección", "@AVISA")] + [(_recorta(a["titulo_natural"], 72), f"@AVISO:{i}") for i, a in enumerate(AVISOS["items"][:20])]
    return subs
for _i, _c in enumerate(CONTENIDO):
    if _c[0] == "rutas":
        CONTENIDO.insert(_i + 1, ("avisos", "Avisos y ayudas", _seccion_avisos()))
        CONTENIDO.insert(_i + 2, ("huerta", "Huerta", [("Este mes en la huerta", "@H:este_mes"), ("El mes que viene en la huerta", "@H:proximo"), ("Receta del mes", "@H:receta"), ("Productos de temporada", "@H:temporada"), ("Calendario de la huerta", "@H:calendario"),
                                                       ("Hortalizas y legumbres", "@H:hortalizas"), ("Frutales y árboles de la zona", "@H:frutales"), ("Aromáticas, medicinales y silvestres", "@H:aromaticas"),
                                                       ("Flores", "@H:flores"), ("Setas: temporadas y peligros", "@H:setas"), ("Plantas peligrosas", "@H:peligros"), ("Consejos para la huerta (altitud de la zona: 958 m)", "@H:consejos")]))
        CONTENIDO.insert(_i + 3, ("naturaleza", "Fauna y flora", [("Un territorio, muchos hábitats", "@N:habitats"), ("Aves de los cortados y del cielo", "@N:rapaces"), ("Aves del campo, del pueblo y de la noche", "@N:campo"),
                                                                 ("Calendario de las aves", "@N:calendario"), ("Mamíferos", "@N:mamiferos"), ("Reptiles y anfibios", "@N:reptiles"), ("Insectos y polinizadores", "@N:insectos"),
                                                                 ("Árboles y arbustos", "@N:arboles"), ("Plantas y flores silvestres", "@N:flora"), ("Mirar sin molestar", "@N:mirar")]))
        break

LEADS = {"huerta": "Qué sembrar, plantar y cosechar cada mes a unos 958 m de altitud sobre el nivel del mar (la de la zona, no la superficie del terreno), con fichas de cultivos, frutales, flores, setas y plantas peligrosas.", "naturaleza": "Todo lo vivo de las loras y los páramos: aves, mamíferos, reptiles, insectos, árboles y flores.", "avisos": "Lo que sale en los boletines oficiales y en la prensa del medio rural y puede interesar a Rebolledo de la Torre y sus localidades.", "rutas": "Itinerarios del entorno, dentro del Geoparque Mundial de la UNESCO Las Loras.",
         "astro": "Cielo oscuro para mirar con calma, sin luces ni prisas.",
         "patrimonio": "Su iglesia, su torre y las costumbres que siguen vivas.",
         "eventos": "Lo que se vive en el pueblo, contado por quienes lo viven.",
         "comunidad": "Canales de Telegram, fotos de vecinas y vecinos, y cómo sumarse.",
         "visitar": "Horarios, transporte, cómo llegar, el tiempo y cómo escribirnos."}

# Curvatura de lóbulos de roble como único motivo: borde festoneado (máscara), línea que crece y rama de fondo.
def rama_fondo():
    return ('<svg class="rama-fondo" viewBox="0 0 120 1000" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            '<path class="tallo" pathLength="1" d="M70 1000C96 930 40 880 66 820S104 720 62 650 28 560 70 480 96 380 56 300 38 210 74 140 80 60 62 0"/>'
            '<path class="ramita r1" pathLength="1" d="M64 830C40 810 22 812 8 790"/>'
            '<path class="ramita r2" pathLength="1" d="M70 480C94 462 108 466 118 444"/>'
            '<path class="ramita r3" pathLength="1" d="M56 300C34 288 22 292 10 270"/>'
            '<path class="ramita r4" pathLength="1" d="M74 140C94 126 106 132 116 112"/>'
            '</svg>')

CATEGORIAS_AVISOS = {k: v['nombre'] for k, v in json.loads((Path(__file__).parent / 'avisos' / 'config.json').read_text())['categorias'].items()}

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
            'Los sectores de color del plano (relieve que podría tapar el cielo, luz del pueblo) son una estimación a ojo. Mira desde caminos públicos y sin pisar cultivos ni fincas. ¿Conoces un sitio mejor? Cuéntalo al equipo por el bot de Telegram (botón «Hablar con el equipo»).</p>')

def _sol_txt(filas):
    li = "".join(f"<li><strong>{n}.</strong> Sale hacia {az:.0f}° (desde el norte) y se pone hacia {360-az:.0f}°; sube a {alt:.0f}° al mediodía y el día dura unas {int(d)} h {round((d % 1) * 60):02d} min.</li>" for n, alt, az, d, _ in filas)
    return f'<ol class="guia" style="list-style:none;padding:0">{li}</ol><p class="nota">Cálculo geométrico para la latitud de Rebolledo (sin refracción: el día real dura unos minutos más). 90° = este, 180° = sur, 270° = oeste.</p>'

def tarjeta(ident, titulo, texto):
    if texto == "@ASTRO":
        return (f'<article class="tarjeta ancha" id="{ident}"><div class="figuras">{graficos.carta_polar()}{graficos.montura()}</div>'
                f'<div class="texto"><h3>{escape(titulo)}</h3><details><summary>Ver los pasos</summary>{ASTRO_GUIA}</details></div></article>')
    if texto.startswith("@H:") or texto.startswith("@N:"):
        icono, cuerpo, ancha = huerta_web.card(texto[1:])
        cls = "tarjeta ancha" if ancha else "tarjeta"
        if cuerpo.startswith('<div class="figuras'):
            i = cuerpo.index("</div>") + 6
            return f'<article class="{cls}" id="{ident}">{cuerpo[:i]}<div class="texto"><h3>{escape(titulo)}</h3>{cuerpo[i:]}</div></article>'
        return f'<article class="{cls}" id="{ident}"><figure>{graficos.icono_natural(icono)}</figure><div class="texto"><h3>{escape(titulo)}</h3>{cuerpo}</div></article>'
    if texto == "@FIESTAS":
        base = Path(__file__).parent / "contenido" / "fiestas"
        try: ids = json.loads((base / "index.json").read_text())
        except Exception: ids = []
        docs = []
        for i in ids:
            try: docs.append(json.loads((base / f"{i}.json").read_text()))
            except Exception: pass
        if not docs:
            cuerpo = ('<p>Aún no hay fiestas contadas aquí. Las contará la gente del pueblo, con sus palabras: cómo se preparan, qué se hace hora a hora, qué se come, qué ha cambiado.</p>'
                      '<p><a href="contar-fiestas.html">Cómo contar una fiesta</a> (el bot de Telegram te lo pregunta paso a paso, por escrito o con notas de voz).</p>')
        else:
            det = ""
            for dd in docs:
                aut = f" · contado por {escape(dd['autor'])}" if dd.get("autor") else ""
                det += (f'<details class="ficha"><summary><strong>{escape(dd["titulo"])}</strong>{aut}</summary><ul class="guia" style="margin:.3rem 0">'
                        + "".join(f'<li><strong>{escape(c_["pregunta"])}</strong> {escape(c_["respuesta"])}</li>' for c_ in dd["campos"] if c_.get("id") != "nombre") + "</ul>"
                        + "".join(f'<figure style="margin:.4rem 0"><img src="contenido/fiestas/{escape(f["archivo"])}" alt="Foto de la fiesta {escape(dd["titulo"])}" loading="lazy" style="max-width:100%;border-radius:12px 12px 0 0"><figcaption class="nota">{escape(f["pie"])}</figcaption></figure>' for f in dd.get("fotos", [])) + "</details>")
            cuerpo = f'<p>Las fiestas, contadas por quienes las viven.</p>{det}<p><a href="contar-fiestas.html">Cuenta tú otra fiesta</a>.</p>'
        return (f'<article class="tarjeta ancha" id="{ident}"><figure>{graficos.icono_natural("calendario")}</figure><div class="texto"><h3>{escape(titulo)}</h3>{cuerpo}</div></article>')
    if texto == "@AVISA":
        est = AVISOS.get("estado_fuentes", {}); act = AVISOS.get("actualizado", "") or "todavía no"
        li = "".join(f"<li>{escape(k)}: {escape(v.split(' (')[0].split(':')[0])}</li>" for k, v in est.items())
        return (f'<article class="tarjeta" id="{ident}"><figure>{graficos.icono_aviso("noticias")}</figure><div class="texto"><h3>{escape(titulo)}</h3>'
                f'<p>Cada día un programa de este proyecto lee el <strong>BOE</strong>, el <strong>BOCYL</strong> y noticias del medio rural de Castilla y León, '
                f'se queda con lo que puede interesar a Rebolledo de la Torre (ayudas, obras y energía, comunicaciones, transporte, vivienda, empleo, educación, cultura, turismo y emprendimiento) y lo cuenta en palabras sencillas. '
                f'No usa inteligencia artificial. <strong>Vale siempre el texto oficial</strong> del enlace.</p>'
                f'<p class="nota">Última actualización: {escape(act)}. Estado de las fuentes:</p><ul class="guia" style="margin-top:0">{li}</ul></div></article>')
    if texto.startswith("@AVISO:"):
        a = AVISOS["items"][int(texto[7:])]
        cats = [k for k in a["categorias"] if k != "noticias"] or a["categorias"]
        orden = ("energia", "comunicaciones", "transporte", "vivienda", "ayudas", "rural", "cultura", "educacion", "turismo", "noticias")
        icono = next((c for c in orden if c in a["categorias"]), "ayudas")
        etiqueta = escape(CATEGORIAS_AVISOS.get(cats[0], cats[0]))
        fecha = "/".join(reversed(a["fecha"].split("-")))
        datos = "".join(f"<li><strong>{k}:</strong> {escape(v)}</li>" for k, v in (("A quién", ", ".join(a["a_quien"])), ("Plazo", a.get("plazo") or ""), ("Importe", a.get("importe") or "")) if v)
        return (f'<article class="tarjeta" id="{ident}"><figure>{graficos.icono_aviso(icono)}</figure><div class="texto"><h3>{escape(_recorta(a["titulo_natural"], 190))}</h3>'
                f'<p><span class="etiqueta">{etiqueta}</span> {fecha} · {escape(a["fuente"])}</p><p>{escape(a["resumen"])}</p>'
                + (f'<ul class="guia" style="margin:.2rem 0 .4rem">{datos}</ul>' if datos else '') +
                f'<p><a href="{escape(a["enlace"])}" rel="noopener">Ver el texto oficial</a></p></div></article>')
    if texto == "@APORTA":
        return (f'<article class="tarjeta" id="{ident}"><figure>{graficos.punto_vacio()}</figure><div class="texto"><h3>{escape(titulo)}</h3>'
                '<p>¿Has recorrido un sendero del entorno y lo has grabado con el móvil? Envía el archivo .gpx al bot de Telegram <a href="https://t.me/rebolledodelatorre_bot" rel="noopener">@rebolledodelatorre_bot</a> escribiendo /ruta en un chat privado. Te pedirá tu permiso, el nombre de la ruta y una descripción corta, y saldrá aquí con su plano, su perfil y sus datos, con el reconocimiento que elijas. Al final podrás añadir hasta 3 fotos de la ruta (opcional): ten esas fotos a mano en el mismo dispositivo. '
                'Solo rutas que hayas grabado tú, por caminos públicos o con permiso. <a href="enviar-rutas.html#gpx">Guía paso a paso: cómo grabar el GPX</a>.</p></div></article>')
    if texto.startswith("@RUTA:"):
        id_ = texto[6:]
        try: svg, m, ru = fichas.ficha_html(id_)
        except FileNotFoundError: return f'<article class="tarjeta" id="{ident}"><div class="texto"><h3>{escape(titulo)}</h3><p>Ficha en preparación. {PEND}</p></div></article>'
        if ru.get("origen") == "comunidad":
            aut = f" Recorrido de {escape(ru['autor'].rstrip('.'))}." if ru.get("autor") else ""
            av = f'<p class="nota"><strong>Aviso:</strong> {escape(ru["avisos"])}</p>' if ru.get("avisos") else ""
            fot = ""
            if ru.get("fotos"):
                cred = f" · Foto: {escape(ru['autor'].rstrip('.'))}" if ru.get("autor") else ""
                fot = '<div class="fotos-ruta">' + "".join(f'<figure><img src="fotos-rutas/{escape(f["archivo"])}" alt="{escape(f["alt"])}" loading="lazy"><figcaption>{escape(ru["nombre"])}{cred}</figcaption></figure>' for f in ru["fotos"]) + '</div>'
            return (f'<article class="tarjeta ancha" id="{ident}"><div class="figuras una ficha">{svg}</div>{fot}<div class="texto"><h3>{escape(titulo)}</h3>'
                    f'<p>{escape(ru["subtitulo"])}. <span class="etiqueta">Recorrida por la comunidad</span>{aut}</p>{av}'
                    f'<p class="nota">Recorrido aportado con permiso de su autoría. ¿Quieres añadir el tuyo? <a href="enviar-rutas.html">Cómo aportar una ruta</a>. '
                    f'<a href="datos-rutas/{id_}.gpx" download>Descargar GPX</a></p></div></article>')
        return (f'<article class="tarjeta ancha" id="{ident}"><div class="figuras una ficha">{svg}</div><div class="texto"><h3>{escape(titulo)}</h3>'
                f'<p>{escape(ru["subtitulo"])}. <span class="etiqueta">Propuesta · por verificar</span></p>'
                + (f'<p class="nota">Llega hasta donde acaba el camino cartografiado: faltan unos {ru["faltan_m"]:.0f} m hasta {escape(ru["destino"])}, sin senda marcada en el mapa.</p>' if ru.get("faltan_m", 0) > 50 else '') +
                f'<p class="nota">Trazado calculado sobre los caminos de OpenStreetMap, aún sin recorrer. Si lo has andado y quieres confirmarlo o corregirlo, <a href="enviar-rutas.html">envíanos tu GPX</a>. '
                f'<a href="datos-rutas/{id_}.gpx" download>Descargar GPX</a></p></div></article>')
    if texto == "@PUNTOS":
        return (f'<article class="tarjeta ancha" id="{ident}"><div class="figuras una" style="background:#dfe6c8">{graficos.plano_observacion()}</div>'
                f'<div class="texto"><h3>{escape(titulo)}</h3><details open><summary>Cinco puntos candidatos</summary>{_puntos_txt()}</details></div></article>')
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
             "lunas": graficos.lunas, "respeto": graficos.respeto, "panorama": graficos.panorama_abierto, "geoparque": graficos.cielo_loras, "observatorios": graficos.telescopio}[nombre]
    else:
        g = graficos.GRAFICOS.get(ident) or graficos.POR_TITULO.get(titulo)
    fig = f'<figure>{g()}</figure>' if g else ""
    return f'<article class="tarjeta" id="{ident}">{fig}<div class="texto"><h3>{escape(titulo)}</h3><p>{texto}</p></div></article>'

def seccion(i, ident, nombre, subs):
    BANNER = ' banner' if ident == 'astro' else ''
    tarjetas = "\n      ".join(tarjeta(f"{ident}-{j+1}", t, x) for j, (t, x) in enumerate(subs))
    rama = '<svg class="trazo" viewBox="0 0 240 24" aria-hidden="true" focusable="false"><path pathLength="1" d="M2 18C30 18 40 4 70 8S110 22 140 14 190 2 238 10"/></svg>'
    return (f'  <section class="banda b{i % 3} sec" id="{ident}" data-nombre="{escape(nombre)}" data-lead="{escape(LEADS[ident])}" aria-labelledby="h-{ident}">\n'
            f'    <div class="envoltorio">\n      <div class="titulo"><h2 id="h-{ident}">{escape(nombre)}</h2></div>\n'
            f'      <p class="lead">{LEADS[ident]}</p>\n      <div class="rejilla{BANNER}">\n      {tarjetas}\n      </div>\n    </div>\n  </section>\n')

def cinta_avisos():
    """Cinta estrecha y negra bajo el vídeo con las entradas de «Avisos y ayudas»; al pulsar el texto se abre la entrada ampliada dentro de la web."""
    items = AVISOS.get("items", [])[:10] if isinstance(AVISOS, dict) else []
    if not items: return ""
    li = "".join(f'<a class="cinta-item{" activo" if i == 0 else ""}" href="#avisos-{i + 2}"><span class="cinta-cat">{escape(CATEGORIAS_AVISOS.get([k for k in a["categorias"] if k != "noticias"][0] if [k for k in a["categorias"] if k != "noticias"] else a["categorias"][0], ""))}</span> {escape(_recorta(a["titulo_natural"], 150))}</a>' for i, a in enumerate(items))
    return (f'<div class="cinta" role="region" aria-label="Últimos avisos y ayudas"><a class="cinta-etq" href="#avisos">Avisos y ayudas</a><div class="cinta-pista">{li}</div>'
            f'<button type="button" class="cinta-b" data-d="-1" aria-label="Aviso anterior">‹</button><button type="button" class="cinta-b" data-d="1" aria-label="Aviso siguiente">›</button></div>')


def cinta_huerta():
    """Segunda cinta negra, el doble de alta, con foto pequeña: lo que toca en la huerta este mes y el próximo; cada entrada lleva a su ficha."""
    items = huerta_web.banner_items()
    if not items: return ""
    li = "".join(f'<a class="cinta-item{" activo" if i == 0 else ""}" href="{it["enlace"]}"><img src="{escape(it["foto"])}" alt="" width="64" height="64" loading="lazy">'
                 f'<span class="cinta-txt"><strong>{escape(it["titulo"])}</strong><span>{escape(it["texto"])}</span></span></a>' for i, it in enumerate(items))
    return (f'<div class="cinta cinta2" data-ms="21000" role="region" aria-label="Lo que toca en la huerta"><a class="cinta-etq" href="#huerta">En la huerta</a><div class="cinta-pista">{li}</div>'
            f'<button type="button" class="cinta-b" data-d="-1" aria-label="Anterior">‹</button><button type="button" class="cinta-b" data-d="1" aria-label="Siguiente">›</button></div>')


def pagina_creditos():
    """creditos-fotos.html: autoría y licencia de cada foto de ejemplo (Wikimedia Commons)."""
    import re
    fot = {}
    try: fot = json.loads((Path(__file__).parent / "naturaleza" / "fotos.json").read_text())
    except Exception: pass
    li = ""
    for nombre, f in sorted(fot.items(), key=lambda kv: kv[0].lower()):
        if not f.get("archivo"): continue
        lic = f'<a href="{escape(f["url_licencia"])}" rel="noopener">{escape(f["licencia"])}</a>' if f.get("url_licencia") else escape(f["licencia"])
        li += f'<li><strong>{escape(nombre)}</strong> — {escape(f["autor"])} · {lic} · <a href="{escape(f["pagina"])}" rel="noopener">archivo original en Wikimedia Commons</a></li>\n'
    try: hf = json.loads((Path(__file__).parent / "huerta" / "fotos.json").read_text())
    except Exception: hf = {}
    try: hd = json.loads((Path(__file__).parent / "huerta" / "datos.json").read_text()); nom = {e["id"]: e["nombre"] for e in hd["especies"] + hd["flores"]}
    except Exception: nom = {}
    for i, f in sorted(hf.items(), key=lambda kv: nom.get(kv[0], kv[0]).lower()):
        if not f.get("archivo"): continue
        lic = f'<a href="{escape(f["url_licencia"])}" rel="noopener">{escape(f["licencia"])}</a>' if f.get("url_licencia") else escape(f["licencia"])
        li += f'<li><strong>{escape(nom.get(i, i))}</strong> (huerta) — {escape(f["autor"])} · {lic} · <a href="{escape(f["pagina"])}" rel="noopener">archivo original en Wikimedia Commons</a></li>\n'
    base = (Path(__file__).parent / "enviar-fotos.html").read_text()
    pag = re.sub(r"<title>.*?</title>", "<title>Créditos de las fotografías · Rebolledo de la Torre</title>", base)
    pag = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="Autoría y licencia de cada fotografía de ejemplo de la sección Fauna y flora.">', pag)
    i, j = pag.index("<main"), pag.index("</main>")
    cuerpo = ('<main id="contenido" class="envoltorio legal">\n  <p><a href="index.html">← Volver a la página principal</a></p>\n  <h1>Créditos de las fotografías</h1>\n'
              '  <p>Las fotos de ejemplo de la sección <strong>Fauna y flora</strong> vienen de <a href="https://commons.wikimedia.org" rel="noopener">Wikimedia Commons</a> y tienen licencia libre '
              '(dominio público, CC0, CC BY o CC BY-SA). Se muestran reducidas de tamaño y siempre con su autoría. Son ejemplos de cada especie, no fotos tomadas en Rebolledo: '
              'las fotos del pueblo irán entrando por el bot, con permiso de quien las haga.</p>\n  <ul class="guia">\n' + li + '  </ul>\n')
    (Path(__file__).parent / "creditos-fotos.html").write_text(pag[:i] + cuerpo + pag[j:])


def barra_html(pref=""):
    """Barra superior con menús desplegables (hiedra que baja al abrir). pref = "" en la portada, "index.html" en el resto de páginas."""
    items = ""
    for ident, nombre, subs in CONTENIDO:
        enl = "".join(f'<a href="{pref}#{ident}-{j+1}">{escape(t)}</a>' for j, (t, _) in enumerate(subs))
        items += (f'<details class="menu" name="menu"><summary data-sec="{ident}">{escape(nombre)}</summary>'
                  f'<div class="sub"><a class="todo" href="{pref}#{ident}">Ver toda la sección</a>{enl}</div></details>')
    ini = f'<a href="{pref or "#inicio"}" data-sec="inicio">Inicio</a>' if pref else '<a href="#inicio" data-sec="inicio">Inicio</a>'
    marca = (f'<a class="marca" href="{pref or "#inicio"}">Rebolledo de la Torre</a>'
             f'<div class="tiempo-cab"><span class="t-ahora" hidden></span><span class="t-manana" hidden></span></div>')
    return f'<header class="barra">\n  {marca}\n  <nav class="navtop" aria-label="Secciones">{ini}{items}</nav>\n</header>\n'


def parchea_paginas():
    """Pone la misma barra (con index.html# en los enlaces) en las páginas fijas, y deja un fragmento para la galería que genera el bot."""
    import re
    base = Path(__file__).parent
    barra = barra_html("index.html")
    for f in ("aviso-legal", "privacidad", "accesibilidad", "colabora", "enviar-fotos", "enviar-rutas", "contar-fiestas", "creditos-fotos"):
        p = base / f"{f}.html"
        if p.exists():
            t = p.read_text()
            t2 = re.sub(r'<header class="barra">.*?</header>\n', lambda m: barra, t, flags=re.S)
            if "js/tiempo.js" not in t2: t2 = t2.replace("</body>", '<script src="js/tiempo.js" defer></script>\n</body>', 1)
            if t2 != t: p.write_text(t2)
    (base / "barra-pagina.html").write_text(barra)


def main():
    try: _nf = json.loads((Path(__file__).parent / "naturaleza" / "fotos.json").read_text())
    except Exception: _nf = {}
    fotos_piedras = "|".join("naturaleza/" + f["archivo"] for f in _nf.values() if f.get("archivo") and "habitat" not in f["archivo"])
    cinta = '<div class="cintas">' + cinta_huerta() + cinta_avisos() + '</div>'
    tabs = "".join(f'<a href="#{c[0]}" data-sec="{c[0]}">{escape(c[1])}</a>' for c in CONTENIDO)
    navtop = '<a href="#inicio" data-sec="inicio">Inicio</a>' + tabs
    secciones = "".join(seccion(i, *c) for i, c in enumerate(CONTENIDO))
    pagina = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rebolledo de la Torre · Naturaleza, historia y estrellas</title>
<meta name="description" content="Página comunitaria no oficial sobre Rebolledo de la Torre (Burgos): rutas, cielo nocturno, patrimonio y comunidad.">
<meta name="theme-color" content="#4a3526">
<link rel="stylesheet" href="css/estilo.css">
<link rel="stylesheet" href="css/roble.css">
</head>
<body>
<a class="salto" href="#contenido">Saltar al contenido</a>
{rama_fondo()}
{barra_html()}

<main id="contenido">
  <div class="marco-arco" data-fotos="{fotos_piedras}">
    <div class="pilar" aria-hidden="true"></div>
    <div class="centro">
      <section class="portada" id="inicio">
        <video autoplay muted loop playsinline controls preload="auto" poster="media/cielo-nocturno.jpg" aria-label="Cielo nocturno sobre Rebolledo de la Torre (vídeo sin sonido)">
          <source src="media/cielo-nocturno.mp4" type="video/mp4">
        </video>
        <div class="portada-texto">
          <h1>Rebolledo de la Torre</h1>
          <p>Naturaleza, historia y estrellas</p>
        </div>
      </section>
      {cinta}
      <p class="aviso"><strong>Importante:</strong> esta web es un proyecto comunitario y <strong>no es la web oficial del Ayuntamiento</strong>. Para trámites, avisos oficiales o información municipal, consulte al Ayuntamiento (<a href="https://www.rebolledodelatorre.es" rel="noopener">rebolledodelatorre.es</a>).</p>
      <section id="carrusel" class="carrusel" aria-roledescription="carrusel" aria-label="Secciones del portal">
        <div class="caja" data-par="0">
          <div class="diap" aria-live="off"></div>
          <div class="controles">
            <button type="button" class="flecha" data-dir="-1" aria-label="Anterior">‹</button>
            <button type="button" class="pausa" aria-pressed="false">⏸ Pausar</button>
            <button type="button" class="flecha" data-dir="1" aria-label="Siguiente">›</button>
          </div>
        </div>
      </section>
    </div>
    <div class="pilar" aria-hidden="true"></div>
  </div>
  <nav class="tabs" aria-label="Secciones">{tabs}</nav>

  <div id="almacen">
{secciones}  </div>
</main>

<footer class="pie">
  <div class="envoltorio">
    <p>Proyecto comunitario sin ánimo de lucro. Sin cookies, sin analítica, sin publicidad y sin recoger datos personales. Vídeo de portada con permiso de su autor. Datos del tiempo: Open-Meteo.com (CC BY 4.0). Avisos: BOE y BOCYL, con enlace al texto oficial.</p>
    <ul>
      <li><a href="enviar-fotos.html">Enviar fotos</a></li>
      <li><a href="enviar-rutas.html">Enviar una ruta</a></li>
      <li><a href="galeria.html">Galería</a></li>
      <li><a href="creditos-fotos.html">Créditos de las fotos</a></li>
      <li><a href="aviso-legal.html">Aviso legal</a></li>
      <li><a href="privacidad.html">Privacidad y cookies</a></li>
      <li><a href="accesibilidad.html">Accesibilidad</a></li>
    </ul>
  </div>
</footer>
<a class="volver" href="#inicio">↑ Volver al inicio</a>
<script src="js/carrusel.js" defer></script>
<script src="js/tiempo.js" defer></script>
</body>
</html>
"""
    Path(__file__).with_name("index.html").write_text(pagina)
    pagina_creditos()
    parchea_paginas()
    print("index.html generado")


if __name__ == "__main__":
    main()
