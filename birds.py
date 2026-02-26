import math
import sys
import pygame
import random

# ----------------------------
# Config
# ----------------------------
W, H = 960, 540
FPS = 60

SKY = (235, 245, 255)
GROUND = (210, 235, 210)
BLACK = (25, 25, 25) 
BIRD_A = (245, 120, 169)   # bailarín
BIRD_A_WING = tuple(min(255, int(c * 0.9)) for c in BIRD_A) 
BIRD_B = (164, 69, 45)   # espectador (color café, que no tiene nada de malo)
BIRD_B_WING = (255, 192, 31) # Color onitsika tiger
WHITE = (250, 250, 250)

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Bird Courtship Dance (Python + Pygame)")
clock = pygame.time.Clock()

import pygame
import math

#----------------------------
#Funciones
#----------------------------

def draw_cap_simple(head_surf, hc, scale=1.0, color=(30, 30, 30), facing=1, backwards=True):
    """
    Dibuja una gorra.
    - head_surf: Surface donde se dibuja (la cabeza)
    - hc: centro (x,y) de la cabeza dentro de head_surf
    - facing: 1 mira derecha, -1 mira izquierda
    - backwards: True = visera hacia atrás (opuesto a donde mira)
    """

    # Tamaños relativos 
    dome_w = int(64 * scale)
    dome_h = int(52 * scale)

    brim_w = int(56 * scale)
    brim_h = int(20 * scale)

    # Posición base (encima de la cabeza)
    dome_rect = pygame.Rect(0, 0, dome_w, dome_h)
    dome_rect.center = (int(hc[0] - 2 * scale), int(hc[1] - 34 * scale))

    # Hacia dónde va la visera
    # forward_dir = dirección hacia donde mira el pájaro
    forward_dir = facing
    brim_dir = facing

    brim_rect = pygame.Rect(0, 0, brim_w, brim_h)
    brim_rect.center = (
        int(dome_rect.centerx + brim_dir * (dome_w * 0.42)),
        int(dome_rect.centery + (dome_h * 0.28))
    )

    # 1) Cúpula
    pygame.draw.ellipse(head_surf, color, dome_rect)

   # 2) Visera
    pygame.draw.ellipse(head_surf, color, brim_rect)

    # 3) Línea inferior para profundidad (comentar para ultra plano)
    pygame.draw.arc(head_surf, (0, 0, 0), dome_rect, math.radians(200), math.radians(340), max(1, int(3 * scale)))

