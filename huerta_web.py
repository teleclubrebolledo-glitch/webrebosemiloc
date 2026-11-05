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


H = _json("huerta/datos.json"); N = _json("naturaleza/datos.json")


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
        return "hortaliza", (f'<p>Lo que da la huerta en <strong>{MES[mes]}</strong> a 958 m:</p><ul class="guia" style="margin-top:.3rem"><li><strong>Hortalizas y legumbres:</strong> {escape(_nombres(ho))}</li>'
                             f'<li><strong>Frutas y frutos:</strong> {escape(_nombres(fr))}</li></ul><p class="nota">Comer de temporada y de cerca es más barato, más sabroso y más sostenible.</p>'), False
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
        svg = G.calendario_barras(filas, [("#4c6b2e", "Sembrar"), ("#d9ad3f", "Plantar"), ("#a3441a", "Cosechar")], "Calendario de la huerta a 958 m")
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
            det += (f'<details class="ficha"><summary><strong>{escape(e["nombre"])}</strong> <em>{escape(e["cientifico"])}</em></summary><ul class="guia" style="margin:.3rem 0">'
                    + "".join(f"<li>{x}</li>" for x in f)
                    + (f"<li><strong>Labores:</strong> {escape(e['labores'])}</li>" if e["labores"] else "") + (f"<li><strong>Usos:</strong> {escape(e['usos'])}</li>" if e["usos"] else "")
                    + (f"<li><strong>Curiosidad:</strong> {escape(e['curiosidad'])}</li>" if e["curiosidad"] else "")
                    + (f"<li><strong>⚠ Precaución:</strong> {escape(e['precaucion'])}</li>" if e["precaucion"] else "") + "</ul></details>")
        return icono, f'<p>{len(lst)} fichas básicas; pulsa una para abrirla.</p>{det}{nota}', True
    if marker == "H:setas":
        setas = sorted([e for e in esp if e["tipo"] == "hongo"], key=lambda e: e["nombre"].lower())
        def nivel(e):
            p = e["precaucion"].upper()
            return ("MORTAL", "#a3441a") if p.startswith("MORTAL") else (("TÓXICA", "#c26b1a") if p.startswith(("TÓXICA", "TOXICA", "TÓXICA CRUDA")) or "TÓXICA" in p[:40] else ("comestible solo con identificación experta", "#4c6b2e"))
        filas = [(e["nombre"], [(meses(e["cosecha"]), nivel(e)[1])]) for e in setas]
        svg = G.calendario_barras(filas, [("#4c6b2e", "Comestible (con experto)"), ("#c26b1a", "Tóxica"), ("#a3441a", "MORTAL")], "Temporadas de setas en la zona", alto_fila=19)
        det = ""
        for e in setas:
            n, col = nivel(e)
            det += (f'<details class="ficha"><summary><strong>{escape(e["nombre"])}</strong> <em>{escape(e["cientifico"])}</em> · <span class="etiqueta" style="border-color:{col};color:{col}">{escape(n)}</span> · {fmt(e["cosecha"])}</summary>'
                    f'<ul class="guia" style="margin:.3rem 0">' + (f"<li>{escape(e['labores'])}</li>" if e["labores"] else "") + f"<li><strong>⚠</strong> {escape(e['precaucion'])}</li></ul></details>")
        aviso = ('<div class="alerta"><p><strong>NUNCA comas una seta porque lo diga una ficha, una foto o una aplicación.</strong> Hay setas mortales que se parecen a las comestibles y los síntomas pueden tardar entre 6 horas y varios días en aparecer, cuando el daño ya es grave. '
                 'Identifícalas solo con una persona experta o con una sociedad micológica. Si has comido una seta dudosa y notas malestar, ve a urgencias con una muestra (112 o Toxicología: 91 562 04 20).</p>'
                 '<p>Recoge solo lo que necesites, en cesta de mimbre (no bolsa de plástico) y sin arrancar ni pisar las que no conoces. En algunos montes de Castilla y León hace falta permiso o hay normas de recolección: infórmate antes en el Ayuntamiento o en el servicio de medio ambiente. <em>(Dato por confirmar.)</em></p></div>')
        return "seta", f'{aviso}<div class="figuras una" style="background:#faf5e8">{svg}</div><p>{len(setas)} setas de la zona. Pulsa para abrir su ficha:</p>{det}', True
    if marker == "H:peligros":
        tox = sorted([e for e in esp if e["tipo"] == "tóxica"], key=lambda e: e["nombre"].lower())
        det = "".join(f'<details class="ficha"><summary><strong>{escape(e["nombre"])}</strong> <em>{escape(e["cientifico"])}</em></summary><ul class="guia" style="margin:.3rem 0"><li><strong>⚠</strong> {escape(e["precaucion"])}</li>'
                      + (f"<li>{escape(e['labores'])}</li>" if e["labores"] else "") + "</ul></details>" for e in tox)
        return "peligro", ('<div class="alerta"><p><strong>Plantas que parecen inofensivas y no lo son.</strong> No pruebes ninguna planta silvestre sin estar segura de cuál es, y enseña estas a niños y niñas: la cicuta se confunde con el perejil, '
                           'el cólquico con el ajo silvestre, y las bayas de la belladona atraen a los más pequeños. Ante cualquier duda tras comer una planta, llama al 112.</p></div>' + det), True
    # ───────── fauna y flora ─────────
    if not N: return "habitat", "<p>Sección en preparación.</p>", False
    aviso_n = f'<p class="nota">{escape(N.get("aviso", ""))}</p>'
    def aves_de(grupos):
        return [a for a in N["aves"] if a["grupo"] in grupos]
    def det_aves(lst):
        return "".join(f'<details class="ficha"><summary><strong>{escape(a["nombre"])}{" ★" if a["geoparque"] else ""}</strong> <em>{escape(a["cientifico"])}</em> · {"todo el año" if a["meses"] == "1-12" else fmt(a["meses"])}</summary>'
                       f'<ul class="guia" style="margin:.3rem 0"><li><strong>Dónde:</strong> {escape(a["donde"])}</li><li><strong>Cómo reconocerla:</strong> {escape(a["rasgo"])}</li><li>{escape(a["dato"])}</li></ul></details>' for a in lst)
    if marker == "N:habitats":
        return "habitat", "<ul class=\"guia\">" + "".join(f"<li><strong>{escape(h['nombre'])}.</strong> {escape(h['dato'])}</li>" for h in N["habitats"]) + f"</ul>{aviso_n}", False
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
            f'<details class="ficha"><summary><strong>{escape(m["nombre"])}</strong> <em>{escape(m["cientifico"])}</em></summary><ul class="guia" style="margin:.3rem 0"><li><strong>Dónde:</strong> {escape(m["donde"])}</li><li><strong>Cómo reconocerlo:</strong> {escape(m["rasgo"])}</li><li>{escape(m["dato"])}</li></ul></details>' for m in N["mamiferos"]) + aviso_n, True
    if marker == "N:reptiles":
        return "reptil", "<p>Reptiles y anfibios. Casi todos son inofensivos; la única víbora venenosa (áspid) se deja pasar y no se toca.</p>" + "".join(
            f'<details class="ficha"><summary><strong>{escape(r["nombre"])}</strong> <em>{escape(r["cientifico"])}</em> · {escape(r["grupo"])}</summary><ul class="guia" style="margin:.3rem 0"><li><strong>Dónde:</strong> {escape(r["donde"])}</li><li>{escape(r["dato"])}</li></ul></details>' for r in N["reptiles"]) + aviso_n, True
    if marker == "N:insectos":
        return "insecto", "<ul class=\"guia\">" + "".join(f"<li><strong>{escape(i['nombre'])}.</strong> {escape(i['dato'])}</li>" for i in N["insectos"]) + "</ul>", False
    if marker == "N:arboles":
        return "arbol", "<p>Árboles y arbustos del monte y los linderos. ★ = citado por fuentes del Geoparque.</p>" + "".join(
            f'<details class="ficha"><summary><strong>{escape(a["nombre"])}{" ★" if a["geoparque"] else ""}</strong> <em>{escape(a["cientifico"])}</em></summary><ul class="guia" style="margin:.3rem 0"><li>{escape(a["dato"])}</li></ul></details>' for a in N["arboles"]) + aviso_n, True
    if marker == "N:flora":
        return "flor", "<ul class=\"guia\">" + "".join(f"<li><strong>{escape(f['nombre'])}</strong> <em>{escape(f['cientifico'])}</em>. {escape(f['dato'])}</li>" for f in N["flora"]) + "</ul>", False
    if marker == "N:mirar":
        return "consejo", "<ul class=\"guia\">" + "".join(f"<li>{escape(x)}</li>" for x in N["mirar"]) + "</ul>", False
    return "habitat", "<p>En preparación.</p>", False
