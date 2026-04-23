#!/usr/bin/env python3
"""Genera reporte HTML de Keyword Research para Ocala Fence Install."""
import csv, os, shutil
from collections import defaultdict

HERE = os.path.dirname(__file__)
CSV_PATH = os.path.join(HERE, "keywords.csv")
OUT = os.path.join(HERE, "index.html")

CLUSTERS = {
    "money": {"name": "Money Keywords", "desc": "Intent transaccional alto — usuario listo para comprar. Prioridad #1.", "color": "#136229", "bg": "#e8f5eb"},
    "near-me": {"name": "Near Me / Geo-Intent", "desc": "Se ganan con Google Business Profile + proximity + reviews. Muy volumen pero pago alto en ads.", "color": "#0d4a1f", "bg": "#e8f5eb"},
    "product": {"name": "Productos (Vinyl / Aluminum / Privacy / Pool)", "desc": "Una landing dedicada por producto. Captura intent especifico.", "color": "#d4a017", "bg": "#fdf6e3"},
    "product-niche": {"name": "Durafence (nicho)", "desc": "Poca competencia SEO — oportunidad de capturar 100% del search volume.", "color": "#b8860b", "bg": "#fdf6e3"},
    "geo-zip": {"name": "ZIPs de Ocala", "desc": "SEO programatico — 1 pagina por ZIP con info local unica.", "color": "#d97706", "bg": "#fff3e0"},
    "geo-county": {"name": "Marion County", "desc": "Capturar a nivel condado.", "color": "#c2410c", "bg": "#fff3e0"},
    "nearby-city": {"name": "Ciudades vecinas (The Villages, Belleview, Summerfield)", "desc": "Expansion geografica — The Villages es el mercado grande al sur.", "color": "#ea580c", "bg": "#fff3e0"},
    "financing": {"name": "Financiamiento ($0 Down)", "desc": "USP principal del cliente — landing dedicada con CTA al aplicador.", "color": "#991b1b", "bg": "#fde7e7"},
    "hispanic": {"name": "Mercado Hispano", "desc": "USP del cliente (habla espanol). Crear version en espanol.", "color": "#7c2d12", "bg": "#fde7e7"},
    "blog": {"name": "Blog / Content SEO", "desc": "Trafico informacional — convertir a leads via lead magnet.", "color": "#4c1d95", "bg": "#ede9fe"},
    "service": {"name": "Servicios y CTAs", "desc": "Quick-win con 'free estimate' y 'same-day'.", "color": "#1e40af", "bg": "#dbeafe"},
    "": {"name": "Negative Keywords (para Google Ads)", "desc": "Excluir en todas las campanas — wood, chain link, repair, DIY, jobs, rental.", "color": "#64748b", "bg": "#f1f5f9"},
}

PRIORITY_ORDER = {"P1": 1, "P2": 2, "P3": 3}

def load():
    with open(CSV_PATH) as f:
        return list(csv.DictReader(f))

def format_cpc(v):
    try: return f"${float(v):.2f}"
    except: return "—"

def format_vol(v):
    try:
        n = int(v)
        if n >= 1000: return f"{n/1000:.1f}k"
        return str(n)
    except: return "—"

def intent_badge(intent):
    colors = {
        "transactional": ("#dcfce7", "#166534"),
        "commercial": ("#fef3c7", "#92400e"),
        "informational": ("#e0e7ff", "#3730a3"),
    }
    bg, fg = colors.get(intent, ("#f3f4f6", "#4b5563"))
    return f'<span class="badge" style="background:{bg};color:{fg}">{intent}</span>'

def comp_badge(c):
    colors = {"high": ("#fee2e2", "#991b1b"), "medium": ("#fef3c7", "#92400e"), "low": ("#dcfce7", "#166534")}
    bg, fg = colors.get(c, ("#f3f4f6", "#4b5563"))
    return f'<span class="badge" style="background:{bg};color:{fg}">{c}</span>'

