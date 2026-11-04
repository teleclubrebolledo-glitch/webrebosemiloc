"""Gráficos vectoriales propios (SVG en línea, sin imágenes de terceros ni JavaScript) para las tarjetas-arco.
Todo es dibujo original: nada procede de fotos ni de bancos de imágenes. Las cartas del cielo son ESQUEMÁTICAS
(posiciones de estrellas redondeadas, para orientarse a ojo; no sustituyen a un planetario)."""
import math
from html import escape

NOCHE, NOCHE2 = "#0f1d3d", "#26407a"
VERDE, VERDE_OSC, CLARO, TRIGO, PIEDRA, ROJO = "#2e5a2b", "#1f3d1c", "#e3eed6", "#e0b341", "#b9a98a", "#c0392b"


def _svg(cuerpo, etiqueta, vb="0 0 300 200", extra=""):
    return (f'<svg viewBox="{vb}" role="img" aria-label="{escape(etiqueta)}" focusable="false" {extra}>'
            f'<title>{escape(etiqueta)}</title>{cuerpo}</svg>')


def _estrellas(n, w, h, seed, tope=None):
    out, x = [], seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2**31; px = x % w
        x = (x * 1103515245 + 12345) % 2**31; py = x % (tope or h)
        x = (x * 1103515245 + 12345) % 2**31; r = .5 + (x % 100) / 100 * 1.1
        out.append(f'<circle cx="{px}" cy="{py}" r="{r:.1f}" fill="#fff" opacity="{.55 + (x % 40) / 100:.2f}"/>')
    return "".join(out)


def _cielo(id_, c1=NOCHE, c2=NOCHE2):
    return (f'<defs><linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="300" height="200" fill="url(#{id_})"/>')


# ───────────── RUTAS ─────────────
def peña_mesa():
    c = (f'<rect width="300" height="200" fill="{CLARO}"/><circle cx="228" cy="52" r="20" fill="{TRIGO}"/>'
         f'<path d="M0 150 L70 110 L96 118 L128 70 H206 L236 118 L300 130 V200 H0Z" fill="{PIEDRA}"/>'
         f'<path d="M128 70 H206 L212 82 H122Z" fill="#cdbf9f"/>'
         f'<path d="M0 168 C60 150 110 175 170 160 S260 150 300 165 V200 H0Z" fill="{VERDE}"/>'
         f'<path d="M40 190 C90 170 120 182 150 150 S190 120 168 84" fill="none" stroke="#fff" stroke-width="2.6" stroke-dasharray="2 6" stroke-linecap="round"/>'
         f'<circle cx="168" cy="84" r="4" fill="{ROJO}"/>')
    return _svg(c, "Dibujo de una peña de cima plana con un sendero que sube hasta ella")


def tuerces():
    pin = "".join(f'<path d="M{x} 200 C{x+2} 150 {x-6} 120 {x+4} {y} C{x+16} {y-6} {x+20} 150 {x+26} 200Z" fill="{col}"/>'
                  for x, y, col in [(40, 70, PIEDRA), (92, 40, "#a99876"), (150, 62, PIEDRA), (206, 34, "#a99876"), (250, 78, PIEDRA)])
    c = f'<rect width="300" height="200" fill="#f3ead2"/><circle cx="60" cy="40" r="16" fill="{TRIGO}"/>{pin}<rect y="184" width="300" height="16" fill="{VERDE}"/>'
    return _svg(c, "Dibujo de formas rocosas esculpidas por el agua y el viento")


def loras():
    c = (f'<rect width="300" height="200" fill="{CLARO}"/>'
         f'<path d="M0 100 H70 L84 112 V130 H180 L194 96 H300 V200 H0Z" fill="{PIEDRA}"/>'
         f'<path d="M0 160 C70 140 130 170 200 150 S270 148 300 156 V200 H0Z" fill="{VERDE}"/>'
         f'<path d="M0 182 C80 170 150 190 300 176 V200 H0Z" fill="{VERDE_OSC}"/>'
         f'<path d="M205 52 q8 -9 16 0 q8 -9 16 0" fill="none" stroke="{VERDE_OSC}" stroke-width="2.4" stroke-linecap="round"/>'
         f'<path d="M244 38 q6 -7 12 0 q6 -7 12 0" fill="none" stroke="{VERDE_OSC}" stroke-width="2" stroke-linecap="round"/>')
    return _svg(c, "Dibujo de un valle con páramos de cima plana (las loras) y aves en el cielo")


