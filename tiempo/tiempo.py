#!/usr/bin/env python3
"""Tiempo en Rebolledo de la Torre para la cabecera de la web: estado actual y previsión de mañana. Datos de Open-Meteo.com (CC BY 4.0).
Se ejecuta en el servidor (GitHub Actions cada pocas horas): los visitantes NO contactan con ningún tercero. Sin IA, sin tokens."""
import json, socket, urllib.request, datetime
from pathlib import Path
_gai = socket.getaddrinfo
socket.getaddrinfo = lambda *a, **k: ([r for r in _gai(*a, **k) if r[0] == socket.AF_INET] or _gai(*a, **k))
URL = ("https://api.open-meteo.com/v1/forecast?latitude=42.6889&longitude=-4.2271&current=temperature_2m,weather_code,is_day"
       "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Europe%2FMadrid&forecast_days=2")
req = urllib.request.Request(URL, headers={"User-Agent": "tiempo-rebolledo/0.1"})
j = json.load(urllib.request.urlopen(req, timeout=40))
c, d = j["current"], j["daily"]
out = {"actualizado": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "fuente": "Open-Meteo.com (CC BY 4.0)",
       "ahora": {"codigo": c["weather_code"], "temp": round(c["temperature_2m"]), "dia": bool(c["is_day"])},
       "manana": {"codigo": d["weather_code"][1], "tmax": round(d["temperature_2m_max"][1]), "tmin": round(d["temperature_2m_min"][1]), "lluvia": d["precipitation_probability_max"][1]}}
(Path(__file__).parent / "tiempo.json").write_text(json.dumps(out, ensure_ascii=False))
print(out)