def priority_badge(p):
    colors = {"P1": ("#fee2e2", "#991b1b"), "P2": ("#fef3c7", "#92400e"), "P3": ("#e0e7ff", "#3730a3")}
    bg, fg = colors.get(p, ("#f3f4f6", "#4b5563"))
    return f'<span class="badge prio" style="background:{bg};color:{fg}">{p}</span>'

def build():
    rows = load()
    total = len(rows)
    total_vol = sum(int(r["monthly_volume"]) for r in rows if r["monthly_volume"].isdigit())
    by_cluster = defaultdict(list)
    for r in rows:
        by_cluster[r["cluster"]].append(r)
    p1_count = sum(1 for r in rows if r["priority"] == "P1")
    avg_cpc = sum(float(r["cpc_usd"]) for r in rows) / total

    cluster_html = ""
    cluster_order = ["money","near-me","product","product-niche","geo-zip","geo-county","nearby-city","financing","hispanic","service","blog",""]
    for cl in cluster_order:
        if cl not in by_cluster: continue
        info = CLUSTERS.get(cl, {"name": cl, "desc":"", "color":"#333", "bg":"#eee"})
        items = sorted(by_cluster[cl], key=lambda r: (PRIORITY_ORDER.get(r["priority"],9), -int(r["monthly_volume"] or 0)))
        total_cluster_vol = sum(int(r["monthly_volume"]) for r in items if r["monthly_volume"].isdigit())

        rows_html = ""
        for r in items:
            notes = r.get("notes","").replace('"',"&quot;")
            target = r.get("target_page","") or "<em style='color:#aaa'>excluir</em>"
            rows_html += f"""
            <tr>
                <td class="kw">{r["keyword"]}</td>
                <td class="num">{format_vol(r["monthly_volume"])}</td>
                <td class="num">{format_cpc(r["cpc_usd"])}</td>
                <td>{comp_badge(r["competition"])}</td>
                <td>{intent_badge(r["intent"])}</td>
                <td>{priority_badge(r["priority"])}</td>
                <td class="target">{target}</td>
                <td class="notes">{notes}</td>
            </tr>
            """

        cluster_html += f"""
        <section class="cluster" style="--cluster-color:{info['color']};--cluster-bg:{info['bg']}">
            <header class="cluster-head">
                <div class="cluster-dot"></div>
                <div class="cluster-meta">
                    <h2>{info['name']}</h2>
                    <p>{info['desc']}</p>
                </div>
                <div class="cluster-stats">
                    <div><strong>{len(items)}</strong><span>keywords</span></div>
                    <div><strong>{format_vol(total_cluster_vol)}</strong><span>vol/mes</span></div>
                </div>
            </header>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>Keyword</th><th>Vol</th><th>CPC</th><th>Comp</th><th>Intent</th><th>Prio</th><th>Target Page</th><th>Notas</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
        </section>
        """

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Keyword Research · Ocala Fence Install · MM Agency</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: 'Inter', -apple-system, sans-serif;
    background: linear-gradient(135deg, #fafaf5 0%, #f5f0e8 100%);
    color: #1a1a1a;
    min-height: 100vh;
    line-height: 1.5;
    padding: 40px 20px;
}}
.container {{ max-width: 1300px; margin: 0 auto; }}

