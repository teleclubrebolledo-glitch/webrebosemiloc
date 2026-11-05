#!/usr/bin/env python3
"""Tiempo en Rebolledo de la Torre para la cabecera de la web: estado de ahora y previsión de mañana, con probabilidad de lluvia y avisos de peligro.
Datos de Open-Meteo.com (CC BY 4.0). Se ejecuta en el servidor (GitHub Actions cada pocas horas): los visitantes NO contactan con ningún tercero. Sin IA, sin tokens.
Los umbrales de peligro están al principio y se pueden ajustar. Es una ayuda orientativa: los avisos oficiales son los de AEMET (aemet.es)."""
import json, socket, urllib.request, datetime
from pathlib import Path
_gai = socket.getaddrinfo
socket.getaddrinfo = lambda *a, **k: ([r for r in _gai(*a, **k) if r[0] == socket.AF_INET] or _gai(*a, **k))

HELADA = 0            # °C: helada (temperatura ≤ este valor)
HELADA_FUERTE = -6    # °C
VIENTO = 70           # km/h de racha: viento fuerte
LLUVIA_FUERTE_DIA = 20   # mm en el día
LLUVIA_FUERTE_AHORA = 4  # mm en la última hora/15 min
NIEVE_DIA = 2         # cm en el día: nevada
NIEVE_FUERTE_DIA = 6  # cm
CALOR = 36            # °C máxima

URL = ("https://api.open-meteo.com/v1/forecast?latitude=42.6889&longitude=-4.2271"
       "&current=temperature_2m,weather_code,is_day,precipitation,wind_gusts_10m"
       "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,wind_gusts_10m_max,snowfall_sum"
       "&timezone=Europe%2FMadrid&forecast_days=2")
req = urllib.request.Request(URL, headers={"User-Agent": "tiempo-rebolledo/0.1"})
j = json.load(urllib.request.urlopen(req, timeout=40))
c, d = j["current"], j["daily"]


def peligros(codigo, tmin, tmax, racha, lluvia, nieve, lluvia_ahora=0):
    out = []
    if tmin <= HELADA_FUERTE: out.append(("helada", f"Helada fuerte (hasta {round(tmin)} °C)", 2))
    elif tmin <= HELADA: out.append(("helada", f"Helada ({round(tmin)} °C)", 1))
    if racha >= VIENTO: out.append(("viento", f"Fuerte viento (rachas de {round(racha)} km/h)", 2 if racha >= 90 else 1))
    if lluvia >= LLUVIA_FUERTE_DIA or lluvia_ahora >= LLUVIA_FUERTE_AHORA: out.append(("lluvia", f"Lluvia fuerte ({round(max(lluvia, lluvia_ahora))} mm)", 2 if lluvia >= 40 else 1))
    if codigo in (96, 99): out.append(("granizo", "Posible granizada", 2))
    elif codigo >= 95: out.append(("tormenta", "Tormenta", 2))
    if nieve >= NIEVE_DIA or codigo in (71, 73, 75, 77, 85, 86): out.append(("nieve", f"Nevada{' fuerte' if nieve >= NIEVE_FUERTE_DIA else ''}" + (f" ({round(nieve)} cm)" if nieve else ""), 2 if nieve >= NIEVE_FUERTE_DIA else 1))
    if codigo in (66, 67): out.append(("hielo", "Lluvia helada: hielo en las carreteras", 2))
    if tmax >= CALOR: out.append(("calor", f"Calor intenso ({round(tmax)} °C)", 2 if tmax >= 40 else 1))
    return [{"k": k, "t": t, "n": n} for k, t, n in out]


hoy = {"codigo": c["weather_code"], "tmin": min(c["temperature_2m"], d["temperature_2m_min"][0]), "tmax": d["temperature_2m_max"][0], "racha": max(c["wind_gusts_10m"], d["wind_gusts_10m_max"][0]),
       "lluvia": d["precipitation_sum"][0], "nieve": d["snowfall_sum"][0]}
# para «ahora» pesa el estado actual, y para el resto de hoy, la previsión del día
p_ahora = peligros(hoy["codigo"], c["temperature_2m"], d["temperature_2m_max"][0], hoy["racha"], hoy["lluvia"], hoy["nieve"], c.get("precipitation", 0))
p_manana = peligros(d["weather_code"][1], d["temperature_2m_min"][1], d["temperature_2m_max"][1], d["wind_gusts_10m_max"][1], d["precipitation_sum"][1], d["snowfall_sum"][1])
out = {"actualizado": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "fuente": "Open-Meteo.com (CC BY 4.0)",
       "ahora": {"codigo": c["weather_code"], "temp": round(c["temperature_2m"]), "dia": bool(c["is_day"]), "lluvia": d["precipitation_probability_max"][0], "peligros": p_ahora},
       "manana": {"codigo": d["weather_code"][1], "tmax": round(d["temperature_2m_max"][1]), "tmin": round(d["temperature_2m_min"][1]), "lluvia": d["precipitation_probability_max"][1], "peligros": p_manana}}
(Path(__file__).parent / "tiempo.json").write_text(json.dumps(out, ensure_ascii=False))
print(json.dumps(out, ensure_ascii=False))
