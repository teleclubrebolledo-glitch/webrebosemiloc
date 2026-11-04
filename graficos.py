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
    "astro-1": cielo_loras, "astro-2": telescopio,
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


# ═════════════ MÁS ASTRO-TURISMO (cálculos propios desde la latitud de Rebolledo) ═════════════
EPS = 23.44   # oblicuidad de la eclíptica (grados)


def _sol(dec_deg, lat=LAT):
    """Altura máxima, acimutes de salida/puesta y duración geométrica del día (sin refracción)."""
    f, d = math.radians(lat), math.radians(dec_deg)
    alt_max = 90 - abs(lat - dec_deg)
    az_sal = math.degrees(math.acos(math.sin(d) / math.cos(f)))
    h = math.degrees(math.acos(-math.tan(f) * math.tan(d)))
    return alt_max, az_sal, 2 * h / 15, h


def _curva_sol(dec_deg, lat=LAT, paso=3):
    f, d = math.radians(lat), math.radians(dec_deg)
    _, _, _, H0 = _sol(dec_deg, lat)
    pts = []
    for h in range(int(-H0), int(H0) + 1, paso):
        H = math.radians(h)
        alt = math.degrees(math.asin(math.sin(f) * math.sin(d) + math.cos(f) * math.cos(d) * math.cos(H)))
        az = math.degrees(math.atan2(-math.sin(H), math.tan(d) * math.cos(f) - math.sin(f) * math.cos(H))) % 360
        pts.append((az, alt))
    return pts


def camino_sol():
    X0, X1, Y0, Y1, A0, A1, ALT = 56, 436, 40, 300, 40, 320, 80
    px = lambda az: X0 + (az - A0) / (A1 - A0) * (X1 - X0)
    py = lambda alt: Y1 - alt / ALT * (Y1 - Y0)
    cuerpo = f'<rect width="460" height="340" fill="#eaf1f8"/><rect x="{X0}" y="{Y1}" width="{X1-X0}" height="26" fill="{VERDE}"/>'
    for a in range(0, 81, 20):
        cuerpo += (f'<line x1="{X0}" y1="{py(a):.0f}" x2="{X1}" y2="{py(a):.0f}" stroke="#9db4cf" stroke-width="1" stroke-dasharray="3 5"/>'
                   f'<text x="{X0-8}" y="{py(a)+4:.0f}" text-anchor="end" fill="{VERDE_OSC}" font-size="11" font-family="system-ui,sans-serif">{a}°</text>')
    for az, nom in ((90, "Este"), (180, "Sur"), (270, "Oeste")):
        cuerpo += (f'<line x1="{px(az):.0f}" y1="{Y0}" x2="{px(az):.0f}" y2="{Y1}" stroke="#9db4cf" stroke-width="1" stroke-dasharray="3 5"/>'
                   f'<text x="{px(az):.0f}" y="{Y1+18}" text-anchor="middle" fill="#fff" font-size="12" font-weight="700" font-family="system-ui,sans-serif">{nom}</text>')
    filas = []
    for dec, nom, col in ((EPS, "Solsticio de verano", ROJO), (0, "Equinoccios", TRIGO), (-EPS, "Solsticio de invierno", NOCHE2)):
        alt, az, dur, _ = _sol(dec)
        pts = " ".join(f"{px(a):.1f},{py(h):.1f}" for a, h in _curva_sol(dec))
        cuerpo += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
        cuerpo += f'<text x="{px(180):.0f}" y="{py(alt)-7:.0f}" text-anchor="middle" fill="{col}" font-size="12" font-weight="700" font-family="system-ui,sans-serif">{alt:.0f}°</text>'
        filas.append((nom, alt, az, dur, col))
    cuerpo += f'<text x="14" y="22" fill="{VERDE_OSC}" font-size="14" font-weight="700" font-family="system-ui,sans-serif">Altura del Sol según el rumbo</text>'
    return _svg(cuerpo, "Gráfico de la altura del Sol sobre el horizonte, de este a oeste, en los solsticios y en los equinoccios, calculado para la latitud de Rebolledo", vb="0 0 460 340"), filas