def draw_bird(surface, x, y, color, wing_color, scale=1.0, tilt=0.0, wing=0.0, blush=0.0,
              facing=1, head_bob=0.0, head_tilt=0.0, cap=False, cap_backwards=True,
              spin=0.0, body_rot=0.0, turn_x=1.0):
    """
    Dibuja un pajarito estilizado con:
    - tilt: inclinación (radianes)
    - wing: aleteo (0..1)
    - blush: rubor/amor (0..1)
    """
    bw0, bh0 = int(220 * scale), int(160 * scale)

    pad_x = int(120 * scale)
    pad_top = int(160 * scale)  # margen EXTRA arriba para que no parezca que la gorra se recorta
    pad_bottom = int(60 * scale)

    bw = bw0 + pad_x
    bh = bh0 + pad_top + pad_bottom

    bird_surf = pygame.Surface((bw, bh), pygame.SRCALPHA)

    # Centro "real" del pájaro, pero empujado hacia abajo para dejar aire arriba
    cx = bw * 0.5
    cy = (bh0 * 0.55) + pad_top

    # Cuerpo (óvalo)
    body_rect = pygame.Rect(0, 0, 140 * scale, 90 * scale)
    body_rect.center = (cx, cy)
    pygame.draw.ellipse(bird_surf, color, body_rect)

    # Ala (triángulo) con "wing" para abrir/cerrar
    wing_open = 20 * scale + 35 * scale * wing
    wing_pts = [
        (cx - 10 * scale, cy),
        (cx - 70 * scale, cy - wing_open),
        (cx - 60 * scale, cy + wing_open * 0.35),
    ]
    pygame.draw.polygon(bird_surf, wing_color, wing_pts)

    pad = int(200 * scale)  # margen extra para que no se recorte la gorra al rotar
    head_w, head_h = int(140 * scale) + pad, int(140 * scale) + pad
    head_surf = pygame.Surface((head_w, head_h), pygame.SRCALPHA)


    # Centro local de la cabeza en head_surf
    hc = (head_w * 0.5, head_h * 0.5)

    # Cabeza (círculo)
    pygame.draw.circle(head_surf, color, (int(hc[0]), int(hc[1])), int(32 * scale))

    # Ojo
    eye = (int(hc[0] + 10 * scale), int(hc[1] - 5 * scale))
    pygame.draw.circle(head_surf, BLACK, eye, int(6 * scale))
    pygame.draw.circle(head_surf, WHITE, (eye[0] - int(2 * scale), eye[1] - int(2 * scale)), int(2 * scale))

    # Pico (triángulo)
    beak_pts = [
        (hc[0] + 28 * scale, hc[1] + 2 * scale),
        (hc[0] + 58 * scale, hc[1] + 12 * scale),
        (hc[0] + 28 * scale, hc[1] + 18 * scale),
    ]
    pygame.draw.polygon(head_surf, (240, 200, 60), [(int(px), int(py)) for px, py in beak_pts])
    
    # Gorra
    if cap:
        draw_cap_simple(
        head_surf,
        hc,
        scale=scale,
        color=(46, 41, 41),   # color único
        facing=facing,
        backwards=True        # gorra hacia atrás
        )

    # Patitas
    leg_y = cy + 40 * scale
    for dx in (-20 * scale, 5 * scale):
        x0 = cx + dx
        pygame.draw.line(bird_surf, BLACK, (int(x0), int(leg_y)), (int(x0), int(leg_y + 25 * scale)), int(4 * scale))


    # Rubor (mejillas)
    if blush > 0:
        cheek_color = (247, 7, 41)
        min_alpha = 30     # no desaparece del todo
        max_alpha = 160

        alpha = int(min_alpha + (max_alpha - min_alpha) * blush)
        pygame.draw.circle(head_surf, (*cheek_color, alpha), (int(hc[0] + 2 * scale), int(hc[1] + 14 * scale)), int(10 * scale))
        pygame.draw.circle(head_surf, (*cheek_color, alpha), (int(hc[0] + 18 * scale), int(hc[1] + 16 * scale)), int(8 * scale))

    # Rotar solo la cabeza (si miras al otro lado, invierte el giro para que se sienta natural)
    head_angle = -math.degrees(head_tilt) * facing
    head_rot = pygame.transform.rotate(head_surf, head_angle)

    # Posición donde “va” la cabeza respecto al cuerpo (en bird_surf)
    head_base_x = cx + 60 * scale
    head_base_y = cy - 30 * scale + head_bob  # SOLO la cabeza sube/baja

    head_rect = head_rot.get_rect(center=(head_base_x, head_base_y))
    bird_surf.blit(head_rot, head_rect.topleft)


    # --- Turn suave ---
    # turn_x: +1 mira normal, -1 volteado. Cerca de 0 se "aplana" para simular giro.
    sx = max(0.08, abs(turn_x))
    new_w = max(1, int(bird_surf.get_width() * sx))
    bird_surf = pygame.transform.smoothscale(bird_surf, (new_w, bird_surf.get_height()))

    if turn_x < 0:
        bird_surf = pygame.transform.flip(bird_surf, True, False)

    # facing 
    if facing == -1:
        bird_surf = pygame.transform.flip(bird_surf, True, False)

    # Rotamos todo el pájaro segun tilt
    rotated = pygame.transform.rotate(bird_surf, -math.degrees(tilt + body_rot + spin))
 

    rect = rotated.get_rect(center=(x, y))
    surface.blit(rotated, rect.topleft)

