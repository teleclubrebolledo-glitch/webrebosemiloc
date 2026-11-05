"""Tarjetas de «Huerta» y «Fauna y flora» para la web. Datos: huerta/datos.json (copia de HuertaDigital) y naturaleza/datos.json (a mano).
Todo orientativo: la web lo dice. Setas y plantas tóxicas: avisos de seguridad en lo más visible."""
import datetime, json
from html import escape
from pathlib import Path
import graficos as G

AQUI = Path(__file__).parent
MES = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def _json(p):
    try: return json.loads((AQUI / p).read_text())
    except Exception: return {}


H = _json("huerta/datos.json"); N = _json("naturaleza/datos.json"); FOT = _json("naturaleza/fotos.json"); FOTH = _json("huerta/fotos.json")


def meses(txt):
    out = set()
    for tr in (txt or "").split(","):
        tr = tr.strip()
        if not tr: continue
        if "-" in tr:
            a, b = [int(x) for x in tr.split("-")]
            out |= set(range(a, b + 1)) if a <= b else set(range(a, 13)) | set(range(1, b + 1))
        else: out.add(int(tr))
    return out


def fmt(txt):
    """'3-4,10-11' → 'marzo–abril, octubre–noviembre'"""
    partes = []
    for tr in (txt or "").split(","):
        tr = tr.strip()
        if not tr: continue
        if "-" in tr:
            a, b = [int(x) for x in tr.split("-")]
            partes.append(f"{MES[a]}–{MES[b]}" if a != b else MES[a])
        else: partes.append(MES[int(tr)])
    return ", ".join(partes)


def hoy_mes():
    return datetime.date.today().month


def _lista(esp, campo, mes, solo_huerta=False):
    return [e for e in esp if mes in meses(e.get(campo, "")) and (e["huerta"] or not solo_huerta)]


def _nombres(lst):
    return ", ".join(sorted({e["nombre"] for e in lst}, key=str.lower)) or "—"


def _mini(nombre, fuente=None, base="naturaleza"):
    f = (FOT if fuente is None else fuente).get(nombre, {})
    return f'<img class="mini" src="{base}/{escape(f["archivo"])}" alt="" width="44" height="44" loading="lazy"> ' if f.get("archivo") else ""


def _ejemplo(nombre, fuente=None, base="naturaleza", pie="Foto de ejemplo"):
    f = (FOT if fuente is None else fuente).get(nombre, {})
    if not f.get("archivo"): return ""
    lic = f'<a href="{escape(f["url_licencia"])}" rel="noopener">{escape(f["licencia"])}</a>' if f.get("url_licencia") else escape(f.get("licencia", ""))
    return (f'<figure class="ejemplo"><img src="{base}/{escape(f["archivo"])}" alt="{pie}: {escape(nombre)}" loading="lazy">'
            f'<figcaption>{pie}: {escape(f["autor"])} · {lic} · <a href="{escape(f["pagina"])}" rel="noopener">Wikimedia Commons</a></figcaption></figure>')


def _hm(e): return _mini(e["id"], FOTH, "huerta")


def _hej(e): return _ejemplo(e["id"], FOTH, "huerta")


def _breve(e):
    """Descripción breve de una ficha de huerta: lo más útil en una frase."""
    for k in ("usos", "curiosidad", "labores"):
        if e.get(k): return e[k].split(". ")[0].rstrip(".") + "."
    return ""


def _ficha(e, extra_sum="", cuerpo=""):
    return (f'<details class="ficha" id="huerta-esp-{escape(e["id"])}"><summary>{_hm(e)}<strong>{escape(e["nombre"])}</strong> <em>{escape(e["cientifico"])}</em>{extra_sum}</summary>'
            f'{_hej(e)}<p class="breve">{escape(_breve(e))}</p>{cuerpo}</details>')