def altura_ladder():
    izq = [(90, "Cenit"), (LAT, "Estrella Polar")]
    der = [(70.8, "Sol de verano"), (47.3, "Sol de equinoccio"), (23.9, "Sol de invierno")]
    X, Y0, Y1 = 150, 34, 172
    py = lambda a: Y1 - a / 90 * (Y1 - Y0)
    c = _cielo("g7") + _estrellas(22, 300, 150, 41) + f'<rect y="{Y1}" width="300" height="30" fill="{VERDE_OSC}"/>'
    c += f'<line x1="{X}" y1="{Y0}" x2="{X}" y2="{Y1}" stroke="#fff" stroke-opacity=".55" stroke-width="2"/>'
    for a in range(0, 91, 10):
        c += f'<line x1="{X-5}" y1="{py(a):.1f}" x2="{X+5}" y2="{py(a):.1f}" stroke="#fff" stroke-opacity=".7"/>'
    for a, nom in izq:
        c += (f'<circle cx="{X}" cy="{py(a):.1f}" r="5" fill="{TRIGO if nom != "Cenit" else "#fff"}"/>'
              f'<text x="{X-12}" y="{py(a)+4:.1f}" text-anchor="end" fill="#fff" font-size="12.5" font-family="system-ui,sans-serif">{nom} {a:.0f}°</text>')
    for (a, nom), col in zip(der, ("#ff9a8b", "#f1d27a", "#9fc0ff")):
        c += (f'<circle cx="{X}" cy="{py(a):.1f}" r="5" fill="{col}"/>'
              f'<text x="{X+12}" y="{py(a)+4:.1f}" fill="{col}" font-size="12.5" font-family="system-ui,sans-serif">{nom} {a:.0f}°</text>')
    c += f'<text x="{X}" y="{Y1+19}" text-anchor="middle" fill="#fff" font-size="12" font-weight="700" font-family="system-ui,sans-serif">Horizonte · 0°</text>'
    return _svg(c, f"Escalera de alturas sobre el horizonte, de 0 a 90 grados, con la Estrella Polar a {LAT:.1f} grados y el Sol de solsticio y equinoccio a mediodía")


def _proy_eq(estrellas, ra0, dec0, k, cx, cy, cosf=1.0):
    return {n: (cx - (ra - ra0) * 15 * k * cosf, cy - (dec - dec0) * k) for n, (ra, dec) in estrellas.items()}


def orion():
    E = {"Betelgeuse": (5.92, 7.41), "Bellatrix": (5.42, 6.35), "Mintaka": (5.53, -0.30), "Alnilam": (5.60, -1.20), "Alnitak": (5.68, -1.94),
         "Saiph": (5.80, -9.67), "Rigel": (5.24, -8.20), "Sirio": (6.75, -16.72), "Aldebarán": (4.60, 16.51)}
    P = _proy_eq(E, 5.6, 0, 5.2, 150, 112, 0.95)
    lin = [("Betelgeuse", "Bellatrix"), ("Betelgeuse", "Alnitak"), ("Bellatrix", "Mintaka"), ("Alnitak", "Alnilam"), ("Alnilam", "Mintaka"),
           ("Alnitak", "Saiph"), ("Mintaka", "Rigel"), ("Saiph", "Rigel")]
    c = _cielo("g8") + _estrellas(40, 300, 200, 9)
    c += f'<line x1="{P["Aldebarán"][0]:.0f}" y1="{P["Aldebarán"][1]:.0f}" x2="{P["Sirio"][0]:.0f}" y2="{P["Sirio"][1]:.0f}" stroke="{TRIGO}" stroke-width="1.6" stroke-dasharray="5 5" opacity=".8"/>'
    for a, b in lin:
        c += f'<line x1="{P[a][0]:.1f}" y1="{P[a][1]:.1f}" x2="{P[b][0]:.1f}" y2="{P[b][1]:.1f}" stroke="#9fb8ee" stroke-width="1.8"/>'
    for n, (x, y) in P.items():
        r = 4.2 if n in ("Betelgeuse", "Rigel", "Sirio") else 3.2
        col = "#ffb36b" if n == "Betelgeuse" else ("#bcd8ff" if n in ("Rigel", "Sirio") else "#fff")
        c += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/>'
    for n, dx, dy in (("Betelgeuse", 7, -4), ("Rigel", 7, 12), ("Sirio", -4, 16), ("Aldebarán", -6, -8)):
        c += f'<text x="{P[n][0]+dx:.1f}" y="{P[n][1]+dy:.1f}" fill="#fff" font-size="10" font-family="system-ui,sans-serif">{n}</text>'
    return _svg(c, "Carta de la constelación de Orión con el Cinturón de tres estrellas, Betelgeuse y Rigel, y la línea que apunta a Sirio y a Aldebarán")


