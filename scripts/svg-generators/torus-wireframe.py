#!/usr/bin/env python3
"""
Generador de torus 3D wireframe en SVG puro.

Usa parametrizacion matematica del torus:
    x(u,v) = (R + r*cos(v)) * cos(u)
    y(u,v) = (R + r*cos(v)) * sin(u)
    z(u,v) = r * sin(v)

Donde:
    R = radio principal del donut (del centro al centro del tubo)
    r = radio del tubo
    u = angulo alrededor del eje central (0..2pi)
    v = angulo alrededor de la seccion del tubo (0..2pi)

Despues aplica rotacion 3D (tilt en X) y proyeccion ortografica a 2D.

Output: SVG con wireframe lineal + superficie con gradiente violeta + contact shadow.
"""

import math

# ==================== CONFIGURACION ====================

CANVAS = 600                    # tamano del viewBox
CENTER_X = CANVAS / 2
CENTER_Y = CANVAS / 2 + 20      # un poco mas abajo para dejar espacio arriba

R = 170                         # radio principal
r = 70                          # radio del tubo (chunky)
TILT_DEG = 62                   # tilt del torus en el eje X (0=frontal, 90=top-down). 62 = perspectiva 3D fuerte

U_SEGMENTS = 48                 # numero de aros longitudinales (alrededor del donut)
V_SEGMENTS = 20                 # numero de aros latitudinales (alrededor del tubo)

# Colores
COLOR_DEEP = "#3D1F8C"          # sombra mas oscura (violeta profundo)
COLOR_MID = "#713DFF"           # violeta medio (MM Agency violet)
COLOR_LIGHT = "#C8A4FF"         # lila claro (highlight)
COLOR_WIRE = "#FFFFFF"          # wireframe
WIRE_OPACITY = 0.55
WIRE_WIDTH = 0.75

BG_TOP = "#15093A"              # indigo oscuro arriba
BG_BOTTOM = "#0A0A0A"           # casi negro abajo

# ==================== MATEMATICA ====================

tilt_rad = math.radians(TILT_DEG)
cos_t = math.cos(tilt_rad)
sin_t = math.sin(tilt_rad)

def torus_point(u, v):
    """Punto 3D en el torus para parametros u, v."""
    x = (R + r * math.cos(v)) * math.cos(u)
    y = (R + r * math.cos(v)) * math.sin(u)
    z = r * math.sin(v)
    return x, y, z

def rotate_and_project(x, y, z):
    """Rotacion X (tilt hacia adelante) + proyeccion ortografica a 2D.

    Rotacion X:
        y' = y*cos(t) - z*sin(t)
        z' = y*sin(t) + z*cos(t)

    Proyeccion: tomamos (x, y') como 2D. z' se usa para depth sorting.
    """
    y_rot = y * cos_t - z * sin_t
    z_rot = y * sin_t + z * cos_t
    return x + CENTER_X, y_rot + CENTER_Y, z_rot

def torus_normal(u, v):
    """Normal del torus en (u, v). Util para sombreado."""
    # Normal apunta radialmente desde el centro del tubo hacia afuera
    nx = math.cos(v) * math.cos(u)
    ny = math.cos(v) * math.sin(u)
    nz = math.sin(v)
    return nx, ny, nz

def rotate_normal(nx, ny, nz):
    """Aplica la misma rotacion X a la normal."""
    ny_rot = ny * cos_t - nz * sin_t
    nz_rot = ny * sin_t + nz * cos_t
    return nx, ny_rot, nz_rot

# Direccion de luz: upper-left, ligeramente al frente. Normalizado.
LIGHT_DIR = (-0.5, -0.6, -0.62)  # x, y, z (negativo z = hacia camara)
_mag = math.sqrt(sum(c*c for c in LIGHT_DIR))
LIGHT_DIR = tuple(c/_mag for c in LIGHT_DIR)