HABITAT_DESC = {
    "Cortados y barrancos calizos": "Las loras son páramos elevados cortados a pico por el agua durante millones de años. Las Tuerces, la Horadada o el cañón del Rudrón son los ejemplos más conocidos; sus repisas y cuevas sirven de nido y refugio.",
    "Páramos y campos de cereal": "Llanuras altas de suelo pobre y mucho cielo, cultivadas de trigo y cebada desde hace siglos. La vida se refugia en las lindes, los majuelos y los barbechos.",
    "Bosques de quejigo, melojo y encina": "Manchas de monte bajo que cubren laderas y vaguadas. Dan sombra, leña, bellotas y setas, y cambian de color con cada estación.",
    "Arroyos y riberas": "Franjas verdes de agua y arboleda entre el pardo del páramo. Son corredores de vida: pocos metros de ribera guardan más especies que kilómetros de campo.",
    "Pueblos, huertas y tapias": "Casas de piedra, tejados, tapias, huertos y paredes viejas forman un hábitat propio: la gente y la fauna comparten aleros, campanarios y rincones.",
}


RECETAS = [
    ("Crema de calabaza y zanahoria", ["calabaza", "zanahoria", "cebolla"], "Rehoga la cebolla, añade la calabaza y la zanahoria troceadas, cubre con agua, cuece 25 minutos y tritura con aceite de oliva, sal y nuez moscada."),
    ("Ensalada de tomate, pimiento y pepino", ["tomate", "pimiento", "pepino", "cebolla"], "Pica todo en dados, aliña con aceite de oliva, vinagre y sal, y deja reposar un cuarto de hora. Con pan tostado es una cena."),
    ("Menestra de primavera", ["guisante", "haba", "alcachofa", "esparrago"], "Saltea ajo, añade las alcachofas, las habas y los guisantes con un poco de agua y cuece tapado 15 minutos; los espárragos, al final."),
    ("Ratatouille de verano", ["calabacin", "berenjena", "tomate", "pimiento", "cebolla"], "Corta las verduras en dados, sofríelas por separado y júntalas con el tomate a fuego lento 20 minutos con tomillo."),
    ("Lentejas con verduras", ["lenteja", "zanahoria", "cebolla", "pimiento"], "Pocha cebolla, zanahoria y pimiento, añade las lentejas, pimentón y agua, y cuece hasta que estén tiernas."),
    ("Potaje de garbanzos y acelgas", ["garbanzo", "acelga", "patata"], "Cuece los garbanzos con la patata en trozos y, al final, las acelgas picadas con un sofrito de ajo y pimentón."),
    ("Judías verdes con patatas", ["judiaverde", "patata", "cebolla"], "Cuece las judías y la patata en trozos con un sofrito de ajo y cebolla; salpimienta y termina con un chorro de aceite."),
    ("Sopa de puerro y patata", ["puerro", "patata", "zanahoria"], "Rehoga el puerro, añade la patata y la zanahoria, cubre con agua y cuece 20 minutos. Se puede tomar caliente o triturada."),
    ("Crema de verduras de invierno", ["puerro", "chirivia", "zanahoria", "col"], "Cuece el puerro, la chirivía y la zanahoria hasta que estén blandos, tritura y sirve con unas hojas de col salteadas."),
    ("Berza o kale salteada con ajo", ["kale", "col", "bruselas", "ajo"], "Cuece las hojas 5 minutos, escúrrelas y saltéalas con ajo laminado y un toque de pimentón."),
    ("Borrajas rehogadas con patata", ["borraja", "patata", "puerro"], "Cuece las borrajas limpias con un poco de patata, escurre y saltea con ajo y aceite de oliva."),
    ("Ensalada de invierno con canónigos", ["canonigo", "escarola", "remolacha", "manzano"], "Mezcla canónigos o escarola con remolacha cocida y manzana en láminas, y aliña con aceite, limón y nueces."),
    ("Crema de coliflor y brócoli", ["coliflor", "brocoli", "puerro", "patata"], "Cuece todo con un poco de patata, tritura con el caldo justo y sirve con pimienta y aceite."),
    ("Ensalada de fresas, rúcula y nueces", ["fresa", "rucula", "lechuga", "nogal"], "Mezcla las hojas con fresas laminadas y nueces; aliña con aceite de oliva, vinagre balsámico y una pizca de sal."),
    ("Compota de manzana y membrillo", ["manzano", "membrillo", "peral"], "Pela y trocea la fruta, cuece con un chorrito de agua y canela hasta que se deshaga. Sin azúcar, o con muy poca."),
    ("Mermelada casera de frutos rojos", ["frambuesa", "grosella", "fresa"], "Cuece la fruta con un poco de azúcar y unas gotas de limón hasta que espese; guarda en frascos esterilizados."),
    ("Tortilla de calabacín", ["calabacin", "cebolla", "patata"], "Pocha cebolla, calabacín y patata en rodajas finas y mézclalo con garbanzo molido y agua para cuajar, o con harina de garbanzo."),
    ("Puré de nabos y zanahorias", ["nabo", "zanahoria", "patata", "colinabo"], "Cuece las raíces troceadas y chafa con aceite de oliva, sal y pimienta; ideal en días fríos."),
    ("Espinacas con garbanzos", ["espinaca", "garbanzo", "ajo"], "Sofríe ajo, añade los garbanzos cocidos y las espinacas, y cuece 5 minutos con comino y pimentón."),
    ("Alcachofas al ajillo", ["alcachofa", "ajo"], "Limpia las alcachofas, cuécelas 10 minutos y dóralas con ajo laminado, aceite de oliva y limón."),
    ("Pisto castellano", ["tomate", "pimiento", "calabacin", "cebolla", "berenjena"], "Sofríe cebolla y pimiento, añade el calabacín y la berenjena, y por último el tomate; cuece a fuego lento 30 minutos."),
]