.hero {{
    background: linear-gradient(135deg, #136229 0%, #0d4a1f 100%);
    color: white;
    padding: 50px 45px;
    border-radius: 20px;
    margin-bottom: 35px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(19,98,41,0.25);
}}
.hero::before {{
    content: '';
    position: absolute;
    top: -50%; right: -20%;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(209,180,135,0.15) 0%, transparent 70%);
    pointer-events: none;
}}
.hero-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
    position: relative;
    z-index: 2;
}}
.hero-logo {{ height: 32px; opacity: 0.95; }}
.hero-client {{
    font-size: 13px;
    color: #d1b487;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
}}
.hero h1 {{
    font-family: 'Playfair Display', serif;
    font-size: 44px;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 12px;
}}
.hero-sub {{
    font-size: 17px;
    opacity: 0.85;
    max-width: 720px;
    margin-bottom: 30px;
    font-weight: 300;
}}
.hero-stats {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    position: relative;
    z-index: 2;
}}
.stat {{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 20px;
    border-radius: 12px;
}}
.stat-num {{
    font-family: 'Playfair Display', serif;
    font-size: 34px;
    font-weight: 800;
    line-height: 1;
}}
.stat-label {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    opacity: 0.75;
    margin-top: 6px;
    font-weight: 500;
}}