def romanico():
    arcos = "".join(f'<path d="M{x} 170 V112 A18 18 0 0 1 {x+36} 112 V170Z" fill="{CLARO}" stroke="{VERDE_OSC}" stroke-width="3"/>'
                    f'<path d="M{x+8} 170 V114 A10 10 0 0 1 {x+28} 114 V170Z" fill="{NOCHE}" opacity=".85"/>' for x in (44, 92, 140, 188))
    c = (f'<rect width="300" height="200" fill="#f3ead2"/><rect x="30" y="86" width="240" height="14" fill="{PIEDRA}"/>'
         f'<rect x="30" y="170" width="240" height="14" fill="{PIEDRA}"/>{arcos}')
    return _svg(c, "Dibujo de una galería de cuatro arcos de medio punto, como las del románico")


# ───────────── ASTROTURISMO ─────────────
def cielo_loras():
    c = (_cielo("g1") + _estrellas(70, 300, 130, 7)
         + f'<path d="M-10 90 C60 40 160 60 320 20 L320 62 C180 100 90 80 -10 130Z" fill="#fff" opacity=".12"/>'
         f'<path d="M0 160 H64 L76 172 V176 H170 L182 150 H300 V200 H0Z" fill="{VERDE_OSC}"/>')
    return _svg(c, "Dibujo del cielo estrellado con la Vía Láctea sobre el perfil de las loras")


def telescopio():
    c = (_cielo("g2") + _estrellas(40, 300, 120, 3)
         + f'<g stroke="#e8ecf5" stroke-width="5" stroke-linecap="round"><path d="M150 140 L116 196"/><path d="M150 140 L184 196"/><path d="M150 140 L150 198"/></g>'
         f'<g transform="rotate(-42 150 134)"><rect x="96" y="122" width="108" height="24" rx="6" fill="#e8ecf5"/><rect x="190" y="118" width="22" height="32" rx="5" fill="{TRIGO}"/>'
         f'<rect x="76" y="128" width="26" height="12" rx="4" fill="#9fb0d0"/></g><circle cx="150" cy="138" r="10" fill="#9fb0d0"/>')
    return _svg(c, "Dibujo de un telescopio sobre un trípode apuntando al cielo nocturno")


def respeto():
    c = (_cielo("g3") + _estrellas(50, 300, 150, 11)
         + f'<path d="M232 46 a26 26 0 1 0 8 40 a20 20 0 1 1 -8 -40Z" fill="#f6efd2"/>'
         f'<path d="M0 168 C80 150 160 176 300 160 V200 H0Z" fill="{VERDE_OSC}"/>'
         f'<g transform="translate(88 138)"><rect x="0" y="0" width="14" height="40" rx="4" fill="#555"/><path d="M-3 0 H17 L24 -12 H-10Z" fill="#777"/>'
         f'<path d="M24 -12 L120 -48 L120 12Z" fill="{ROJO}" opacity=".35"/></g>')
    return _svg(c, "Dibujo de una linterna de luz roja, que no estropea la visión nocturna, bajo la Luna")


# ───────────── PATRIMONIO ─────────────
def iglesia():
    c = (f'<rect width="300" height="200" fill="#f3ead2"/><g transform="translate(14 22) scale(.86)"><rect x="40" y="120" width="220" height="64" fill="{PIEDRA}"/>'
         + "".join(f'<path d="M{x} 184 V150 A9 9 0 0 1 {x+18} 150 V184Z" fill="{NOCHE}"/>' for x in (66, 100, 134, 168, 202))
         + f'<rect x="60" y="112" width="190" height="10" fill="#a99876"/><path d="M40 120 L150 76 L260 120Z" fill="{ROJO}" opacity=".85"/>'
         f'<rect x="236" y="40" width="34" height="90" fill="#a99876"/><path d="M236 40 L253 18 L270 40Z" fill="{VERDE_OSC}"/>'
         f'<path d="M248 70 V58 A5 5 0 0 1 258 58 V70Z" fill="{NOCHE}"/></g>')
    return _svg(c, "Dibujo de una iglesia románica con galería de arcos y torre")


def torre():
    c = (_cielo("g4", "#f7edcb", "#e3eed6")
         + f'<rect x="120" y="60" width="62" height="126" fill="{PIEDRA}"/>'
         + "".join(f'<rect x="{120+i*16}" y="48" width="12" height="14" fill="{PIEDRA}"/>' for i in range(4))
         + f'<path d="M142 186 V158 A9 9 0 0 1 160 158 V186Z" fill="{NOCHE}"/><rect x="143" y="86" width="16" height="22" rx="8" fill="{NOCHE}"/>'
         f'<path d="M0 186 C80 172 200 190 300 176 V200 H0Z" fill="{VERDE}"/>')
    return _svg(c, "Dibujo de una torre medieval con almenas sobre el caserío")


