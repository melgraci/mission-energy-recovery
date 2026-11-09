"""Células de energia coletáveis."""
import math

import config
from game.collisions import distance_xz


class Crystal:
    def __init__(self, x, z, phase):
        self.x = x
        self.z = z
        self.phase = phase          # defasagem da flutuação (cada cristal flutua diferente)
        self.collected = False
        self.collect_timer = 0.0    # tempo desde a coleta (usado na animação de sumiço)

    @property
    def progress(self):
        """0 = inteiro; 1 = animação de coleta terminada."""
        return min(1.0, self.collect_timer / config.CRYSTAL_COLLECT_TIME)

    @property
    def visible(self):
        return not self.collected or self.progress < 1.0

    def update(self, dt):
        if self.collected:
            self.collect_timer += dt

    def can_collect(self, px, pz):
        return (not self.collected) and distance_xz(px, pz, self.x, self.z) <= config.CRYSTAL_PICKUP_RADIUS


def create_crystals():
    posicoes = [(-6.0, 5.0), (6.0, 5.5), (6.5, -4.5), (-6.5, -5.5), (0.0, -3.0)]
    return [Crystal(x, z, i * 1.3) for i, (x, z) in enumerate(posicoes)]
