#!/usr/bin/env python3
"""Fotos de ejemplo de cada ficha de la Huerta (hortalizas, frutales, aromáticas, silvestres, setas, plantas peligrosas y flores), de Wikimedia Commons con licencia libre.
Reutiliza la búsqueda de naturaleza/fotos.py. Guarda miniaturas en huerta/fotos/ y autoría en huerta/fotos.json (clave: id de la especie)."""
import json, re, subprocess, sys, time
from pathlib import Path
AQUI = Path(__file__).parent
sys.path.insert(0, str(AQUI.parent / "naturaleza"))
import fotos as F
D = json.loads((AQUI / "datos.json").read_text())
SAL = AQUI / "fotos.json"
res = json.loads(SAL.read_text()) if SAL.exists() else {}
OVER = {"col": "Brassica oleracea", "berza": "Brassica oleracea var. viridis", "judia_verde": "Phaseolus vulgaris"}
solo = sys.argv[sys.argv.index("--solo") + 1] if "--solo" in sys.argv else None
for e in D["especies"] + D["flores"]:
    i = e["id"]
    if solo and i != solo: continue
    if i in res and res[i].get("archivo") and not solo: continue
    cient = OVER.get(i) or e["cientifico"]
    nombres = [cient] + ([" ".join(cient.split()[:2])] if len(cient.split()) > 2 else []) + [e["nombre"].split("/")[0].strip()]
    elegido = None
    for nom in nombres:
        for arch in F.candidatos(nom)[:4]:
            if not re.search(r"\.(jpe?g|png|webp)$", arch, re.I): continue
            inf = F.info(arch); time.sleep(0.3)
            if inf["miniatura"] and F.libre(inf["licencia"]) and inf["mime"].startswith("image/"): elegido = inf; break
        if elegido: break
    if not elegido: res[i] = {"error": "sin imagen libre", "buscado": cient}; print("✗", e["nombre"], cient, flush=True); continue
    tmp = AQUI / "fotos" / f"_{i}.tmp"; dest = AQUI / "fotos" / f"{i}.jpg"
    if not F.descarga(elegido["miniatura"], tmp): res[i] = {"error": "descarga"}; continue
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(tmp), "-map_metadata", "-1", "-vf", "scale='min(380,iw)':-2", "-q:v", "6", "-f", "mjpeg", str(dest)], check=False); tmp.unlink(missing_ok=True)
    if not dest.exists(): res[i] = {"error": "conversión"}; continue
    res[i] = {"archivo": f"fotos/{dest.name}", "autor": elegido["autor"], "licencia": elegido["licencia"], "url_licencia": elegido["url_licencia"], "pagina": elegido["pagina"], "buscado": cient}
    print("✓", e["nombre"], "·", elegido["licencia"], flush=True)
    SAL.write_text(json.dumps(res, ensure_ascii=False, indent=1)); time.sleep(0.5)
SAL.write_text(json.dumps(res, ensure_ascii=False, indent=1))
print("hecho:", sum(1 for v in res.values() if v.get("archivo")), "con foto de", len(res), flush=True)
