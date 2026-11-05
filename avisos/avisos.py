#!/usr/bin/env python3
"""Avisos útiles para Rebolledo de la Torre y sus localidades, en lenguaje natural. SIN IA y SIN gastar tokens: solo reglas y expresiones regulares.
Fuentes (config.json): BOE (API de datos abiertos), BOCYL (RSS), BOP de Burgos (pendiente), RSS de noticias del medio rural.
Uso: python3 avisos.py            → actualiza salida/avisos.json (acumula histórico y recalcula puntuaciones)
     python3 avisos.py --prueba   → no escribe; imprime un resumen
Reglas: solo se publican título oficial (de dominio público), un resumen hecho por programa y el enlace al texto oficial. Nunca sustituye a la publicación oficial."""
import datetime, hashlib, html, json, re, socket, subprocess, sys, tempfile, time, unicodedata, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

AQUI = Path(__file__).parent
SALIDA = AQUI / "salida" / "avisos.json"
CFG = json.loads((AQUI / "config.json").read_text())
UA = "Mozilla/5.0 (X11; Linux x86_64) avisos-rebolledo/0.1 (+https://teleclubrebolledo-glitch.github.io/webrebosemiloc/)"

_gai = socket.getaddrinfo    # algunas redes tienen IPv6 roto: se prefiere IPv4
socket.getaddrinfo = lambda *a, **k: ([r for r in _gai(*a, **k) if r[0] == socket.AF_INET] or _gai(*a, **k))


def norm(t):
    return unicodedata.normalize("NFKD", t.lower()).encode("ascii", "ignore").decode()


def get(url, accept=None, binario=False, intentos=3):
    for i in range(intentos):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, **({"Accept": accept} if accept else {})})
            d = urllib.request.urlopen(req, timeout=40).read()
            return d if binario else d.decode("utf-8", "replace")
        except Exception as e:
            ultimo = e; time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"{url}: {type(ultimo).__name__}")


def limpia(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t or ""))).strip()


# ───────────────────────── fuentes ─────────────────────────
def desde_boe(dias):
    out = []
    hoy = datetime.date.today()
    for k in range(dias):
        f = hoy - datetime.timedelta(days=k)
        try:
            j = json.loads(get(f"https://www.boe.es/datosabiertos/api/boe/sumario/{f:%Y%m%d}", accept="application/json"))
        except Exception:
            continue                                                  # sin BOE ese día (domingo/festivo)
        def anda(nodo, sec="", dep="", epi=""):
            if isinstance(nodo, list):
                for x in nodo: anda(x, sec, dep, epi)
            elif isinstance(nodo, dict):
                if "identificador" in nodo and "titulo" in nodo:
                    u = nodo.get("url_pdf"); u = u.get("texto") if isinstance(u, dict) else u
                    out.append(dict(id=nodo["identificador"], fecha=f.isoformat(), fuente="BOE", organismo=dep, seccion=sec, epigrafe=epi,
                                    titulo=limpia(nodo["titulo"]), enlace=nodo.get("url_html") or u, pdf=u, xml=nodo.get("url_xml")))
                    return
                s = nodo.get("nombre", "") if "codigo" in nodo and "departamento" in nodo else sec
                d = nodo.get("nombre", "") if "epigrafe" in nodo or ("item" in nodo and "codigo" not in nodo) else dep
                e = nodo.get("nombre", "") if "item" in nodo and "epigrafe" not in nodo and "codigo" not in nodo and dep else epi
                for key in ("diario", "seccion", "departamento", "epigrafe", "item"):
                    if key in nodo: anda(nodo[key], s or sec, d or dep, e or epi)
        anda(j.get("data", {}).get("sumario", {}))
    return out