/* Executive summary */
.summary {{
    background: white;
    border-radius: 16px;
    padding: 30px 35px;
    margin-bottom: 30px;
    border-left: 5px solid #d1b487;
    box-shadow: 0 4px 20px rgba(0,0,0,0.04);
}}
.summary h2 {{
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    margin-bottom: 14px;
    color: #136229;
}}
.summary p {{ margin-bottom: 10px; color: #444; }}
.summary ul {{ padding-left: 22px; margin: 10px 0 14px; }}
.summary li {{ margin-bottom: 6px; color: #444; }}
.summary strong {{ color: #136229; }}

/* Cluster section */
.cluster {{
    background: white;
    border-radius: 16px;
    margin-bottom: 24px;
    padding: 30px 32px;
    border-left: 5px solid var(--cluster-color);
    box-shadow: 0 4px 20px rgba(0,0,0,0.04);
}}
.cluster-head {{
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 22px;
    padding-bottom: 18px;
    border-bottom: 1px solid #eee;
    flex-wrap: wrap;
}}
.cluster-dot {{
    width: 14px; height: 14px;
    border-radius: 50%;
    background: var(--cluster-color);
    box-shadow: 0 0 0 4px var(--cluster-bg);
    flex-shrink: 0;
}}
.cluster-meta {{ flex: 1; min-width: 280px; }}
.cluster-meta h2 {{
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    color: #1a1a1a;
    margin-bottom: 3px;
}}
.cluster-meta p {{ font-size: 13px; color: #666; }}
.cluster-stats {{
    display: flex;
    gap: 22px;
    font-size: 12px;
    color: #666;
}}
.cluster-stats strong {{
    display: block;
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    color: var(--cluster-color);
    font-weight: 700;
    line-height: 1;
    margin-bottom: 2px;
}}
.cluster-stats span {{ text-transform: uppercase; letter-spacing: 1px; font-size: 10px; }}

/* Table */
.table-wrap {{ overflow-x: auto; }}
table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}}
th {{
    text-align: left;
    padding: 10px 12px;
    background: var(--cluster-bg);
    color: var(--cluster-color);
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 2px solid var(--cluster-color);
    white-space: nowrap;
}}
td {{
    padding: 11px 12px;
    border-bottom: 1px solid #f0f0f0;
    vertical-align: top;
}}
td.kw {{ font-weight: 600; color: #1a1a1a; }}
td.num {{ font-family: 'SF Mono', Menlo, monospace; font-size: 12px; font-weight: 600; }}
td.target {{ font-size: 12px; color: #555; font-family: 'SF Mono', Menlo, monospace; }}
td.notes {{ font-size: 12px; color: #666; max-width: 260px; }}

.badge {{
    display: inline-block;
    padding: 3px 9px;
    border-radius: 10px;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.badge.prio {{ font-family: 'SF Mono', Menlo, monospace; }}

.footer {{
    text-align: center;
    padding: 40px 20px 10px;
    color: #666;
    font-size: 13px;
}}
.footer-logo {{
    height: 28px;
    margin-bottom: 10px;
    opacity: 0.75;
}}

@media (max-width: 640px) {{
    body {{ padding: 20px 10px; }}
    .hero {{ padding: 32px 22px; }}
    .hero h1 {{ font-size: 30px; }}
    .hero-stats {{ grid-template-columns: repeat(2, 1fr); }}
    .cluster {{ padding: 22px 18px; }}
    .cluster-head {{ flex-direction: column; align-items: flex-start; }}
    table {{ font-size: 11px; }}
    th, td {{ padding: 8px 6px; }}
}}
</style>
</head>
<body>
<div class="container">
    <div class="hero">
        <div class="hero-top">
            <img src="assets/mm-logo-white.png" alt="MM Agency" class="hero-logo">
            <div class="hero-client">Ocala Fence Install</div>
        </div>
        <h1>Keyword Research</h1>
        <p class="hero-sub">Universo de búsqueda para dominar el SEO local y pagado de Ocala, FL. {total} keywords analizadas, segmentadas por intent y clusterizadas para ejecución.</p>
        <div class="hero-stats">
            <div class="stat"><div class="stat-num">{total}</div><div class="stat-label">Keywords</div></div>
            <div class="stat"><div class="stat-num">{format_vol(total_vol)}</div><div class="stat-label">Vol/mes total</div></div>
            <div class="stat"><div class="stat-num">{p1_count}</div><div class="stat-label">Prioridad 1</div></div>
            <div class="stat"><div class="stat-num">${avg_cpc:.2f}</div><div class="stat-label">CPC promedio</div></div>
        </div>
    </div>

    <section class="summary">
        <h2>Resumen Ejecutivo</h2>
        <p>El mercado de fencing en Ocala tiene <strong>{format_vol(total_vol)} búsquedas mensuales capturables</strong> cruzando SEO orgánico + Google Ads. Estrategia propuesta:</p>
        <ul>
            <li><strong>Homepage:</strong> optimizada para "fence company ocala fl" + "fence contractor ocala fl" (money kw #1 y #2, combinados 530 vol/mes).</li>
            <li><strong>4 service pages:</strong> Vinyl, Aluminum, Privacy, Pool — una landing por producto con intent de compra directa.</li>
            <li><strong>Landing $0 Down Financing:</strong> USP diferenciador. Captura búsquedas que la competencia no trabaja (Fence Pro, Perimeter Fence, Ocala Fence no rankean para estas).</li>
            <li><strong>6 páginas por ZIP (34471-34480):</strong> SEO programático. Bajo volumen por página pero alta conversión (local intent máximo).</li>
            <li><strong>The Villages page:</strong> The Villages = mercado grande al sur con 90 vol/mes. Oportunidad clara.</li>
            <li><strong>Landing en español:</strong> USP del cliente (habla español) + mercado hispano grande en Marion County sin competencia.</li>
            <li><strong>Blog hub:</strong> "how much does a fence cost in florida" (590 vol/mes) como pillar content + 6 artículos de soporte.</li>
            <li><strong>Negative keywords (Ads):</strong> excluir wood, chain link, repair, DIY, jobs, rental, used — salva presupuesto.</li>
        </ul>
        <p><strong>Ángulo diferenciador clave (del briefing):</strong> "fence for bears florida" (90 vol/mes) es un blog post que nadie en Ocala tiene escrito — se puede ganar 100% del SERP con un artículo bien hecho.</p>
    </section>

    {cluster_html}

    <div class="footer">
        <img src="assets/mm-logo-dark.png" alt="MM Agency" class="footer-logo">
        <div>Martin Mercedes · martin@mmagency.do · MM Agency</div>
    </div>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    # Copiar logos
    src = os.path.abspath(os.path.join(HERE, "../../dashboard/assets"))
    dst = os.path.join(HERE, "assets")
    if os.path.exists(src):
        os.makedirs(dst, exist_ok=True)
        for f in os.listdir(src):
            shutil.copy(os.path.join(src,f), os.path.join(dst,f))
    html = build()
    with open(OUT,"w") as f:
        f.write(html)
    print(f"✅ Reporte: {OUT}")
