"""Ficha-ruta en vectores: plano + perfil + datos, desde datos-rutas/<id>.json (trazado + altitudes). Sin JavaScript ni imágenes de terceros.
Datos de mapa © colaboradores de OpenStreetMap (ODbL); altitudes EU-DEM 25 m (Copernicus). Los trazados propuestos están POR VERIFICAR andando."""
import json, math
from html import escape
from pathlib import Path
import graficos as G

DATOS = Path(__file__).parent / "datos-rutas"
R = 6371000


def _d(a, b):
    p1, p2 = math.radians(a[0]), math.radians(b[0]); dl = math.radians(b[1] - a[1]); dp = p2 - p1
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def cargar(id_):
    return json.loads((DATOS / f"{id_}.json").read_text())


def metricas(pts):
    """km acumulados, altitudes suavizadas, desnivel positivo/negativo (con umbral de 3 m para no sumar ruido), min y max."""
    km = [0.0]
    for a, b in zip(pts, pts[1:]): km.append(km[-1] + _d(a, b) / 1000)
    alt = [p[2] for p in pts]
    sua = [sum(alt[max(0, i - 2): i + 3]) / len(alt[max(0, i - 2): i + 3]) for i in range(len(alt))]
    sube = baja = 0.0; ref = sua[0]
    for h in sua[1:]:
        if h - ref >= 3: sube += h - ref; ref = h
        elif ref - h >= 3: baja += ref - h; ref = h
    horas = km[-1] / 5 + sube / 600            # regla de Naismith (5 km/h + 1 h por 600 m de subida), sin paradas
    return dict(km=km, alt=sua, dist=km[-1], sube=sube, baja=baja, mn=min(sua), mx=max(sua), horas=horas)


def dificultad(m):
    if m["dist"] < 6 and m["sube"] < 150: return "Fácil"
    if m["dist"] < 14 and m["sube"] < 500: return "Moderada"
    return "Exigente"


def _hm(h):
    t = int(round(h * 60)); return f"{t // 60} h {t % 60:02d} min"