def _ids_cosecha(mes):
    return {e["id"] for e in _lista(H.get("especies", []), "cosecha", mes, True)}


def receta(mes):
    """La receta cuyos ingredientes principales se cosechan este mes (la que más coincide); sin etiquetas de dieta."""
    cos = _ids_cosecha(mes)
    mejor = None
    for nombre, ing, texto in RECETAS:
        n = sum(1 for i in ing if i in cos)
        if n >= 2 or (n == len(ing) and n >= 1):
            pt = (n / len(ing), n)
            if not mejor or pt > mejor[0]: mejor = (pt, nombre, ing, texto, n)
    return mejor


def banner_items(mes=None):
    """Para la segunda cinta: especies que este mes y el próximo se siembran, plantan o cosechan. [{foto, titulo, texto, enlace}]"""
    mes = mes or hoy_mes(); sig = mes % 12 + 1
    esp = {e["id"]: e for e in H.get("especies", []) + H.get("flores", [])}
    out = []
    for m, cuando in ((mes, "este mes"), (sig, "el mes que viene")):
        for campo, verbo in (("cosecha", "se cosecha"), ("siembra_aire", "se siembra"), ("siembra_prot", "se siembra bajo cubierta"), ("plantar", "se planta")):
            for e in _lista(list(esp.values()), campo, m, True):
                if e["tipo"] in ("hongo", "tóxica", "silvestre"): continue
                f = FOTH.get(e["id"], {})
                if not f.get("archivo"): continue
                if any(o["id"] == e["id"] for o in out): continue
                out.append({"id": e["id"], "foto": "huerta/" + f["archivo"], "titulo": e["nombre"], "texto": f"{verbo} {cuando}", "enlace": f"#huerta-esp-{e['id']}", "orden": (0 if m == mes else 1, 0 if campo == "cosecha" else 1)})
    out.sort(key=lambda o: o["orden"])
    return out[:14]