def triangulo_verano():
    E = {"Vega": (18.62, 38.78), "Deneb": (20.69, 45.28), "Altair": (19.85, 8.87)}
    P = _proy_eq(E, 19.7, 28, 3.3, 150, 112, 0.78)
    c = _cielo("g9") + _estrellas(45, 300, 200, 13)
    c += f'<path d="M-10 190 C80 150 160 90 320 20 L320 62 C180 130 90 190 -10 214Z" fill="#fff" opacity=".13"/>'
    pts = " ".join(f"{P[n][0]:.1f},{P[n][1]:.1f}" for n in ("Vega", "Deneb", "Altair"))
    c += f'<polygon points="{pts}" fill="{TRIGO}" fill-opacity=".10" stroke="{TRIGO}" stroke-width="1.8" stroke-dasharray="6 5"/>'
    for n, (x, y) in P.items():
        c += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.4" fill="#fff"/><text x="{x+8:.1f}" y="{y-6:.1f}" fill="#fff" font-size="11" font-family="system-ui,sans-serif">{n}</text>'
    return _svg(c, "Carta del Triángulo de Verano formado por Vega, Deneb y Altair, sobre la banda de la Vía Láctea")


def lunas():
    c = f'<rect width="300" height="200" fill="{NOCHE}"/>' + _estrellas(26, 300, 200, 17)
    nombres = ["Nueva", "Creciente", "1.er cuarto", "Gibosa", "Llena", "Gibosa", "3.er cuarto", "Menguante"]
    r = 19
    for i in range(8):
        cx, cy = 66 + (i % 4) * 56, 84 + (i // 4) * 74
        p = i / 8; ang = 2 * math.pi * p; rx = abs(r * math.cos(ang))
        c += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#26324f"/>'
        if i == 4:
            c += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f6efd2"/>'
        elif i != 0:
            cos = math.cos(ang)
            if p < .5:   # creciente: iluminada la derecha
                c += (f'<path d="M{cx} {cy-r} A{r} {r} 0 0 1 {cx} {cy+r} A{rx:.1f} {r} 0 0 {0 if cos > 0 else 1} {cx} {cy-r}Z" fill="#f6efd2"/>')
            else:        # menguante: iluminada la izquierda
                c += (f'<path d="M{cx} {cy-r} A{r} {r} 0 0 0 {cx} {cy+r} A{rx:.1f} {r} 0 0 {1 if cos > 0 else 0} {cx} {cy-r}Z" fill="#f6efd2"/>')
        c += f'<text x="{cx}" y="{cy+r+14}" text-anchor="middle" fill="#bcd0f2" font-size="10.5" font-family="system-ui,sans-serif">{nombres[i]}</text>'
    return _svg(c, "Las ocho fases de la Luna, de la nueva a la llena y de nuevo a la nueva, vistas desde el hemisferio norte")


LLUVIAS = [  # (nombre, mes, día del máximo, constelación)
    ("Cuadrántidas", 1, 3, "Boyero"), ("Líridas", 4, 22, "Lira"), ("η-Acuáridas", 5, 6, "Acuario"), ("Perseidas", 8, 12, "Perseo"),
    ("Oriónidas", 10, 21, "Orión"), ("Leónidas", 11, 17, "Leo"), ("Gemínidas", 12, 14, "Géminis")]
MESES = "E F M A M J J A S O N D".split()


def rueda_lluvias():
    cx, cy, R = 260, 210, 124
    ac = lambda mes, dia: ((mes - 1) + (dia - 1) / 30.4) / 12 * 2 * math.pi - math.pi / 2
    c = f'<rect width="520" height="420" fill="{NOCHE}"/>' + _estrellas(80, 520, 420, 31)
    c += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="2"/>'
    for m in range(12):
        a = ac(m + 1, 1) + (math.pi / 12)
        c += (f'<line x1="{cx+(R-6)*math.cos(ac(m+1,1)):.1f}" y1="{cy+(R-6)*math.sin(ac(m+1,1)):.1f}" x2="{cx+(R+6)*math.cos(ac(m+1,1)):.1f}" y2="{cy+(R+6)*math.sin(ac(m+1,1)):.1f}" stroke="#fff" stroke-opacity=".5"/>'
              f'<text x="{cx+(R-24)*math.cos(a):.1f}" y="{cy+(R-24)*math.sin(a)+4:.1f}" text-anchor="middle" fill="#bcd0f2" font-size="13" font-family="system-ui,sans-serif">{MESES[m]}</text>')
    for nom, mes, dia, con in LLUVIAS:
        a = ac(mes, dia); x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        col = ROJO if nom == "Perseidas" else TRIGO
        lx, ly = cx + (R + 24) * math.cos(a), cy + (R + 24) * math.sin(a)
        anc = "start" if math.cos(a) > .2 else ("end" if math.cos(a) < -.2 else "middle")
        c += (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+22*math.cos(a)-18*math.cos(a)*0:.1f}" y2="{y+22*math.sin(a):.1f}" stroke="{col}" stroke-opacity=".0"/>'
              f'<path d="M{x-16*math.cos(a)+10:.1f} {y-16*math.sin(a)-10:.1f} L{x:.1f} {y:.1f}" stroke="{col}" stroke-width="2.4" stroke-linecap="round"/>'
              f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{col}"/>'
              f'<text x="{lx:.1f}" y="{ly+4:.1f}" text-anchor="{anc}" fill="#fff" font-size="11.5" font-weight="700" font-family="system-ui,sans-serif">{nom}</text>')
    c += (f'<text x="{cx}" y="{cy-4}" text-anchor="middle" fill="#fff" font-size="16" font-weight="700" font-family="system-ui,sans-serif">Lluvias de</text>'
          f'<text x="{cx}" y="{cy+16}" text-anchor="middle" fill="#fff" font-size="16" font-weight="700" font-family="system-ui,sans-serif">estrellas</text>')
    return _svg(c, "Rueda del año con la fecha del máximo de siete lluvias de meteoros: Cuadrántidas, Líridas, eta Acuáridas, Perseidas, Oriónidas, Leónidas y Gemínidas", vb="0 0 520 420")


