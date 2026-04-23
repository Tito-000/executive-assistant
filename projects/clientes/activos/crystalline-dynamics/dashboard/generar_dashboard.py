#!/usr/bin/env python3
"""
Genera dashboard HTML del proyecto Crystalline Dynamics / Ocala Fence Install
leyendo tareas desde Motion API y escribiendo un HTML estetico.
"""
import urllib.request, json, os
from datetime import datetime

API_KEY = "DZ4rBKFQPEQdT1etPajO+ECXJym97X+Iu0FDF3kKG0Y="
PROJECT = "pr_tWthys7wB2LPBF5rFSeyfU"
OUTPUT = os.path.join(os.path.dirname(__file__), "index.html")

PHASES = [
    {"key": "F1", "name": "Fase 1 · Foundation", "color": "#136229", "bg": "#e8f5eb", "weeks": "Semanas 1-2"},
    {"key": "F2", "name": "Fase 2 · Lanzamiento", "color": "#d4a017", "bg": "#fdf6e3", "weeks": "Semanas 3-4"},
    {"key": "F3", "name": "Fase 3 · Optimizacion", "color": "#d97706", "bg": "#fff3e0", "weeks": "Semanas 5-8"},
    {"key": "F4", "name": "Fase 4 · Escalamiento", "color": "#991b1b", "bg": "#fde7e7", "weeks": "Semanas 9-12"},
]

def fetch_tasks():
    tasks = []
    cursor = None
    while True:
        url = f"https://api.usemotion.com/v1/tasks?projectId={PROJECT}"
        if cursor: url += f"&cursor={cursor}"
        r = urllib.request.Request(url)
        r.add_header("X-API-Key", API_KEY)
        r.add_header("User-Agent", "MM-Agency-PM/1.0")
        data = json.loads(urllib.request.urlopen(r).read())
        tasks += data.get("tasks", [])
        cursor = data.get("meta", {}).get("nextCursor")
        if not cursor: break
    return tasks

def fmt_date(iso):
    if not iso: return "—"
    try:
        d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return d.strftime("%d %b").lower()
    except:
        return "—"

def phase_of(name):
    for i, p in enumerate(PHASES):
        if name.startswith(p["key"] + ".") or name.startswith(p["key"] + " "):
            return i
    return 0

def build_html(tasks):
    # Ordenar tareas por número (F1.1, F1.2...)
    def sort_key(t):
        name = t["name"]
        try:
            num = float(name.split(" ")[0][1:])
        except:
            num = 0
        return num
    tasks.sort(key=sort_key)

    # Agrupar por fase
    by_phase = {i: [] for i in range(4)}
    for t in tasks:
        by_phase[phase_of(t["name"])].append(t)

    total = len(tasks)
    done = sum(1 for t in tasks if t.get("completed"))
    pct_total = round(done / total * 100) if total else 0

    # Generar HTML de fases
    phase_html = ""
    for i, phase in enumerate(PHASES):
        ptasks = by_phase[i]
        pdone = sum(1 for t in ptasks if t.get("completed"))
        ptotal = len(ptasks)
        pct = round(pdone / ptotal * 100) if ptotal else 0

        tasks_html = ""
        for t in ptasks:
            is_done = t.get("completed", False)
            status = t.get("status", {}).get("name", "Todo")
            is_hito = "[HITO]" in t["name"]
            name_clean = t["name"].replace(" [HITO]", "").replace("[HITO]", "")
            start = fmt_date(t.get("startOn") or t.get("scheduledStart"))
            due = fmt_date(t.get("dueDate"))
            status_class = "done" if is_done else ("progress" if status.lower() in ("in progress","doing") else "todo")
            status_label = "Completada" if is_done else ("En progreso" if status_class == "progress" else "Pendiente")

            tasks_html += f"""
            <div class="task {status_class}">
                <div class="task-check">{'✓' if is_done else ''}</div>
                <div class="task-body">
                    <div class="task-name">
                        {name_clean}
                        {' <span class="milestone">HITO</span>' if is_hito else ''}
                    </div>
                    <div class="task-meta">
                        <span class="task-dates">{start} → {due}</span>
                        <span class="task-status status-{status_class}">{status_label}</span>
                    </div>
                </div>
            </div>
            """

        phase_html += f"""
        <section class="phase" style="--phase-color: {phase['color']}; --phase-bg: {phase['bg']};">
            <header class="phase-header">
                <div class="phase-title-wrap">
                    <div class="phase-dot"></div>
                    <div>
                        <h2 class="phase-title">{phase['name']}</h2>
                        <div class="phase-sub">{phase['weeks']} · {pdone} de {ptotal} completadas</div>
                    </div>
                </div>
                <div class="phase-progress-wrap">
                    <div class="phase-pct">{pct}%</div>
                    <div class="phase-bar"><div class="phase-bar-fill" style="width: {pct}%"></div></div>
                </div>
            </header>
            <div class="tasks">{tasks_html}</div>
        </section>
        """

    updated_at = datetime.now().strftime("%d %B %Y · %I:%M %p").lower()

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>Ocala Fence Install · Project Dashboard · MM Agency</title>
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
.container {{ max-width: 1100px; margin: 0 auto; }}

