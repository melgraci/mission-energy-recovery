"""Os três obstáculos físicos da estação."""
from game import collisions


class Obstacle:
    """Obstáculo estático. kind: 'container' (caixa), 'tank' (cilindro) ou 'tower' (cone)."""

    def __init__(self, kind, x, z, radius=1.0, half_x=1.0, half_z=1.0, height=2.0):
        self.kind = kind
        self.x = x
        self.z = z
        self.radius = radius
        self.half_x = half_x
        self.half_z = half_z
        self.height = height

    def resolve(self, px, pz, pr):
        """Retorna a posição corrigida do jogador se houver colisão; senão None."""
        if self.kind == "container":
            return collisions.circle_vs_aabb(px, pz, pr, self.x, self.z, self.half_x, self.half_z)
        return collisions.circle_vs_circle(px, pz, pr, self.x, self.z, self.radius)


def create_obstacles():
    return [
        Obstacle("container", -3.5, -2.5, half_x=1.1, half_z=1.1, height=1.8),
        Obstacle("tank", 4.0, 0.5, radius=1.1, height=2.2),
        Obstacle("tower", -2.0, 3.5, radius=1.0, height=2.8),
    ]
