"""Funções de colisão no plano XZ (círculo x círculo e círculo x retângulo)."""
import math


def distance_xz(ax, az, bx, bz):
    return math.hypot(ax - bx, az - bz)


def circle_vs_circle(px, pz, pr, cx, cz, cr):
    """Retorna a nova posição (x, z) do círculo P empurrado para fora, ou None se não colide."""
    dx, dz = px - cx, pz - cz
    dist = math.hypot(dx, dz)
    minimo = pr + cr
    if dist >= minimo:
        return None
    if dist < 1e-6:
        dx, dz, dist = 0.0, 1.0, 1.0
    return cx + dx / dist * minimo, cz + dz / dist * minimo


def circle_vs_aabb(px, pz, pr, cx, cz, hx, hz):
    """Círculo P contra retângulo alinhado aos eixos (centro c, meias-medidas hx/hz)."""
    mais_x = max(cx - hx, min(px, cx + hx))     # ponto do retângulo mais próximo do círculo
    mais_z = max(cz - hz, min(pz, cz + hz))
    dx, dz = px - mais_x, pz - mais_z
    dist = math.hypot(dx, dz)
    if dist >= pr:
        return None
    if dist > 1e-6:
        return mais_x + dx / dist * pr, mais_z + dz / dist * pr
    # centro do círculo dentro do retângulo: empurra pela face mais próxima
    saidas = [(px - (cx - hx), "xn"), ((cx + hx) - px, "xp"), (pz - (cz - hz), "zn"), ((cz + hz) - pz, "zp")]
    _, lado = min(saidas)
    if lado == "xn":
        return cx - hx - pr, pz
    if lado == "xp":
        return cx + hx + pr, pz
    if lado == "zn":
        return px, cz - hz - pr
    return px, cz + hz + pr


def resolve_player_vs_obstacles(player, obstacles, radius):
    """Empurra o jogador para fora de qualquer obstáculo. Retorna True se houve colisão."""
    colidiu = False
    for obstaculo in obstacles:
        novo = obstaculo.resolve(player.x, player.z, radius)
        if novo is not None:
            player.x, player.z = novo
            colidiu = True
    return colidiu