/* HERO */
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
    margin-bottom: 30px;
    position: relative;
    z-index: 2;
}}
.hero-logo {{
    height: 32px;
    width: auto;
    opacity: 0.95;
}}
.hero-client {{
    font-size: 13px;
    color: #d1b487;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
}}
.hero-eyebrow {{
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: #d1b487;
    font-weight: 600;
    margin-bottom: 18px;
}}
.hero h1 {{
    font-family: 'Playfair Display', serif;
    font-size: 44px;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 10px;
}}
.hero-sub {{
    font-size: 17px;
    opacity: 0.85;
    font-weight: 300;
    max-width: 620px;
    margin-bottom: 35px;
}}

.hero-stats {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-top: 10px;
    position: relative;
    z-index: 2;
}}
.stat {{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 20px 18px;
    border-radius: 12px;
}}
.stat-num {{
    font-family: 'Playfair Display', serif;
    font-size: 36px;
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

.overall-bar {{
    margin-top: 30px;
    padding: 18px 20px;
    background: rgba(0,0,0,0.2);
    border-radius: 10px;
    position: relative;
    z-index: 2;
}}
.overall-bar-label {{
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
    opacity: 0.85;
}}
.overall-bar-track {{
    height: 8px;
    background: rgba(255,255,255,0.15);
    border-radius: 4px;
    overflow: hidden;
}}
.overall-bar-fill {{
    height: 100%;
    background: linear-gradient(90deg, #d1b487, #ffffff);
    border-radius: 4px;
    transition: width 1s ease;
}}

/* PHASES */
.phase {{
    background: white;
    border-radius: 16px;
    margin-bottom: 22px;
    padding: 30px 32px;
    border-left: 5px solid var(--phase-color);
    box-shadow: 0 4px 20px rgba(0,0,0,0.04);
}}
.phase-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
    padding-bottom: 18px;
    border-bottom: 1px solid #eee;
    flex-wrap: wrap;
    gap: 15px;
}}
.phase-title-wrap {{
    display: flex;
    align-items: center;
    gap: 14px;
}}
.phase-dot {{
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: var(--phase-color);
    box-shadow: 0 0 0 4px var(--phase-bg);
}}
.phase-title {{
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 700;
    color: #1a1a1a;
}}
.phase-sub {{
    font-size: 13px;
    color: #666;
    margin-top: 2px;
    font-weight: 500;
}}
.phase-progress-wrap {{
    display: flex;
    align-items: center;
    gap: 14px;
    min-width: 220px;
}}
.phase-pct {{
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    font-weight: 700;
    color: var(--phase-color);
    min-width: 55px;
}}
.phase-bar {{
    flex: 1;
    height: 8px;
    background: #f0f0f0;
    border-radius: 4px;
    overflow: hidden;
}}
.phase-bar-fill {{
    height: 100%;
    background: var(--phase-color);
    border-radius: 4px;
    transition: width 1s ease;
}}

/* TASKS */
.tasks {{ display: flex; flex-direction: column; gap: 10px; }}
.task {{
    display: flex;
    gap: 14px;
    padding: 14px 16px;
    background: var(--phase-bg);
    border-radius: 10px;
    align-items: flex-start;
    transition: transform 0.15s ease;
}}
.task:hover {{ transform: translateX(3px); }}
.task.done {{ opacity: 0.55; }}
.task.done .task-name {{ text-decoration: line-through; }}

.task-check {{
    width: 22px; height: 22px;
    border-radius: 50%;
    border: 2px solid var(--phase-color);
    background: white;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px;
    font-weight: 800;
    color: var(--phase-color);
    flex-shrink: 0;
    margin-top: 2px;
}}
.task.done .task-check {{
    background: var(--phase-color);
    color: white;
}}
.task-body {{ flex: 1; }}
.task-name {{
    font-weight: 600;
    font-size: 15px;
    color: #1a1a1a;
    margin-bottom: 4px;
}}
.milestone {{
    display: inline-block;
    font-size: 10px;
    padding: 2px 8px;
    background: var(--phase-color);
    color: white;
    border-radius: 4px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-left: 6px;
    vertical-align: middle;
}}
.task-meta {{
    display: flex;
    gap: 14px;
    font-size: 12px;
    color: #666;
    align-items: center;
    flex-wrap: wrap;
}}
.task-dates {{ font-family: 'SF Mono', Menlo, monospace; font-size: 11px; }}
.task-status {{
    padding: 3px 10px;
    border-radius: 12px;
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.status-done {{ background: #dcfce7; color: #166534; }}
.status-progress {{ background: #fef3c7; color: #92400e; }}
.status-todo {{ background: #f3f4f6; color: #4b5563; }}

/* FOOTER */
.footer {{
    text-align: center;
    padding: 40px 20px 10px;
    color: #666;
    font-size: 13px;
}}
.footer-logo {{
    height: 28px;
    width: auto;
    margin-bottom: 10px;
    opacity: 0.75;
}}
.footer-updated {{
    font-family: 'SF Mono', Menlo, monospace;
    font-size: 11px;
    color: #999;
    margin-top: 10px;
    letter-spacing: 0.5px;
}}

@media (max-width: 640px) {{
    body {{ padding: 20px 12px; }}
    .hero {{ padding: 35px 25px; }}
    .hero h1 {{ font-size: 32px; }}
    .hero-stats {{ grid-template-columns: repeat(2, 1fr); gap: 12px; }}
    .phase {{ padding: 22px 20px; }}
    .phase-header {{ flex-direction: column; align-items: flex-start; }}
    .phase-progress-wrap {{ width: 100%; }}
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
        <div class="hero-eyebrow">Project Dashboard</div>
        <h1>Fence Growth System</h1>
        <p class="hero-sub">Sistema de 12 semanas para llenar tu agenda de instalaciones en Ocala, FL. Tracking en tiempo real.</p>

        <div class="hero-stats">
            <div class="stat">
                <div class="stat-num">{total}</div>
                <div class="stat-label">Tareas totales</div>
            </div>
            <div class="stat">
                <div class="stat-num">{done}</div>
                <div class="stat-label">Completadas</div>
            </div>
            <div class="stat">
                <div class="stat-num">{total - done}</div>
                <div class="stat-label">Pendientes</div>
            </div>
            <div class="stat">
                <div class="stat-num">12</div>
                <div class="stat-label">Semanas</div>
            </div>
        </div>

        <div class="overall-bar">
            <div class="overall-bar-label">
                <span>Progreso total del proyecto</span>
                <span>{pct_total}%</span>
            </div>
            <div class="overall-bar-track">
                <div class="overall-bar-fill" style="width: {pct_total}%"></div>
            </div>
        </div>
    </div>

    {phase_html}

    <div class="footer">
        <img src="assets/mm-logo-dark.png" alt="MM Agency" class="footer-logo">
        <div>Martin Mercedes · martin@mmagency.do</div>
        <div class="footer-updated">Actualizado: {updated_at}</div>
    </div>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    tasks = fetch_tasks()
    html = build_html(tasks)
    with open(OUTPUT, "w") as f:
        f.write(html)
    print(f"✅ Dashboard generado: {OUTPUT}")
    print(f"   Tareas: {len(tasks)}")
