#!/usr/bin/env python3
"""Fotos de ejemplo de cada ser vivo de «Fauna y flora», de Wikimedia Commons (solo licencias libres: CC0, dominio público, CC BY, CC BY-SA).
Para cada especie: imagen principal de Wikidata (P18) o, si no sirve, la imagen de portada de Wikipedia; se comprueba su licencia en Commons, se guarda una miniatura
en naturaleza/fotos/ y se anota autor, licencia y enlace en naturaleza/fotos.json (la web muestra siempre el crédito). Sin tokens. Uso: python3 fotos.py [--solo Nombre]"""
import json, re, sys, time, urllib.parse, urllib.request, socket, html
from pathlib import Path
_g = socket.getaddrinfo
socket.getaddrinfo = lambda *a, **k: ([r for r in _g(*a, **k) if r[0] == socket.AF_INET] or _g(*a, **k))
AQUI = Path(__file__).parent
UA = "rebolledo-web-fotos/0.1 (https://teleclubrebolledo-glitch.github.io/webrebosemiloc/; proyecto comunitario sin ánimo de lucro)"
D = json.loads((AQUI / "datos.json").read_text())
FOT = AQUI / "fotos.json"
previo = json.loads(FOT.read_text()) if FOT.exists() else {}

OVERRIDE = {  # cuando el nombre científico del dato es un grupo o varias especies
    "Murciélagos": "Pipistrellus pipistrellus", "Chopo y sauce": "Populus nigra", "Brezo y tomillo": "Calluna vulgaris", "Narcisos": "Narcissus pseudonarcissus",
    "Orquídeas silvestres": "Ophrys apifera", "Amapolas, acianos y margaritas": "Papaver rhoeas", "Tomillo, cantueso y espliego": "Thymus vulgaris", "Setas": "Amanita muscaria",
    "Abejorros y abejas silvestres": "Bombus terrestris", "Mariposas diurnas": "Papilio machaon", "Luciérnagas": "Lampyris noctiluca", "Libélulas y caballitos del diablo": "Anax imperator",
    "Escarabajos peloteros": "Scarabaeus laticollis", "Saltamontes y grillos": "Tettigonia viridissima", "Lobo": "Canis lupus", "Búho real": "Bubo bubo"}


ARCHIVO_FORZADO = {"Búho real": "Bubo_bubo_3_(Martin_Mecnarowski).jpg"}   # cuando la imagen automática no es buena


def api(url):
    for i in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40))
        except Exception:
            time.sleep(2 * (i + 1))
    return {}


def candidatos(nombre_cient):
    """Archivos de Commons posibles para una especie: P18 de Wikidata y portada de Wikipedia (en/es)."""
    out = []
    for wiki in ("en", "es"):
        q = f"https://{wiki}.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(nombre_cient)}&prop=pageprops|pageimages&ppprop=wikibase_item&piprop=name&redirects=1&format=json"
        pg = next(iter(api(q).get("query", {}).get("pages", {}).values()), {})
        qid = pg.get("pageprops", {}).get("wikibase_item")
        if qid:
            cl = api(f"https://www.wikidata.org/w/api.php?action=wbgetclaims&entity={qid}&property=P18&format=json").get("claims", {}).get("P18", [])
            for c in cl:
                try: out.append(c["mainsnak"]["datavalue"]["value"])
                except Exception: pass
        if pg.get("pageimage"): out.append(pg["pageimage"])
        time.sleep(0.4)
    vistos = []
    for f in out:
        if f not in vistos: vistos.append(f)
    return vistos


def libre(lic):
    l = (lic or "").upper()
    if "NC" in l.split() or "-NC" in l or "-ND" in l or "ND " in l: return False
    return bool(re.match(r"^(CC0|PUBLIC DOMAIN|PD|CC BY(-SA)? \d)", l))


def info(archivo):
    q = ("https://commons.wikimedia.org/w/api.php?action=query&titles=" + urllib.parse.quote("File:" + archivo) +
         "&prop=imageinfo&iiprop=extmetadata|url|mime|size&iiurlwidth=420&format=json")
    pg = next(iter(api(q).get("query", {}).get("pages", {}).values()), {})
    ii = (pg.get("imageinfo") or [{}])[0]
    em = ii.get("extmetadata", {})
    lic = em.get("LicenseShortName", {}).get("value", "")
    artista = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", em.get("Artist", {}).get("value", "")))).strip()
    return dict(licencia=lic, url_licencia=em.get("LicenseUrl", {}).get("value", ""), autor=artista[:90] or "autoría indicada en Wikimedia Commons",
                miniatura=ii.get("thumburl"), mime=ii.get("mime", ""), pagina=ii.get("descriptionurl", ""), titulo=archivo)


def descarga(url, destino):
    for i in range(3):
        try:
            d = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
            destino.write_bytes(d); return True
        except Exception:
            time.sleep(3 * (i + 1))
    return False


def entradas():
    for g in ("aves", "mamiferos", "reptiles", "arboles", "flora", "insectos"):
        for e in D.get(g, []):
            yield e["nombre"], OVERRIDE.get(e["nombre"]) or e.get("cientifico", "")


if __name__ == "__main__":
    solo = sys.argv[sys.argv.index("--solo") + 1] if "--solo" in sys.argv else None
    res = dict(previo)
    for nombre, cient in entradas():
        if solo and nombre != solo: continue
        if nombre in res and res[nombre].get("archivo") and not solo: continue
        if not cient: res[nombre] = {"error": "sin nombre científico"}; continue
        elegido = None
        for arch in ([ARCHIVO_FORZADO[nombre]] if nombre in ARCHIVO_FORZADO else candidatos(cient)[:5]):
            if not re.search(r"\.(jpe?g|png|webp)$", arch, re.I): continue
            i = info(arch); time.sleep(0.4)
            if i["miniatura"] and libre(i["licencia"]) and i["mime"].startswith("image/"):
                elegido = i; break
        if not elegido:
            res[nombre] = {"error": "sin imagen libre encontrada", "buscado": cient}; print("✗", nombre, cient); continue
        slug = re.sub(r"[^a-z0-9]+", "-", re.sub(r"[áàä]", "a", re.sub(r"[éèë]", "e", re.sub(r"[íìï]", "i", re.sub(r"[óòö]", "o", re.sub(r"[úùü]", "u", nombre.lower())))))).strip("-")
        tmpf = AQUI / "fotos" / f"_{slug}.tmp"
        dest = AQUI / "fotos" / f"{slug}.jpg"
        if not descarga(elegido["miniatura"], tmpf): res[nombre] = {"error": "descarga fallida"}; print("✗ descarga", nombre); continue
        import subprocess      # miniatura ligera: 380 px de ancho, JPEG, sin metadatos
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(tmpf), "-map_metadata", "-1", "-vf", "scale='min(380,iw)':-2", "-q:v", "6", "-f", "mjpeg", str(dest)], check=False); tmpf.unlink(missing_ok=True)
        if not dest.exists(): res[nombre] = {"error": "conversión fallida"}; print("✗ conv", nombre); continue
        res[nombre] = {"archivo": f"fotos/{dest.name}", "autor": elegido["autor"], "licencia": elegido["licencia"], "url_licencia": elegido["url_licencia"], "pagina": elegido["pagina"], "buscado": cient}
        print("✓", nombre, "·", elegido["licencia"], "·", elegido["autor"][:40])
        FOT.write_text(json.dumps(res, ensure_ascii=False, indent=1)); time.sleep(0.6)
    FOT.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print("hecho:", sum(1 for v in res.values() if v.get("archivo")), "con foto de", len(res))