def ficha_svg(ru):
    pts = ru["pts"]; m = metricas(pts)
    lat0 = sum(p[0] for p in pts) / len(pts); k = math.cos(math.radians(lat0))
    xs = [p[1] * k for p in pts]; ys = [p[0] for p in pts]
    PX0, PY0, PW, PH = 20, 20, 520, 380
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    esc = min(PW / max(x1 - x0, 1e-9), PH / max(y1 - y0, 1e-9)) * .88
    ox = PX0 + (PW - (x1 - x0) * esc) / 2; oy = PY0 + (PH - (y1 - y0) * esc) / 2
    P = lambda lat, lon: (ox + (lon * k - x0) * esc, oy + (y1 - lat) * esc)
    m_por_px = 111320 / esc if esc else 1
    c = f'<rect width="760" height="640" fill="#faf7ef"/><rect x="{PX0}" y="{PY0}" width="{PW}" height="{PH}" rx="4" fill="#e6edd2"/>'
    c += f'<clipPath id="cl{ru["id"]}"><rect x="{PX0}" y="{PY0}" width="{PW}" height="{PH}"/></clipPath><g clip-path="url(#cl{ru["id"]})">'
    for via in ru.get("contexto", []):
        pp = " ".join("%.1f,%.1f" % P(a, b) for a, b in via)
        c += f'<polyline points="{pp}" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/><polyline points="{pp}" fill="none" stroke="#c9b98d" stroke-width="1.5" stroke-linecap="round"/>'
    tr = " ".join("%.1f,%.1f" % P(p[0], p[1]) for p in pts)
    c += f'<polyline points="{tr}" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
    c += f'<polyline points="{tr}" fill="none" stroke="{G.ROJO}" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/>'
    # marcas cada kilómetro
    for i in range(1, int(m["dist"]) + 1):
        j = min(range(len(m["km"])), key=lambda q: abs(m["km"][q] - i)); x, y = P(pts[j][0], pts[j][1])
        c += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#fff" stroke="{G.VERDE_OSC}" stroke-width="1.5"/><text x="{x:.1f}" y="{y+3.6:.1f}" text-anchor="middle" font-size="10" font-weight="700" fill="{G.VERDE_OSC}" font-family="system-ui,sans-serif">{i}</text>'
    sx, sy = P(pts[0][0], pts[0][1]); ex, ey = P(*ru["extremo"])
    c += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="11" fill="{G.VERDE}" stroke="#fff" stroke-width="3"/><text x="{sx:.1f}" y="{sy+4.5:.1f}" text-anchor="middle" font-size="13" font-weight="700" fill="#fff" font-family="system-ui,sans-serif">S</text>'
    c += f'<path d="M{ex:.1f} {ey+2:.1f} V{ey-24:.1f} L{ex+18:.1f} {ey-18:.1f} L{ex:.1f} {ey-12:.1f}" fill="{G.TRIGO}" stroke="{G.VERDE_OSC}" stroke-width="2.4" stroke-linejoin="round"/><circle cx="{ex:.1f}" cy="{ey+2:.1f}" r="3.2" fill="{G.VERDE_OSC}"/>'
    c += "</g>"
    # escala y norte
    esc_m = 100
    for metros in (100, 200, 500, 1000, 2000, 5000):
        if metros / m_por_px < PW * .35: esc_m = metros
    ancho = esc_m / m_por_px
    c += f'<line x1="{PX0+14}" y1="{PY0+PH-16}" x2="{PX0+14+ancho:.1f}" y2="{PY0+PH-16}" stroke="{G.VERDE_OSC}" stroke-width="4"/><text x="{PX0+14+ancho/2:.1f}" y="{PY0+PH-24}" text-anchor="middle" font-size="12" fill="{G.VERDE_OSC}" font-family="system-ui,sans-serif">{esc_m if esc_m < 1000 else esc_m // 1000} {"m" if esc_m < 1000 else "km"}</text>'
    c += f'<path d="M{PX0+PW-30} {PY0+54} V{PY0+16} M{PX0+PW-30} {PY0+16} L{PX0+PW-37} {PY0+30} M{PX0+PW-30} {PY0+16} L{PX0+PW-23} {PY0+30}" stroke="{G.VERDE_OSC}" stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/><text x="{PX0+PW-30}" y="{PY0+12}" text-anchor="middle" font-size="14" font-weight="700" fill="{G.VERDE_OSC}" font-family="system-ui,sans-serif">N</text>'
    # datos
    DX = 560
    datos = [("Distancia", f'{m["dist"]:.1f} km'), ("Desnivel +", f'{m["sube"]:.0f} m'), ("Desnivel −", f'{m["baja"]:.0f} m'), ("Cota máx.", f'{m["mx"]:.0f} m'),
             ("Cota mín.", f'{m["mn"]:.0f} m'), ("Tiempo", _hm(m["horas"])), ("Dificultad", dificultad(m)), ("Tipo", "Circular" if ru["circular"] else "Ida y vuelta")]
    for i, (t, v) in enumerate(datos):
        y = 20 + i * 48
        c += (f'<rect x="{DX}" y="{y}" width="180" height="40" rx="14" ry="14" fill="#fff" stroke="#c9b98d"/>'
              f'<text x="{DX+12}" y="{y+15}" font-size="10.5" fill="#6b6b5a" font-family="system-ui,sans-serif">{t}</text>'
              f'<text x="{DX+12}" y="{y+32}" font-size="16" font-weight="700" fill="{G.VERDE_OSC}" font-family="system-ui,sans-serif">{escape(v)}</text>')
    # perfil
    QX0, QY0, QW, QH = 60, 440, 660, 140
    amin, amax = math.floor(m["mn"] / 20) * 20, math.ceil(m["mx"] / 20) * 20
    if amax - amin < 60: amax = amin + 60
    px = lambda kmv: QX0 + kmv / m["dist"] * QW
    py = lambda h: QY0 + QH - (h - amin) / (amax - amin) * QH
    c += f'<text x="20" y="{QY0-12}" font-size="14" font-weight="700" fill="{G.VERDE_OSC}" font-family="system-ui,sans-serif">Perfil de altura</text>'
    for h in range(int(amin), int(amax) + 1, 20 if amax - amin <= 200 else 50):
        c += f'<line x1="{QX0}" y1="{py(h):.1f}" x2="{QX0+QW}" y2="{py(h):.1f}" stroke="#e1d8bf" stroke-width="1"/><text x="{QX0-6}" y="{py(h)+4:.1f}" text-anchor="end" font-size="10.5" fill="#6b6b5a" font-family="system-ui,sans-serif">{h}</text>'
    area = f'M{px(0):.1f},{QY0+QH} ' + " ".join(f"L{px(a):.1f},{py(h):.1f}" for a, h in zip(m["km"], m["alt"])) + f" L{px(m['dist']):.1f},{QY0+QH}Z"
    c += f'<path d="{area}" fill="{G.VERDE}" fill-opacity=".28"/><polyline points="{" ".join("%.1f,%.1f" % (px(a), py(h)) for a, h in zip(m["km"], m["alt"]))}" fill="none" stroke="{G.VERDE_OSC}" stroke-width="2.4" stroke-linejoin="round"/>'
    for i in range(0, int(m["dist"]) + 1):
        c += f'<text x="{px(i):.1f}" y="{QY0+QH+16}" text-anchor="middle" font-size="10.5" fill="#6b6b5a" font-family="system-ui,sans-serif">{i} km</text>'
    jmax = max(range(len(m["alt"])), key=lambda i: m["alt"][i])
    c += f'<circle cx="{px(m["km"][jmax]):.1f}" cy="{py(m["alt"][jmax]):.1f}" r="4.5" fill="{G.ROJO}"/><text x="{px(m["km"][jmax]):.1f}" y="{py(m["alt"][jmax])-9:.1f}" text-anchor="middle" font-size="11.5" font-weight="700" fill="{G.ROJO}" font-family="system-ui,sans-serif">{m["mx"]:.0f} m</text>'
    c += f'<text x="20" y="620" font-size="10.5" fill="#6b6b5a" font-family="system-ui,sans-serif">Trazado propuesto sobre caminos de © OpenStreetMap (ODbL) · altitudes EU-DEM (Copernicus) · tiempo: regla de Naismith · POR VERIFICAR</text>'
    etiqueta = f'Ficha de la ruta {ru["nombre"]}: plano con el trazado, perfil de altura y datos; {m["dist"]:.1f} kilómetros, {m["sube"]:.0f} metros de subida, dificultad {dificultad(m).lower()}'
    return G._svg(c, etiqueta, vb="0 0 760 640"), m


def ficha_html(id_):
    ru = cargar(id_); svg, m = ficha_svg(ru)
    return svg, m, ru