def desde_bocyl(secciones):
    out = []
    hoy = datetime.date.today().isoformat()
    for s in secciones:
        try:
            r = ET.fromstring(get(f"https://bocyl.jcyl.es/rss.do?seccion={s}"))
        except Exception:
            continue
        for it in r.findall(".//item"):
            m = re.search(r"del d[ií]a (\d\d)/(\d\d)/(\d{4})", it.findtext("title") or "")
            fecha = f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else hoy
            desc = html.unescape(it.findtext("description") or "")
            for li in re.findall(r"<li.*?</li>", desc, flags=re.S):
                a = re.search(r'<a href="([^"]+)">(.*?)</a>', li, flags=re.S); ps = re.findall(r"<p[^>]*>(.*?)</p>", li, flags=re.S)
                if not a or len(ps) < 2: continue
                titulo = limpia(ps[1]); pdf = a.group(1)
                partes = [limpia(x) for x in re.findall(r"<xml-fragment[^>]*>(.*?)</xml-fragment>", a.group(2))] or [limpia(a.group(2))]
                out.append(dict(id="BOCYL-" + hashlib.sha1(pdf.encode()).hexdigest()[:12], fecha=fecha, fuente="BOCYL", organismo=partes[-1] if partes else "",
                                seccion=partes[0] if partes else "", epigrafe="", titulo=titulo, enlace=pdf, pdf=pdf, xml=None))
    return out


def desde_rss(cfg):
    out = []
    try:
        r = ET.fromstring(get(cfg["url"]))
    except Exception:
        return out
    for it in r.findall(".//item"):
        link = it.findtext("link") or ""
        try: f = datetime.datetime.strptime((it.findtext("pubDate") or "")[:25].strip(), "%a, %d %b %Y %H:%M:%S").date().isoformat()
        except Exception: f = datetime.date.today().isoformat()
        out.append(dict(id="RSS-" + hashlib.sha1(link.encode()).hexdigest()[:12], fecha=f, fuente=cfg["nombre"], organismo=cfg["nombre"], seccion="", epigrafe="",
                        titulo=limpia(it.findtext("title")), enlace=link, pdf=None, xml=None, texto=limpia(it.findtext("description"))[:700], categoria_fija=cfg.get("categoria")))
    return out


# ───────────────────────── puntuación ─────────────────────────
def contiene(t, palabras):
    return [p for p in palabras if norm(p) in t]


def puntua(it):
    t = norm(" ".join([it["titulo"], it.get("organismo", ""), it.get("epigrafe", ""), it.get("texto", "")]))
    terr = CFG["territorio"]; P = CFG["puntuacion"]
    if contiene(t, CFG["descartar"]) and not contiene(t, [terr["municipio"]] + terr["localidades"]):
        return None
    ambito, base = None, 0
    if contiene(t, [terr["municipio"]] + [l for l in terr["localidades"] if l != "Rebolledo"]) or re.search(r"\brebolledo\b", t): ambito, base = "local", P["local"]
    elif contiene(t, terr["comarca"]): ambito, base = "comarca", P["comarca"]
    elif contiene(t, terr["provincia"]): ambito, base = "provincia", P["provincia"]
    elif contiene(t, terr["region"]): ambito, base = "region", P["region"]
    else: ambito = "nacional"
    if ambito == "nacional" and contiene(t, CFG.get("otras_regiones", [])):
        return None                                               # ayuda o anuncio de otra comunidad autónoma
    cats, pts = [], 0
    for k, c in CFG["categorias"].items():
        if k == "noticias": continue
        hit = contiene(t, c["palabras"])
        if hit: cats.append(k); pts += c["peso"] + min(len(hit) - 1, 2)
    if it.get("categoria_fija") == "noticias":
        if not ({"rural", "ayudas", "energia", "comunicaciones", "turismo", "emprendimiento", "vivienda"} & set(cats)): return None
        cats.append("noticias")
    if "ayudas" in cats and not ({"rural", "energia", "comunicaciones", "transporte", "turismo", "emprendimiento", "vivienda", "cultura", "educacion", "empleo"} & set(cats)): pts -= 6
    if ambito == "nacional" and not ({"ayudas", "rural"} <= set(cats) or {"energia"} <= set(cats) and "burgos" in t): pts = pts // 3
    if it["fuente"] == "BOE" and ambito == "nacional" and not ("rural" in cats or "despoblaci" in t): pts = pts // 2
    total = base + pts
    if it.get("categoria_fija") == "noticias": total = max(total, base + pts + 6)
    it["ambito"] = ambito; it["categorias"] = cats or ["otros"]; it["puntos"] = total
    return total if total >= P["minimo"] and cats else None


