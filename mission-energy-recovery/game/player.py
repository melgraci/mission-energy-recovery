"""Estado e movimento do drone (lógica pura, sem OpenGL)."""
import math

import config


class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x, self.z = config.DRONE_START
        self.vx = 0.0
        self.vz = 0.0
        self.yaw = 0.0   # graus; 0 = olhando para -Z (para o fundo da cena)

    def update(self, dt, forward, back, left, right):
        """Move o drone com velocidade suavizada. W = -Z, S = +Z, A = -X, D = +X."""
        dx = (1 if right else 0) - (1 if left else 0)
        dz = (1 if back else 0) - (1 if forward else 0)
        comprimento = math.hypot(dx, dz)
        if comprimento > 0:               # normaliza para a diagonal não ser mais rápida
            dx /= comprimento
            dz /= comprimento
        k = min(1.0, config.DRONE_RESPONSE * dt)
        self.vx += (dx * config.DRONE_SPEED - self.vx) * k
        self.vz += (dz * config.DRONE_SPEED - self.vz) * k
        self.x += self.vx * dt
        self.z += self.vz * dt

        if math.hypot(self.vx, self.vz) > 0.4:   # vira o drone na direção do movimento
            alvo = math.degrees(math.atan2(-self.vx, -self.vz))
            diferenca = (alvo - self.yaw + 180.0) % 360.0 - 180.0
            self.yaw += diferenca * min(1.0, 10.0 * dt)

    def clamp_to_platform(self):
        """Impede o drone de sair da plataforma."""
        limite = config.PLATFORM_HALF - config.DRONE_RADIUS
        if abs(self.x) > limite:
            self.x = math.copysign(limite, self.x)
            self.vx = 0.0
        if abs(self.z) > limite:
            self.z = math.copysign(limite, self.z)
            self.vz = 0.0