def card(marker):
    """→ (icono, html_texto, ancha)"""
    esp = H.get("especies", []); flores = H.get("flores", []); mes = hoy_mes()
    nota = f'<p class="nota">{escape(H.get("aviso", ""))}</p>' if H else ""
    if marker == "H:este_mes":
        l = H.get("labores_mes", {}).get(str(mes), "")
        s = _lista(esp, "siembra_aire", mes, True); sp = _lista(esp, "siembra_prot", mes, True); p = _lista(esp, "plantar", mes, True); c = _lista(esp, "cosecha", mes, True)
        return "calendario", (f'<p><strong>{MES[mes].capitalize()}.</strong> {escape(l)}</p><ul class="guia" style="margin-top:.3rem">'
                              f'<li><strong>Sembrar al aire libre:</strong> {escape(_nombres(s))}</li><li><strong>Sembrar bajo cubierta:</strong> {escape(_nombres(sp))}</li>'
                              f'<li><strong>Plantar o trasplantar:</strong> {escape(_nombres(p))}</li><li><strong>Cosechar:</strong> {escape(_nombres(c))}</li></ul>{nota}'), False
    if marker == "H:temporada":
        c = [e for e in _lista(esp, "cosecha", mes, True) if e["tipo"] in ("hortaliza", "legumbre", "frutal", "fruto", "cereal", "otro")]
        fr = [e for e in c if e["tipo"] in ("frutal", "fruto")]; ho = [e for e in c if e not in fr]
        return "hortaliza", (f'<p>Lo que da la huerta en <strong>{MES[mes]}</strong> a unos 958 m de <strong>altitud sobre el nivel del mar</strong>:</p><ul class="guia" style="margin-top:.3rem"><li><strong>Hortalizas y legumbres:</strong> {escape(_nombres(ho))}</li>'
                             f'<li><strong>Frutas y frutos:</strong> {escape(_nombres(fr))}</li></ul><p class="nota">Comer de temporada y de cerca es más barato, más sabroso y más sostenible.</p>'), False
    if marker == "H:proximo":
        sig = mes % 12 + 1
        l = H.get("labores_mes", {}).get(str(sig), "")
        s_ = _lista(esp, "siembra_aire", sig, True); sp = _lista(esp, "siembra_prot", sig, True); p = _lista(esp, "plantar", sig, True); c = _lista(esp, "cosecha", sig, True)
        return "calendario", (f'<p><strong>{MES[sig].capitalize()}, el mes que viene.</strong> {escape(l)}</p><ul class="guia" style="margin-top:.3rem">'
                              f'<li><strong>Sembrar al aire libre:</strong> {escape(_nombres(s_))}</li><li><strong>Sembrar bajo cubierta:</strong> {escape(_nombres(sp))}</li>'
                              f'<li><strong>Plantar o trasplantar:</strong> {escape(_nombres(p))}</li><li><strong>Cosechar:</strong> {escape(_nombres(c))}</li></ul>{nota}'), False
    if marker == "H:receta":
        r = receta(mes)
        if not r: return "hortaliza", "<p>Este mes la huerta descansa: buen momento para preparar el suelo y mirar conservas.</p>", False
        _, nombre, ing, texto, _n = r
        por = {e["id"]: e["nombre"] for e in esp}
        lista = ", ".join(por[i].lower() for i in ing if i in por)
        mos = "".join(f'<img src="huerta/{escape(FOTH[i]["archivo"])}" alt="{escape(por[i])}" title="{escape(por[i])}" loading="lazy">' for i in ing if i in por and FOTH.get(i, {}).get("archivo"))
        mos = f'<div class="figuras mosaico mos{min(len(ing), 6)}">{mos}</div>' if mos else ""
        return "hortaliza", (mos + f'<p><strong>{escape(nombre)}.</strong></p><p>Con lo que se cosecha en {MES[mes]}: {escape(lista)}, más aceite de oliva, sal y especias.</p><p>{escape(texto)}</p>'
                             '<p class="nota">Sugerencia orientativa; cambia cantidades y especias a tu gusto. Fotos de ingredientes: Wikimedia Commons, licencia libre; autoría en <a href="creditos-fotos.html">créditos de las fotos</a>.</p>'), False
    if marker == "H:consejos":
        li = ["Aquí hiela hasta mediados de mayo y puede volver a helar en octubre: no trasplantes tomates ni pimientos antes de entonces o protégelos con manta térmica.",
              "Riega temprano y poco a poco; acolchar con paja o hierba seca ahorra agua y mantiene el suelo vivo.",
              "Rota los cultivos: no repitas en el mismo bancal la misma familia (tomates, patatas y pimientos son de la misma) dos años seguidos.",
              "Pon flores (caléndula, tagetes, capuchina) entre las hortalizas: atraen polinizadores y alejan plagas.",
              "Deja un rincón silvestre: erizos, lagartijas y mariquitas hacen de guardianes de la huerta.",
              "Compost siempre: restos de cocina y de poda; el suelo es lo más valioso de la huerta."]
        return "consejo", "<ul class=\"guia\">" + "".join(f"<li>{escape(x)}</li>" for x in li) + f"</ul>{nota}", False
    if marker == "H:calendario":
        pri = ["ajo", "cebolla", "patata", "zanahoria", "lechuga", "judia_verde", "tomate", "pimiento", "calabacin", "calabaza", "guisante", "haba", "col", "espinaca", "fresa", "puerro"]
        por_id = {e["id"]: e for e in esp}
        filas = []
        for i in pri:
            e = por_id.get(i) or next((x for x in esp if x["id"].startswith(i)), None)
            if not e: continue
            filas.append((e["nombre"], [(meses(e["siembra_aire"]) | meses(e["siembra_prot"]), "#4c6b2e"), (meses(e["plantar"]), "#d9ad3f"), (meses(e["cosecha"]), "#a3441a")]))
        svg = G.calendario_barras(filas, [("#4c6b2e", "Sembrar"), ("#d9ad3f", "Plantar"), ("#a3441a", "Cosechar")], "Calendario de la huerta (altitud de la zona: 958 m)")
        return "calendario", f'<div class="figuras una" style="background:#faf5e8">{svg}</div>', True
    grupos = {"H:hortalizas": ("hortaliza", "Hortalizas y legumbres", ("hortaliza", "legumbre", "cereal", "otro")), "H:frutales": ("frutal", "Frutales y árboles de la zona", ("frutal", "fruto")),
              "H:aromaticas": ("aromatica", "Aromáticas, medicinales y silvestres", ("aromática", "medicinal", "silvestre")), "H:flores": ("flor", "Flores", ("flor",))}
    if marker in grupos:
        icono, tit, tipos = grupos[marker]
        lst = sorted([e for e in esp + flores if e["tipo"] in tipos], key=lambda e: e["nombre"].lower())
        det = ""
        for e in lst:
            f = []
            if e["siembra_aire"]: f.append(f"<strong>Siembra al aire libre:</strong> {fmt(e['siembra_aire'])}")
            if e["siembra_prot"]: f.append(f"<strong>Siembra protegida:</strong> {fmt(e['siembra_prot'])}")
            if e["plantar"]: f.append(f"<strong>Plantar:</strong> {fmt(e['plantar'])}")
            if e["cosecha"]: f.append(f"<strong>{e.get('etiqueta_mes') or 'Cosecha'}:</strong> {fmt(e['cosecha'])}")
            det += _ficha(e, "", '<ul class="guia" style="margin:.3rem 0">' + "".join(f"<li>{x}</li>" for x in f)
                          + (f"<li><strong>Labores:</strong> {escape(e['labores'])}</li>" if e["labores"] else "") + (f"<li><strong>Usos:</strong> {escape(e['usos'])}</li>" if e["usos"] else "")
                          + (f"<li><strong>Curiosidad:</strong> {escape(e['curiosidad'])}</li>" if e["curiosidad"] else "")
                          + (f"<li><strong>⚠ Precaución:</strong> {escape(e['precaucion'])}</li>" if e["precaucion"] else "") + "</ul>")
        return icono, f'<p>{len(lst)} fichas básicas; pulsa una para abrirla.</p>{det}{nota}', True
    if marker == "H:setas":
        setas = sorted([e for e in esp if e["tipo"] == "hongo"], key=lambda e: e["nombre"].lower())
        def nivel(e):
            p = e["precaucion"].upper()
            if p.startswith("TÓXICA CRUDA") or p.startswith("TOXICA CRUDA"): return ("comestible solo bien cocinada y con experto", "#b58a1a")
            return ("MORTAL", "#a3441a") if p.startswith("MORTAL") else (("TÓXICA", "#c26b1a") if p.startswith(("TÓXICA", "TOXICA", "TÓXICA CRUDA")) or "TÓXICA" in p[:40] else ("comestible solo con identificación experta", "#4c6b2e"))
        filas = [(e["nombre"], [(meses(e["cosecha"]), nivel(e)[1])]) for e in setas]
        svg = G.calendario_barras(filas, [("#4c6b2e", "Comestible (con experto)"), ("#b58a1a", "Solo bien cocinada"), ("#c26b1a", "Tóxica"), ("#a3441a", "MORTAL")], "Temporadas de setas en la zona", alto_fila=19)
        det = ""
        for e in setas:
            n, col = nivel(e)
            det += _ficha(e, f' · <span class="etiqueta" style="border-color:{col};color:{col}">{escape(n)}</span> · {fmt(e["cosecha"])}',
                          '<ul class="guia" style="margin:.3rem 0">' + (f"<li>{escape(e['labores'])}</li>" if e["labores"] else "") + f"<li><strong>⚠</strong> {escape(e['precaucion'])}</li></ul>")
        aviso = ('<div class="alerta"><p><strong>NUNCA comas una seta porque lo diga una ficha, una foto o una aplicación.</strong> Hay setas mortales que se parecen a las comestibles y los síntomas pueden tardar entre 6 horas y varios días en aparecer, cuando el daño ya es grave. '
                 'Identifícalas solo con una persona experta o con una sociedad micológica. Si has comido una seta dudosa y notas malestar, ve a urgencias con una muestra (112 o Toxicología: 91 562 04 20).</p>'
                 '<p>Recoge solo lo que necesites, en cesta de mimbre (no bolsa de plástico) y sin arrancar ni pisar las que no conoces. En algunos montes de Castilla y León hace falta permiso o hay normas de recolección: infórmate antes en el Ayuntamiento o en el servicio de medio ambiente. <em>(Dato por confirmar.)</em></p></div>')
        return "seta", f'{aviso}<div class="figuras una" style="background:#faf5e8">{svg}</div><p>{len(setas)} setas de la zona. Pulsa para abrir su ficha:</p>{det}', True
    if marker == "H:peligros":
        tox = sorted([e for e in esp if e["tipo"] == "tóxica"], key=lambda e: e["nombre"].lower())
        det = "".join(_ficha(e, "", f'<ul class="guia" style="margin:.3rem 0"><li><strong>⚠</strong> {escape(e["precaucion"])}</li>' + (f"<li>{escape(e['labores'])}</li>" if e["labores"] else "") + "</ul>") for e in tox)
        return "peligro", ('<div class="alerta"><p><strong>Plantas que parecen inofensivas y no lo son.</strong> No pruebes ninguna planta silvestre sin estar segura de cuál es, y enseña estas a niños y niñas: la cicuta se confunde con el perejil, '
                           'el cólquico con el ajo silvestre, y las bayas de la belladona atraen a los más pequeños. Ante cualquier duda tras comer una planta, llama al 112.</p></div>' + det), True
    # ───────── fauna y flora ─────────
    if not N: return "habitat", "<p>Sección en preparación.</p>", False
    aviso_n = f'<p class="nota">{escape(N.get("aviso", ""))}</p>'
    def aves_de(grupos):
        return [a for a in N["aves"] if a["grupo"] in grupos]
    def det_aves(lst):
        return "".join(f'<details class="ficha"><summary>{_mini(a["nombre"])}<strong>{escape(a["nombre"])}{" ★" if a["geoparque"] else ""}</strong> <em>{escape(a["cientifico"])}</em> · {"todo el año" if a["meses"] == "1-12" else fmt(a["meses"])}</summary>'
                       f'{_ejemplo(a["nombre"])}<ul class="guia" style="margin:.3rem 0"><li><strong>Dónde:</strong> {escape(a["donde"])}</li><li><strong>Cómo reconocerla:</strong> {escape(a["rasgo"])}</li><li>{escape(a["dato"])}</li></ul></details>' for a in lst)
    if marker == "N:habitats":
        return "habitat", "".join(f'<section class="habitat"><h4>{escape(h["nombre"])}</h4>{_ejemplo(h["nombre"], pie="Foto de ejemplo")}<p>{escape(HABITAT_DESC.get(h["nombre"], ""))}</p><p><strong>Quién vive aquí:</strong> {escape(h["dato"])}</p></section>' for h in N["habitats"]) + aviso_n, True
    if marker == "N:rapaces":
        l = aves_de(("rapaz", "córvido", "ave de roca"))
        return "ave", f"<p>Las aves de los cortados y del cielo de las loras: rapaces, carroñeras y córvidos. ★ = citada por fuentes del Geoparque.</p>{det_aves(l)}{aviso_n}", True
    if marker == "N:campo":
        l = aves_de(("ave de campo", "ave de pueblo", "nocturna", "ave de bosque"))
        return "ave", f"<p>Las del campo de cereal, los pueblos, el bosque y la noche.</p>{det_aves(l)}{aviso_n}", True
    if marker == "N:calendario":
        pr = ["Buitre leonado", "Alimoche", "Milano real", "Aguilucho cenizo", "Cigüeña blanca", "Golondrina común", "Vencejo común", "Abubilla", "Codorniz común", "Avión roquero", "Petirrojo", "Alondra común"]
        por = {a["nombre"]: a for a in N["aves"]}
        filas = [(n, [(meses(por[n]["meses"]), "#4c6b2e")]) for n in pr if n in por]
        svg = G.calendario_barras(filas, [("#4c6b2e", "Se la puede ver")], "Calendario de las aves: cuándo están aquí")
        return "ave", f'<div class="figuras una" style="background:#faf5e8">{svg}</div><p class="nota">Los meses son orientativos: llegan y se van según el tiempo de cada año.</p>', True
    if marker == "N:mamiferos":
        return "mamifero", "<p>Mamíferos de la zona; casi todos de costumbres nocturnas o muy discretos.</p>" + "".join(
            f'<details class="ficha"><summary>{_mini(m["nombre"])}<strong>{escape(m["nombre"])}</strong> <em>{escape(m["cientifico"])}</em></summary>{_ejemplo(m["nombre"])}<ul class="guia" style="margin:.3rem 0"><li><strong>Dónde:</strong> {escape(m["donde"])}</li><li><strong>Cómo reconocerlo:</strong> {escape(m["rasgo"])}</li><li>{escape(m["dato"])}</li></ul></details>' for m in N["mamiferos"]) + aviso_n, True
    if marker == "N:reptiles":
        return "reptil", "<p>Reptiles y anfibios. Casi todos son inofensivos; la única víbora venenosa (áspid) se deja pasar y no se toca.</p>" + "".join(
            f'<details class="ficha"><summary>{_mini(r["nombre"])}<strong>{escape(r["nombre"])}</strong> <em>{escape(r["cientifico"])}</em> · {escape(r["grupo"])}</summary>{_ejemplo(r["nombre"])}<ul class="guia" style="margin:.3rem 0"><li><strong>Dónde:</strong> {escape(r["donde"])}</li><li>{escape(r["dato"])}</li></ul></details>' for r in N["reptiles"]) + aviso_n, True
    if marker == "N:insectos":
        return "insecto", "".join(f'<details class="ficha"><summary>{_mini(i["nombre"])}<strong>{escape(i["nombre"])}</strong></summary>{_ejemplo(i["nombre"])}<ul class="guia" style="margin:.3rem 0"><li>{escape(i["dato"])}</li></ul></details>' for i in N["insectos"]), True
    if marker == "N:arboles":
        return "arbol", "<p>Árboles y arbustos del monte y los linderos. ★ = citado por fuentes del Geoparque.</p>" + "".join(
            f'<details class="ficha"><summary>{_mini(a["nombre"])}<strong>{escape(a["nombre"])}{" ★" if a["geoparque"] else ""}</strong> <em>{escape(a["cientifico"])}</em></summary>{_ejemplo(a["nombre"])}<ul class="guia" style="margin:.3rem 0"><li>{escape(a["dato"])}</li></ul></details>' for a in N["arboles"]) + aviso_n, True
    if marker == "N:flora":
        return "flor", "".join(f'<details class="ficha"><summary>{_mini(f["nombre"])}<strong>{escape(f["nombre"])}</strong> <em>{escape(f["cientifico"])}</em></summary>{_ejemplo(f["nombre"])}<ul class="guia" style="margin:.3rem 0"><li>{escape(f["dato"])}</li></ul></details>' for f in N["flora"]), True
    if marker == "N:mirar":
        return "consejo", "<ul class=\"guia\">" + "".join(f"<li>{escape(x)}</li>" for x in N["mirar"]) + "</ul>", False
    return "habitat", "<p>En preparación.</p>", False