# ───────────────────────── lenguaje natural ─────────────────────────
MESES = "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split()
TIPOS = [("convocatoria", r"\bse convocan?\b|\bconvocatoria\b|extracto de la (orden|resoluci[oó]n)"), ("bases", r"bases reguladoras"),
         ("informacion", r"informaci[oó]n p[uú]blica|somete a informaci[oó]n|exposici[oó]n p[uú]blica"), ("ambiental", r"impacto ambiental|autorizaci[oó]n ambiental|autorizaci[oó]n administrativa"),
         ("licitacion", r"licitaci[oó]n|contrato de|formalizaci[oó]n"), ("concesion", r"\bse concede\b|concesi[oó]n directa|resoluci[oó]n de concesi[oó]n"),
         ("aprobacion", r"aprobaci[oó]n (inicial|definitiva|provisional)|aprueba (inicial|definitiva)"), ("noticia", r"$^")]
QUE_HACER = {"convocatoria": "Si encaja contigo, mira en el texto oficial quién puede pedirla, el plazo y cómo se solicita.",
             "bases": "Son las normas de unas ayudas: sirven para saber con antelación si podrás pedirlas.",
             "informacion": "Cualquiera puede consultar el proyecto y presentar alegaciones dentro del plazo que marca el anuncio.",
             "ambiental": "Afecta al entorno: conviene leer qué se va a hacer, dónde y si se puede alegar.",
             "licitacion": "Es una contratación pública: solo interesa a empresas que quieran presentar oferta.",
             "concesion": "Se han concedido ayudas o subvenciones; mira si entre los beneficiarios hay alguien de la zona.",
             "aprobacion": "Es un acuerdo ya aprobado; el texto oficial dice qué cambia y desde cuándo.",
             "noticia": "Noticia de un medio: el enlace lleva a la información completa.",
             "otro": "Lee el texto oficial para ver si te afecta."}
QUIEN = [("agricultores y ganaderos", r"agricultor|ganader|explotaciones agrari|titulares de explotaci|apicultor"), ("jóvenes que se incorporan al campo", r"incorporaci[oó]n de j[oó]venes|joven agricultor"),
         ("ayuntamientos y entidades locales", r"entidades locales|ayuntamientos|municipios"), ("personas emprendedoras, autónomas y pymes", r"emprendedor|aut[oó]nomos|pymes?|microempresa|empresas"),
         ("asociaciones y entidades sin ánimo de lucro", r"sin [aá]nimo de lucro|asociaciones|fundaciones"), ("propietarios y vecinos de la zona", r"propietarios|vecinos|afectados|interesados"),
         ("quien quiera estudiar o formarse", r"alumnado|estudiantes|\bbecas\b|\bformaci[oó]n (profesional|para el empleo|continua)")]


def tipo_de(t):
    for k, rx in TIPOS:
        if re.search(rx, t, flags=re.I): return k
    return "otro"