def costumbres():
    c = (f'<rect width="300" height="200" fill="#f7edcb"/><path d="M0 170 C80 150 160 176 300 160 V200 H0Z" fill="{VERDE}"/>'
         f'<path d="M150 150 C100 130 110 80 150 56 C190 80 200 130 150 150Z" fill="{ROJO}" opacity=".9"/>'
         f'<path d="M150 150 C140 120 146 90 150 64" stroke="{TRIGO}" stroke-width="3" fill="none"/>'
         + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="{TRIGO}"/>' for x, y in [(70, 60), (230, 70), (96, 36), (210, 34), (50, 110), (252, 112)]))
    return _svg(c, "Dibujo de una hoguera de fiesta con chispas")


# ───────────── EVENTOS / COMUNIDAD / VISITAR ─────────────
def eclipse():
    c = (_cielo("g5", "#16254a", "#4a6aa8") + _estrellas(18, 300, 100, 5)
         + f'<circle cx="150" cy="96" r="44" fill="{TRIGO}"/><circle cx="168" cy="90" r="42" fill="#0b1226"/>'
         f'<path d="M0 170 C80 156 160 178 300 164 V200 H0Z" fill="{VERDE_OSC}"/>')
    return _svg(c, "Dibujo de un eclipse de Sol, con la Luna cubriendo casi todo el disco")


def evento():
    c = (f'<rect width="300" height="200" fill="#f3ead2"/><rect x="92" y="44" width="116" height="108" rx="10" fill="#fff" stroke="{VERDE}" stroke-width="4"/>'
         f'<rect x="92" y="44" width="116" height="26" rx="10" fill="{VERDE}"/>'
         + "".join(f'<circle cx="{110+i*20}" cy="{96+j*20}" r="3" fill="{PIEDRA}"/>' for i in range(5) for j in range(3))
         + f'<circle cx="170" cy="116" r="9" fill="none" stroke="{ROJO}" stroke-width="3"/>')
    return _svg(c, "Dibujo de un calendario con un día marcado")


def telegram():
    c = (f'<rect width="300" height="200" fill="{CLARO}"/><path d="M52 150 L252 56 L214 160 L168 126 L146 150 L142 118Z" fill="#fff" stroke="{VERDE}" stroke-width="4" stroke-linejoin="round"/>'
         f'<path d="M142 118 L252 56" stroke="{VERDE}" stroke-width="4"/>')
    return _svg(c, "Dibujo de un avión de papel, como los mensajes de los canales")


def fotos():
    c = (f'<rect width="300" height="200" fill="#f3ead2"/><rect x="62" y="56" width="176" height="104" rx="12" fill="{VERDE_OSC}"/>'
         f'<circle cx="150" cy="108" r="34" fill="#fff"/><circle cx="150" cy="108" r="22" fill="{NOCHE2}"/><circle cx="142" cy="100" r="6" fill="#fff" opacity=".7"/>'
         f'<rect x="108" y="44" width="40" height="16" rx="4" fill="{VERDE_OSC}"/><circle cx="214" cy="76" r="5" fill="{TRIGO}"/>')
    return _svg(c, "Dibujo de una cámara de fotos")


def galeria():
    c = (f'<rect width="300" height="200" fill="{CLARO}"/>'
         + "".join(f'<rect x="{x}" y="{y}" width="64" height="48" rx="4" fill="#fff" stroke="{VERDE}" stroke-width="3"/>'
                   f'<path d="M{x+6} {y+42} L{x+26} {y+20} L{x+40} {y+34} L{x+50} {y+26} L{x+58} {y+42}Z" fill="{VERDE}" opacity=".8"/>'
                   for x, y in [(50, 40), (118, 62), (186, 40), (84, 112), (152, 124)]))
    return _svg(c, "Dibujo de varias fotografías enmarcadas")


def mapa():
    c = (f'<rect width="300" height="200" fill="#f3ead2"/><path d="M0 120 C70 90 120 150 200 110 S280 100 300 116" fill="none" stroke="{PIEDRA}" stroke-width="10" stroke-linecap="round"/>'
         f'<path d="M0 120 C70 90 120 150 200 110 S280 100 300 116" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="8 8"/>'
         f'<path d="M150 150 C120 110 124 76 150 58 C176 76 180 110 150 150Z" fill="{ROJO}"/><circle cx="150" cy="92" r="11" fill="#fff"/>')
    return _svg(c, "Dibujo de un mapa con un camino y un punto marcado")


def tiempo():
    c = (_cielo("g6", "#bcd6ef", "#e8f1fb") + f'<circle cx="104" cy="70" r="28" fill="{TRIGO}"/>'
         f'<g fill="#fff"><circle cx="150" cy="104" r="26"/><circle cx="182" cy="96" r="32"/><circle cx="214" cy="108" r="24"/><rect x="150" y="104" width="64" height="28"/></g>'
         f'<path d="M150 140 q0 10 -5 14 M182 144 q0 10 -5 14 M212 140 q0 10 -5 14" stroke="#6c8fc0" stroke-width="3" fill="none" stroke-linecap="round"/>')
    return _svg(c, "Dibujo del Sol asomando entre nubes")


def contacto():
    c = (f'<rect width="300" height="200" fill="{CLARO}"/><rect x="66" y="58" width="168" height="104" rx="8" fill="#fff" stroke="{VERDE}" stroke-width="4"/>'
         f'<path d="M66 66 L150 122 L234 66" fill="none" stroke="{VERDE}" stroke-width="4" stroke-linejoin="round"/>')
    return _svg(c, "Dibujo de un sobre de correo")


# ───────────── CARTA DEL CIELO: orientar el telescopio desde Rebolledo ─────────────
LAT = 42.6889   # latitud de Rebolledo de la Torre
# (nombre, AR en horas, Dec en grados): coordenadas redondeadas, para un esquema
ESTRELLAS = {
    "Polar": (2.53, 89.26), "Dubhe": (11.06, 61.75), "Merak": (11.03, 56.38), "Phecda": (11.90, 53.69),
    "Megrez": (12.26, 57.03), "Alioth": (12.90, 55.96), "Mizar": (13.40, 54.93), "Alkaid": (13.79, 49.31),
    "Caph": (0.15, 59.15), "Schedar": (0.68, 56.54), "γ Cas": (0.95, 60.72), "Ruchbah": (1.43, 60.24), "Segin": (1.91, 63.67),
}
CARRO = ["Dubhe", "Merak", "Phecda", "Megrez", "Alioth", "Mizar", "Alkaid"]
CASIOPEA = ["Caph", "Schedar", "γ Cas", "Ruchbah", "Segin"]
DOBLE_CUMULO = (2.33, 57.14)   # h y χ Persei, entre Casiopea y Perseo


def carta_polar():
    cx, cy, k, giro = 230, 212, 3.55, -100
    def pos(ra, dec):
        r, a = (90 - dec) * k, math.radians(ra * 15 + giro)
        return cx + r * math.cos(a), cy - r * math.sin(a)
    P = {n: pos(*v) for n, v in ESTRELLAS.items()}
    aros = "".join(f'<circle cx="{cx}" cy="{cy}" r="{(90-d)*k:.0f}" fill="none" stroke="#fff" stroke-opacity=".2" stroke-dasharray="3 5"/>'
                   f'<text x="{cx+4}" y="{cy-(90-d)*k+12:.0f}" fill="#bcd0f2" font-size="10" font-family="system-ui,sans-serif">+{d}°</text>' for d in (80, 70, 60, 50))
    def linea(lista, col):
        pts = " ".join(f"{P[n][0]:.1f},{P[n][1]:.1f}" for n in lista)
        return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>'
    def punto(n, r=4):
        x, y = P[n]; return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fff"/>'
    # indicadoras del Carro: de Merak a Dubhe y 5 veces esa distancia hasta la Polar
    mx, my = P["Merak"]; dx, dy = P["Dubhe"]
    ind = f'<line x1="{mx:.1f}" y1="{my:.1f}" x2="{cx}" y2="{cy}" stroke="{TRIGO}" stroke-width="2.4" stroke-dasharray="6 5"/>'
    dcx, dcy = pos(*DOBLE_CUMULO)
    doble = (f'<circle cx="{dcx:.1f}" cy="{dcy:.1f}" r="9" fill="none" stroke="{ROJO}" stroke-width="2"/>'
             f'<text x="{dcx+14:.1f}" y="{dcy+4:.1f}" fill="#ffb4a8" font-size="11" font-family="system-ui,sans-serif">Doble Cúmulo</text>')
    etq = lambda n, dx_, dy_: f'<text x="{P[n][0]+dx_:.1f}" y="{P[n][1]+dy_:.1f}" fill="#fff" font-size="11" font-family="system-ui,sans-serif">{n}</text>'
    cuerpo = (f'<rect width="460" height="420" fill="{NOCHE}"/>' + _estrellas(60, 460, 420, 21) + aros
              + linea(CARRO, "#9fb8ee") + linea(CASIOPEA, "#9fb8ee") + ind + doble
              + "".join(punto(n) for n in ESTRELLAS if n != "Polar") + f'<circle cx="{cx}" cy="{cy}" r="6" fill="{TRIGO}"/>'
              + etq("Polar", 10, -8) + etq("Dubhe", 8, -6) + etq("Merak", -40, 14) + etq("Alkaid", 8, 14) + etq("Schedar", -8, 22) + etq("Caph", -30, 4)
              + f'<text x="54" y="40" fill="#fff" font-size="14" font-weight="700" font-family="system-ui,sans-serif">Mirando al norte</text>'
              f'<text x="54" y="58" fill="#bcd0f2" font-size="11" font-family="system-ui,sans-serif">Esquema: el cielo gira cada noche alrededor de la Polar</text>')
    return _svg(cuerpo, "Carta del cielo del norte: el Carro y Casiopea a ambos lados de la Estrella Polar, con la línea que une Merak y Dubhe señalándola y el Doble Cúmulo de Perseo entre Casiopea y Perseo", vb="0 0 460 420")


def montura():
    """Perfil de una montura ecuatorial: el eje polar se inclina como la latitud (42,7°)."""
    ang = LAT
    ox, oy, L = 120, 330, 230
    a = math.radians(ang)
    tx, ty = ox + L * math.cos(a), oy - L * math.sin(a)       # eje polar apuntando al norte (a la derecha)
    arco = f"M{ox+90} {oy} A90 90 0 0 0 {ox+90*math.cos(a):.1f} {oy-90*math.sin(a):.1f}"
    cuerpo = (f'<rect width="460" height="420" fill="#eaf1f8"/><rect y="{oy}" width="460" height="90" fill="{VERDE}"/>'
              f'<line x1="{ox-30}" y1="{oy}" x2="{ox+300}" y2="{oy}" stroke="{VERDE_OSC}" stroke-width="2" stroke-dasharray="6 5"/>'
              f'<text x="{ox+232}" y="{oy-8}" fill="{VERDE_OSC}" font-size="12" font-family="system-ui,sans-serif">horizonte norte</text>'
              f'<g stroke="#555" stroke-width="6" stroke-linecap="round"><line x1="{ox}" y1="{oy}" x2="{ox-34}" y2="{oy+40}"/><line x1="{ox}" y1="{oy}" x2="{ox+34}" y2="{oy+40}"/><line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy+44}"/></g>'
              f'<line x1="{ox}" y1="{oy}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{NOCHE2}" stroke-width="10" stroke-linecap="round"/>'
              f'<path d="{arco}" fill="none" stroke="{ROJO}" stroke-width="3"/>'
              f'<text x="{ox+98}" y="{oy-22}" fill="{ROJO}" font-size="18" font-weight="700" font-family="system-ui,sans-serif">{ang:.1f}°</text>'
              f'<circle cx="{tx+14:.1f}" cy="{ty-10:.1f}" r="7" fill="{TRIGO}"/>'
              f'<text x="{tx-70:.1f}" y="{ty-24:.1f}" fill="{VERDE_OSC}" font-size="12" font-family="system-ui,sans-serif">Estrella Polar</text>'
              f'<text x="14" y="24" fill="{VERDE_OSC}" font-size="14" font-weight="700" font-family="system-ui,sans-serif">Montura ecuatorial vista de perfil</text>')
    return _svg(cuerpo, f"Perfil de una montura ecuatorial cuyo eje polar se inclina {ang:.1f} grados sobre el horizonte norte, apuntando a la Estrella Polar", vb="0 0 460 420")


GRAFICOS = {
    "rutas-1": peña_mesa, "rutas-2": tuerces, "rutas-3": loras, "rutas-4": romanico,
    "astro-1": cielo_loras, "astro-2": telescopio, "astro-4": respeto,
    "patrimonio-1": iglesia, "patrimonio-2": torre, "patrimonio-3": costumbres,
    "eventos-1": eclipse, "eventos-2": evento,
    "comunidad-1": telegram, "comunidad-2": fotos, "comunidad-3": galeria,
    "visitar-1": mapa, "visitar-2": tiempo, "visitar-3": contacto,
}

if __name__ == "__main__":
    from pathlib import Path
    out = Path("/tmp/graf-prueba.html")
    out.write_text("<body style='background:#ddd;display:grid;grid-template-columns:repeat(4,300px);gap:8px'>"
                   + "".join(f for f in (g() for g in GRAFICOS.values())) + carta_polar() + montura() + "</body>")