def shade_color(nx, ny, nz):
    """Calcula color interpolado entre DEEP, MID, LIGHT segun angulo con la luz."""
    # Dot product con la luz (-1 a 1)
    dot = nx*LIGHT_DIR[0] + ny*LIGHT_DIR[1] + nz*LIGHT_DIR[2]
    # Lambertian: max(0, -dot) porque LIGHT_DIR apunta DESDE la luz
    intensity = max(0.0, -dot)
    # Aplicar curva suave
    intensity = intensity ** 0.7

    # Interpolar: 0 = DEEP, 0.5 = MID, 1 = LIGHT
    if intensity < 0.5:
        t = intensity * 2
        return lerp_color(COLOR_DEEP, COLOR_MID, t)
    else:
        t = (intensity - 0.5) * 2
        return lerp_color(COLOR_MID, COLOR_LIGHT, t)

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*[max(0, min(255, int(round(c)))) for c in rgb])

def lerp_color(a, b, t):
    ra, ga, ba = hex_to_rgb(a)
    rb, gb, bb = hex_to_rgb(b)
    return rgb_to_hex((ra + (rb-ra)*t, ga + (gb-ga)*t, ba + (bb-ba)*t))

# ==================== GENERACION DE QUADS SOMBREADOS ====================

def build_shaded_quads():
    """
    Genera la superficie del torus como quads poligonales rellenos,
    cada uno sombreado segun su normal promedio.
    Ordenados por profundidad (painter's algorithm) para oclusion correcta.
    """
    quads = []
    U_SURF = 72   # mas denso para superficie suave
    V_SURF = 36

    for i in range(U_SURF):
        for j in range(V_SURF):
            u1 = 2*math.pi * i / U_SURF
            u2 = 2*math.pi * (i+1) / U_SURF
            v1 = 2*math.pi * j / V_SURF
            v2 = 2*math.pi * (j+1) / V_SURF

            # 4 vertices del quad
            p1 = torus_point(u1, v1)
            p2 = torus_point(u2, v1)
            p3 = torus_point(u2, v2)
            p4 = torus_point(u1, v2)

            proj = [rotate_and_project(*p) for p in (p1, p2, p3, p4)]

            # Profundidad promedio (z_rot promedio)
            avg_z = sum(pt[2] for pt in proj) / 4

            # Normal en el centro del quad
            u_mid = (u1 + u2) / 2
            v_mid = (v1 + v2) / 2
            nx, ny, nz = torus_normal(u_mid, v_mid)
            nx_r, ny_r, nz_r = rotate_normal(nx, ny, nz)

            # Backface culling: si la normal apunta hacia atras (nz > 0 hacia la camara),
            # el quad es visible. Camara mira hacia +z, asi que normal visible tiene nz_r < 0.
            # Lo conservamos todo y dejamos que painter's algorithm lo resuelva.
            color = shade_color(nx_r, ny_r, nz_r)

            quads.append((avg_z, proj, color))

    # Ordenar de atras hacia adelante (z alto primero = lejos)
    quads.sort(key=lambda q: q[0], reverse=True)
    return quads

def quad_to_path(proj):
    """Convierte 4 puntos proyectados a un path SVG cerrado."""
    (x1,y1,_), (x2,y2,_), (x3,y3,_), (x4,y4,_) = proj
    return f"M{x1:.2f},{y1:.2f} L{x2:.2f},{y2:.2f} L{x3:.2f},{y3:.2f} L{x4:.2f},{y4:.2f} Z"

# ==================== GENERACION DE WIREFRAME ====================