def draw_heart(surface, x, y, size, alpha=200):
    heart = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    c = (255, 80, 120, alpha)
    r = int(size * 0.6)
    pygame.draw.circle(heart, c, (int(size * 0.7), int(size * 0.7)), r)
    pygame.draw.circle(heart, c, (int(size * 1.3), int(size * 0.7)), r)
    pts = [(size * 0.2, size * 0.9), (size, size * 1.8), (size * 1.8, size * 0.9)]
    pygame.draw.polygon(heart, c, [(int(px), int(py)) for px, py in pts])
    surface.blit(heart, (int(x - size), int(y - size)))

def ease_in_out(u):
    u = max(0.0, min(1.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u)

def ramp(tau, start, dur):
    if tau <= start: return 0.0
    if tau >= start + dur: return 1.0
    return ease_in_out((tau - start) / dur)

t = 0.0
running = True

# Posiciones base
left_x, right_x = int(W * 0.33), int(W * 0.70)
ground_y = int(H * 0.72)

hearts = []

# Rutina del bailarín
dance_cycle = 5.2  # duración total del ciclo (segundos)

# Duraciones por fase (suman ~ dance_cycle)
T_TURN_OUT = 0.35
T_BACKSTEP = 1.10
T_RETURN = 1.10
T_PREP = 0.45
T_SPIN = 1.00
T_HOLD = 1.10  

# Distancia de "pasos hacia atrás"
BACK_DIST = 90  # px 

pygame.init()

#----------------------------
# Loop principal
#----------------------------

pygame.mixer.init()
pygame.mixer.music.load("quevashacer.mp3")
pygame.mixer.music.set_volume(0.5)  # volumen 0.0 - 1.0
pygame.mixer.music.play(-1)  # -1 = loop infinito

while running:
    dt = clock.tick(FPS) / 1000.0
    t += dt

    # ----------------------------
    # Eventos
    # ----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos

            for i in range(12):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(80, 160)

                hearts.append({
                    "x": mouse_x,
                    "y": mouse_y,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": 1.4,
                    "age": 0.0,
                    "phase": i * 0.5
                })

    # ----------------------------
    # Fondo
    # ----------------------------
    screen.fill(SKY)
    pygame.draw.rect(screen, GROUND, (0, ground_y, W, H - ground_y))

    # ----------------------------
    # Parámetros comunes
    # ----------------------------
    blush = 0.5 + 0.5 * math.sin(t * 0.8)


    # ============================
    # PÁJARO ROSA (BAILARÍN)
    # ============================
    # Ciclo completo de rutina (ajusta a gusto)
    cycle = 6.0 + T_HOLD
    tau = (t % cycle)

    # Duraciones
    T_TURN_AWAY = 0.35   # girarse para dar la espalda
    T_BACKWALK  = 1.10   # caminar hacia el café (perreo)
    T_FWDWALK   = 1.10   # de regreso a su lugar
    T_TURN_BACK = 0.35   # girarse para ver al café otra vez
    T_SPIN      = 1.00   # giro 360
 

    # Distancia que se acerca
    BACK_DIST = 110  # px

    # Marcadores de tiempo
    t1 = T_TURN_AWAY
    t2 = t1 + T_BACKWALK
    t3 = t2 + T_FWDWALK
    t4 = t3 + T_TURN_BACK
    t5 = t4 + T_SPIN
    t6 = t5 + T_HOLD

    # Dirección hacia el café (café está a la derecha)
    toward_dir = 1 if (right_x > left_x) else -1

    # --- Offset de caminata (se acerca de espaldas, luego regresa de frente) ---
    move_u = 0.0
    walk_offset = 0.0
    step_wiggle = 0.0

    if tau < t1:
        # aún no camina
        move_u = 0.0
        walk_offset = 0.0

    elif tau < t2:
        # BACKWALK: offset 0 -> BACK_DIST (se acerca)
        u = ramp(tau, t1, T_BACKWALK)   # 0..1 suave
        move_u = u
        walk_offset = toward_dir * (BACK_DIST * u)

        # pasitos (solo mientras se mueve)
        step_wiggle = toward_dir * (7 * math.sin(2 * math.pi * 3 * u) * u)

    elif tau < t3:
        # FWDWALK: offset BACK_DIST -> 0 (regresa)
        u = ramp(tau, t2, T_FWDWALK)    # 0..1 suave
        move_u = 1.0 - u
        walk_offset = toward_dir * (BACK_DIST * (1.0 - u))

        step_wiggle = toward_dir * (7 * math.sin(2 * math.pi * 3 * u) * (1.0 - u))

    else:
        move_u = 0.0
        walk_offset = 0.0
        step_wiggle = 0.0

    walk_offset += step_wiggle

    # --- Giro "de espalda"  ---
    # turn_x va de +1 (mirando al café) a -1 (dándole la espalda)
    if tau < t1:
        u = ramp(tau, 0.0, T_TURN_AWAY)    # 0..1
        theta = math.pi * u
        turn_x = math.cos(theta)           # 1 -> -1 suave (aplastado al centro)
    elif tau < t3:
        turn_x = -1.0                      # totalmente de espaldas mientras camina
    elif tau < t4:
        u = ramp(tau, t3, T_TURN_BACK)     # 0..1
        theta = math.pi * u
        turn_x = -math.cos(theta)          # -1 -> +1 suave
    else:
        turn_x = 1.0

    # --- Spin 360 ya que regresó y mira al café ---
    if (tau >= t4) and (tau < t5):
        u = ease_in_out((tau - t4) / T_SPIN)
        spin = 2 * math.pi * u
    else:
        spin = 0.0

    # --- Movimiento base ---
    # Bounce original solo mientras camina,
    bounce_base = 18 * abs(math.sin(t * 2.4))
    bounce = bounce_base * (1.0 - 0.35 * min(1.0, move_u))   # reduce hasta 35% durante caminata

    sway = 22 * math.sin(t * 1.2)
    tilt = 0.25 * math.sin(t * 2.2)
    wing = 0.5 + 0.5 * math.sin(t * 8.0)

    dancer_x = left_x + sway + walk_offset
    dancer_y = ground_y - 60 - bounce

    draw_bird(
    screen, dancer_x, dancer_y, BIRD_A, BIRD_A_WING,
    scale=1.0, tilt=tilt, wing=wing, blush=0.6 * blush,
    facing=1,
    spin=spin,
    body_rot=0.0,     
    turn_x=turn_x    
    )


    # ============================
    # PÁJARO CAFÉ (OBSERVA)
    # ============================
    watcher_x = right_x
    watcher_y = ground_y - 55   # cuerpo fijo 

    head_bob = 6 * math.sin(t * 1.3)         # solo cabeza
    head_tilt = -0.18 * math.sin(t * 1.6)

    # Aleteo suave siempre positivo rango aprox: 0.06 .. 0.14
    reaction_boost = 0.2 if spin > 0.1 else 0.0
    wing_watcher = 0.1 + reaction_boost + 0.03 * math.sin(t * 2.0)

    draw_bird(
        screen, watcher_x, watcher_y, BIRD_B, BIRD_B_WING,
        scale=1.0,
        tilt=0.0,
        wing=wing_watcher,
        blush=0.6 * blush,
        facing=-1,
        head_bob=head_bob,
        head_tilt=head_tilt,
        cap=True,
        cap_backwards=True
    )

    # ----------------------------
    # Corazones (click)
    # ----------------------------
    new_hearts = []
    for h in hearts:
        h["age"] += dt
        if h["age"] >= h["life"]:
            continue

        h["x"] += h["vx"] * dt
        h["y"] -= h["vy"] * dt
        h["x"] += 12 * math.sin(2.5 * (t + h["phase"])) * dt

        uu = h["age"] / h["life"]
        alpha = int(220 * (1 - uu))

        draw_heart(screen, h["x"], h["y"], size=12, alpha=max(0, alpha))
        new_hearts.append(h)

    hearts = new_hearts

    # ----------------------------
    # UI / salida
    # ----------------------------
    font = pygame.font.SysFont(None, 26)
    msg = "La primavera empieza el 20 de marzo"
    screen.blit(font.render(msg, True, (60, 60, 60)), (18, 18))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    pygame.display.flip()


pygame.quit()
sys.exit()