def natural(it, texto=""):
    t = it["titulo"]; plano = norm(t + " " + texto)
    tipo = "noticia" if it.get("categoria_fija") == "noticias" else tipo_de(t)
    m = re.search(r",? por (la|el) que se (.*)$", t, flags=re.I | re.S)
    if m: titulo = m.group(2).strip().rstrip(".")
    else:
        titulo = re.sub(r"^(extracto de la )?(orden|resoluci[oó]n|acuerdo|anuncio|decreto|edicto)[^,]{0,80},( de \d+ de \w+( de \d{4})?,?)?( de la [^,]+,)?", "", t, flags=re.I).strip(" ,.")
        titulo = titulo or t
    verbos = (("convocan", "Se convocan"), ("convoca", "Se convoca"), ("aprueba", "Se aprueba"), ("aprueban", "Se aprueban"), ("somete", "Sale"), ("publica", "Se publica"), ("concede", "Se concede"), ("resuelve", "Se resuelve"))
    titulo = titulo[0].upper() + titulo[1:] if titulo else t
    if m:
        v = m.group(2).split()[0].lower()
        for k, rep in verbos:
            if v.startswith(k): titulo = rep + titulo[len(m.group(2).split()[0]):]; break
        else: titulo = "Se " + m.group(2).strip().rstrip(".")
        titulo = titulo.replace("Sale a información pública", "Sale a información pública") if "informaci" in titulo.lower() else titulo
    titulo = titulo[:230].rstrip(" ,;") + ("…" if len(titulo) > 230 else "")
    plazo = importe = None
    mp = re.search(r"plazo de (\w+(?: \(\d+\))?|\d+) (d[ií]as h[aá]biles|d[ií]as naturales|d[ií]as|meses|mes)", texto, flags=re.I)
    if mp: plazo = f"{mp.group(1)} {mp.group(2)} desde la publicación"
    mf = re.search(r"hasta el (\d{1,2} de (?:" + "|".join(MESES) + r") de \d{4})", texto, flags=re.I)
    if mf: plazo = (plazo + "; " if plazo else "") + "hasta el " + mf.group(1)
    mi = re.search(r"(?:cr[eé]dito|dotaci[oó]n|importe|cuant[ií]a|presupuesto)[^.]{0,120}?(\d{1,3}(?:\.\d{3})+(?:,\d{1,2})?|\d+(?:,\d{1,2})?) ?(?:euros|€)", texto, flags=re.I)
    if mi: importe = mi.group(1) + " €"
    quien = [n for n, rx in QUIEN if re.search(rx, texto or t, flags=re.I)][:2]
    dondes = re.findall(r"(?:t[eé]rmino municipal de|municipio de|t[eé]rminos municipales de|en) ((?:[A-ZÁÉÍÓÚÑ][\wáéíóúñ]+)(?: (?:de|del|la|las|los|y) [A-ZÁÉÍÓÚÑ][\wáéíóúñ]+)*)", t)
    donde = next((d for d in dondes if len(d) > 3 and d.lower() not in ("el", "la")), None)
    proyecto = re.search(r"(parque e[oó]lico|planta fotovoltaica|instalaci[oó]n fotovoltaica|instalaci[oó]n solar|l[ií]nea el[eé]ctrica[^,]{0,60}|subestaci[oó]n[^,]{0,40})", t, flags=re.I)
    den = re.search(r"denominad[ao]s? [«\"“]?([^»\"”,.]{3,60})", t)
    if tipo in ("informacion", "ambiental") and proyecto:
        nom = den.group(1).split("«")[-1].strip() if den else ""
        nombre = f" «{nom}»" if nom else ""
        lugar = f" en la zona de {donde}" if donde else ""
        titulo = f"Sale a información pública un proyecto de {proyecto.group(1).lower()}{nombre}{lugar}"
        if not quien: quien = ["cualquier persona o entidad interesada (se puede alegar)"]
    elif tipo in ("informacion", "ambiental") and not quien:
        quien = ["cualquier persona o entidad interesada (se puede alegar)"]
    partes = []
    if it["ambito"] == "local": partes.append("Menciona tu municipio o sus localidades.")
    elif it["ambito"] in ("comarca", "provincia"): partes.append("Afecta a la comarca o a la provincia de Burgos.")
    elif it["ambito"] == "region": partes.append("Es de ámbito Castilla y León.")
    if proyecto and donde: partes.append(f"Proyecto: {proyecto.group(1).lower()} en la zona de {donde}.")
    partes.append(QUE_HACER[tipo])
    return dict(tipo=tipo, titulo_natural=titulo, resumen=" ".join(partes), a_quien=quien, plazo=plazo, importe=importe)