def build_wireframe_lines():
    """
    Genera las lineas del wireframe (u-loops y v-loops) como paths polyline.
    Cada linea se asocia a una profundidad promedio para ordenarlas.
    """
    lines = []
    SAMPLES = 60  # puntos por linea para suavidad

    # U-loops: v fijo, u varia (aros alrededor del donut)
    for j in range(V_SEGMENTS):
        v = 2*math.pi * j / V_SEGMENTS
        pts = []
        depths = []
        for k in range(SAMPLES + 1):
            u = 2*math.pi * k / SAMPLES
            x, y, z = torus_point(u, v)
            px, py, pz = rotate_and_project(x, y, z)
            pts.append((px, py))
            depths.append(pz)
        avg_depth = sum(depths) / len(depths)
        lines.append((avg_depth, pts, "u"))

    # V-loops: u fijo, v varia (aros alrededor de la seccion del tubo)
    for i in range(U_SEGMENTS):
        u = 2*math.pi * i / U_SEGMENTS
        pts = []
        depths = []
        for k in range(SAMPLES + 1):
            v = 2*math.pi * k / SAMPLES
            x, y, z = torus_point(u, v)
            px, py, pz = rotate_and_project(x, y, z)
            pts.append((px, py))
            depths.append(pz)
        avg_depth = sum(depths) / len(depths)
        lines.append((avg_depth, pts, "v"))

    return lines

def pts_to_path(pts):
    if not pts:
        return ""
    d = f"M{pts[0][0]:.2f},{pts[0][1]:.2f}"
    for x, y in pts[1:]:
        d += f" L{x:.2f},{y:.2f}"
    return d

# ==================== ENSAMBLAJE SVG ====================

def build_svg():
    quads = build_shaded_quads()
    wires = build_wireframe_lines()

    # Separar wires en "back" (detras del centro del torus) y "front"
    # back: avg_depth > 0 (lejos de camara, z positivo despues de rotacion)
    # front: avg_depth < 0 (cerca)
    back_wires = [w for w in wires if w[0] > 0]
    front_wires = [w for w in wires if w[0] <= 0]

    # Construir paths de superficie
    surface_paths = []
    for _, proj, color in quads:
        d = quad_to_path(proj)
        surface_paths.append(f'<path d="{d}" fill="{color}" stroke="none"/>')

    back_wire_paths = []
    for _, pts, _ in back_wires:
        d = pts_to_path(pts)
        back_wire_paths.append(
            f'<path d="{d}" fill="none" stroke="{COLOR_WIRE}" '
            f'stroke-width="{WIRE_WIDTH}" stroke-opacity="{WIRE_OPACITY * 0.35}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )

    front_wire_paths = []
    for _, pts, _ in front_wires:
        d = pts_to_path(pts)
        front_wire_paths.append(
            f'<path d="{d}" fill="none" stroke="{COLOR_WIRE}" '
            f'stroke-width="{WIRE_WIDTH}" stroke-opacity="{WIRE_OPACITY}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )

    # Contact shadow: elipse aplastada debajo del torus
    shadow_cy = CENTER_Y + R * sin_t + r * 0.4
    shadow_rx = R * 0.95
    shadow_ry = 14

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS} {CANVAS}">
  <defs>
    <radialGradient id="bg" cx="50%" cy="40%" r="75%">
      <stop offset="0%" stop-color="{BG_TOP}"/>
      <stop offset="100%" stop-color="{BG_BOTTOM}"/>
    </radialGradient>
    <radialGradient id="shadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Background -->
  <rect width="{CANVAS}" height="{CANVAS}" fill="url(#bg)"/>

  <!-- Contact shadow debajo del torus -->
  <ellipse cx="{CENTER_X}" cy="{shadow_cy}" rx="{shadow_rx}" ry="{shadow_ry}" fill="url(#shadow)"/>

  <!-- Surface (painter's order, back to front) -->
  <g id="surface">
    {chr(10).join("    " + p for p in surface_paths)}
  </g>

  <!-- Back wireframe (atenuado, detras de la superficie visible pero visible entre quads) -->
  <g id="wire-back" opacity="0.6">
    {chr(10).join("    " + p for p in back_wire_paths)}
  </g>

  <!-- Front wireframe (encima de la superficie) -->
  <g id="wire-front">
    {chr(10).join("    " + p for p in front_wire_paths)}
  </g>
</svg>
'''
    return svg

# ==================== MAIN ====================

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "torus-violet.svg"
    svg = build_svg()
    with open(out, "w") as f:
        f.write(svg)
    print(f"Generated {out}")