# ═════════════ PANORAMA PÚBLICO: qué sale por dónde desde un punto abierto de Rebolledo ═════════════
def _alt_az(dec, H_deg, lat=LAT):
    f, d, H = map(math.radians, (lat, dec, H_deg))
    alt = math.degrees(math.asin(math.sin(f) * math.sin(d) + math.cos(f) * math.cos(d) * math.cos(H)))
    az = math.degrees(math.atan2(-math.sin(H), math.tan(d) * math.cos(f) - math.sin(f) * math.cos(H))) % 360
    return az, alt


def panorama_abierto():
    X0, X1, Y0, Y1, ALT = 40, 560, 24, 224, 90
    def x_(az): return X0 + ((((az - 180) + 180) % 360)) / 360 * (X1 - X0)
    py = lambda a: Y1 - a / ALT * (Y1 - Y0)
    c = (f'<defs><linearGradient id="pa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0f1d3d"/><stop offset="1" stop-color="#4a6aa8"/></linearGradient></defs>'
         f'<rect width="600" height="290" fill="#f3ead2"/><rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" fill="url(#pa)"/>')
    for a in range(0, 91, 15):
        c += (f'<line x1="{X0}" y1="{py(a):.0f}" x2="{X1}" y2="{py(a):.0f}" stroke="#fff" stroke-opacity=".25" stroke-dasharray="3 5"/>'
              f'<text x="{X0-6}" y="{py(a)+4:.0f}" text-anchor="end" fill="{VERDE_OSC}" font-size="11" font-family="system-ui,sans-serif">{a}°</text>')
    for dec, col in ((EPS, "#ff9a8b"), (0, "#f1d27a"), (-EPS, "#9fc0ff")):
        pts = " ".join(f"{x_(a):.1f},{py(h):.1f}" for a, h in _curva_sol(dec, paso=2))
        c += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2" stroke-opacity=".95"/>'
    for ra_dec, col in (((57.14), "#ff9a8b"), ((-1.2), "#9fb8ee"), ((38.78), "#8fd18a")):
        for H in range(0, 361, 3):
            az, alt = _alt_az(ra_dec, H)
            if alt > 0: c += f'<circle cx="{x_(az):.1f}" cy="{py(alt):.1f}" r="1.6" fill="{col}"/>'
    for xx in (x_(0), x_(359.99)):
        c += f'<circle cx="{xx:.1f}" cy="{py(LAT):.1f}" r="5" fill="{TRIGO}"/>'
    c += f'<rect x="{X0}" y="{Y1}" width="{X1-X0}" height="26" fill="{VERDE_OSC}"/>'
    for az, nm in ((0, "N"), (45, "NE"), (90, "E"), (135, "SE"), (180, "S"), (225, "SO"), (270, "O"), (315, "NO"), (359.9, "N")):
        c += f'<text x="{x_(az):.0f}" y="{Y1+18}" text-anchor="middle" fill="#fff" font-size="12" font-weight="700" font-family="system-ui,sans-serif">{nm}</text>'
    ley = [("#ff9a8b", "Sol, solsticio de verano"), ("#f1d27a", "Sol, equinoccios"), ("#9fc0ff", "Sol, solsticio de invierno"), ("#ff9a8b", "Doble Cúmulo"),
           ("#9fb8ee", "Cinturón de Orión"), ("#8fd18a", "Vega"), (TRIGO, "Estrella Polar")]
    for i, (col, tx) in enumerate(ley):
        xx = 24 + (i % 4) * 140; yy = 268 + (i // 4) * 16
        c += f'<circle cx="{xx}" cy="{yy-4}" r="4" fill="{col}"/><text x="{xx+9}" y="{yy}" fill="{VERDE_OSC}" font-size="10.5" font-family="system-ui,sans-serif">{tx}</text>'
    return _svg(c, "Panorama del horizonte, de norte a norte pasando por el sur, con las trayectorias del Sol, la Polar, el Doble Cúmulo, Orión y Vega vistas desde un punto despejado de Rebolledo", vb="0 0 600 296")


def punto_vacio():
    c = (_cielo("g10") + _estrellas(40, 300, 140, 23)
         + f'<path d="M0 160 C80 140 160 166 300 150 V200 H0Z" fill="{VERDE_OSC}"/>'
         f'<path d="M150 150 C118 112 122 78 150 58 C178 78 182 112 150 150Z" fill="{ROJO}"/><circle cx="150" cy="92" r="11" fill="#fff"/>'
         f'<text x="150" y="190" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui,sans-serif">¿Dónde se ve mejor?</text>')
    return _svg(c, "Dibujo de una chincheta de mapa sobre un campo bajo el cielo estrellado: lugar por señalar")