def texto_oficial(it):
    """Texto del anuncio, solo para sacar plazo e importe (BOE: XML; BOCYL: PDF con pdftotext)."""
    try:
        if it.get("xml"):
            x = get(it["xml"], accept="application/xml"); return limpia(x)[:20000]
        if it["fuente"] == "BOCYL" and it.get("pdf"):
            with tempfile.TemporaryDirectory() as d:
                p = Path(d) / "a.pdf"; p.write_bytes(get(it["pdf"], binario=True))
                return subprocess.run(["pdftotext", "-q", str(p), "-"], capture_output=True, text=True, timeout=60).stdout[:20000]
    except Exception:
        return ""
    return ""


# ───────────────────────── principal ─────────────────────────
def main():
    prueba = "--prueba" in sys.argv
    if "--dias" in sys.argv: CFG["fuentes"]["boe"]["dias"] = int(sys.argv[sys.argv.index("--dias") + 1])
    F = CFG["fuentes"]; estado = {}; nuevos = []
    for clave, fn in (("boe", lambda: desde_boe(F["boe"]["dias"])), ("bocyl", lambda: desde_bocyl(F["bocyl"]["secciones"]))):
        if F[clave]["activa"]:
            try: r = fn(); nuevos += r; estado[clave] = f"ok ({len(r)} anuncios leídos)"
            except Exception as e: estado[clave] = "error: " + type(e).__name__
        else: estado[clave] = "desactivada"
    estado["bopbu"] = "pendiente: " + F["bopbu"].get("nota", "")
    for f in F["rss"]:
        if f.get("activa"):
            r = desde_rss(f); nuevos += r; estado[f["nombre"]] = f"ok ({len(r)} noticias leídas)" if r else "sin datos hoy"
    previo = {}
    if SALIDA.exists():
        try:
            for a in json.loads(SALIDA.read_text()).get("items", []): previo[a["id"]] = a
        except Exception: pass
    limite = (datetime.date.today() - datetime.timedelta(days=CFG["puntuacion"]["dias_historico"])).isoformat()
    todos = {i["id"]: i for i in nuevos if i["fecha"] >= limite}
    elegidos = []
    for i in todos.values():
        if i["id"] in previo and previo[i["id"]].get("titulo_natural"):
            elegidos.append(previo[i["id"]]); continue
        p = puntua(i)
        if p is not None: elegidos.append(i)
    for a in previo.values():
        if a["id"] not in todos and a["fecha"] >= limite: elegidos.append(a)
    # texto oficial solo para los de más puntos que aún no tienen resumen
    elegidos.sort(key=lambda a: (-a.get("puntos", 0), a["fecha"]), reverse=False)
    pend = [a for a in elegidos if not a.get("titulo_natural")][:25]
    for a in pend:
        txt = a.get("texto") or texto_oficial(a); a.update(natural(a, txt)); a.pop("texto", None); a.pop("categoria_fija", None); a.pop("xml", None)
    for a in elegidos:
        if not a.get("titulo_natural"): a.update(natural(a, a.get("texto", ""))); a.pop("texto", None); a.pop("categoria_fija", None); a.pop("xml", None)
    vistos, final = set(), []
    for a in sorted(elegidos, key=lambda a: (-a["puntos"], -int(a["fecha"].replace("-", "")))):
        if a["id"] in vistos: continue
        vistos.add(a["id"]); final.append(a)
    final = final[: CFG["puntuacion"]["maximo_total"]]
    salida = {"actualizado": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "estado_fuentes": estado, "total": len(final),
              "aviso": "Resumen automático hecho por un programa, sin inteligencia artificial. Lo que vale es el texto oficial del enlace.", "items": final}
    if prueba:
        print(json.dumps(estado, ensure_ascii=False, indent=1))
        for a in final[:15]: print(f"{a['puntos']:3d} {a['fecha']} {a['fuente']:6s} [{a['ambito']}] {','.join(a['categorias'])} · {a['titulo_natural'][:110]}")
        print(len(final), "avisos")
    else:
        SALIDA.parent.mkdir(exist_ok=True); SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1))
        print("escrito", SALIDA, len(final), "avisos")


if __name__ == "__main__":
    main()
