"""Drone de manutenção modelado em partes independentes com transformações hierárquicas."""
import math

from OpenGL.GL import *

import config
from graphics import lighting
from graphics import primitives as prim


class DroneRenderer:
    def __init__(self):
        self.prop_angle = 0.0   # ângulo atual das hélices (graus)

    def update(self, dt):
        """Rotação contínua das hélices: ângulo += velocidade * dt."""
        self.prop_angle = (self.prop_angle + config.PROPELLER_SPEED * dt) % 360.0

    def draw(self, player, t):
        x, z = player.x, player.z
        y = config.DRONE_HEIGHT + 0.08 * math.sin(t * 3.0)   # flutuação leve
        self._draw_shadow(x, z, y)

        # inclinação para o lado do movimento (efeito de inércia)
        roll = -player.vx * 2.2
        pitch = player.vz * 2.2

        glPushMatrix()
        glTranslatef(x, y, z)             # TRANSLAÇÃO: posição do drone no mundo
        glRotatef(roll, 0, 0, 1)          # ROTAÇÃO: inclinação lateral
        glRotatef(pitch, 1, 0, 0)         # ROTAÇÃO: inclinação frontal
        glRotatef(player.yaw, 0, 1, 0)    # ROTAÇÃO: direção do drone

        self._draw_body(t)
        self._draw_visor()
        self._draw_arms_and_props()
        self._draw_antenna(t)
        glPopMatrix()

        self._draw_prop_blur(x, y, z, player)

    # ---------------------------------------------------------------- partes
    def _draw_shadow(self, x, z, y):
        """Sombra falsa: disco escuro translúcido no chão (ajuda a perceber a altura)."""
        lighting.emissive_begin()
        glDepthMask(GL_FALSE)
        glColor4f(0.12, 0.02, 0.25, 0.38)
        glPushMatrix()
        glTranslatef(x, 0.04, z)
        glScalef(1.0 - (y - 1.0) * 0.2, 1.0, 1.0 - (y - 1.0) * 0.2)   # ESCALA
        prim.draw_disc(0.85, 32)
        glPopMatrix()
        glDepthMask(GL_TRUE)
        lighting.emissive_end()

    def _draw_body(self, t):
        # corpo principal: esfera achatada (escala não uniforme)
        lighting.material(config.PEARL, specular=0.9, shininess=90)
        glPushMatrix()
        glScalef(1.0, 0.5, 1.0)
        prim.draw_sphere(0.55, 28, 18)
        glPopMatrix()
        # anel metálico central
        lighting.material(config.METAL_GRAY, specular=0.8, shininess=60)
        glPushMatrix()
        glScalef(1.0, 0.18, 1.0)
        prim.draw_cylinder(0.62, 0.5, 28, True, 1.0)
        glPopMatrix()
        # calota inferior em cone (triângulos), com a ponta para baixo
        lighting.material(config.LILAC, specular=0.7, shininess=50)
        glPushMatrix()
        glTranslatef(0, -0.12, 0)
        glRotatef(180, 1, 0, 0)
        prim.draw_cone(0.32, 0.25, 20)
        glPopMatrix()
        # luzes decorativas rosas ao redor do corpo (esferas pequenas pulsantes)
        brilho = 0.7 + 0.3 * math.sin(t * 5.0)
        lighting.material(config.PINK, specular=0.3, emission=(brilho, 0.1 * brilho, 0.4 * brilho))
        for ang in (0, 90, 180, 270):
            glPushMatrix()
            glRotatef(ang, 0, 1, 0)
            glTranslatef(0.5, 0.0, 0.0)
            prim.draw_sphere(0.05, 10, 8)
            glPopMatrix()

    def _draw_visor(self):
        """Cabine/visor na frente do drone (-Z local)."""
        lighting.material((0.55, 0.85, 1.0), specular=1.0, shininess=110, emission=(0.18, 0.30, 0.45))
        glPushMatrix()
        glTranslatef(0.0, 0.06, -0.38)
        glScalef(0.42, 0.24, 0.26)
        prim.draw_sphere(1.0, 20, 14)
        glPopMatrix()

    def _draw_arms_and_props(self):
        """Quatro braços em X. Cada braço é um sub-objeto: braço -> motor -> hélice."""
        for i, ang in enumerate((45, 135, 225, 315)):
            glPushMatrix()
            glRotatef(ang, 0, 1, 0)                       # gira o braço em torno do corpo
            # braço (caixa)
            lighting.material(config.METAL_GRAY, specular=0.7, shininess=50)
            glPushMatrix()
            glTranslatef(0.62, 0.0, 0.0)
            prim.draw_box(0.85, 0.08, 0.13)
            glPopMatrix()
            # motor (cilindro) na ponta do braço
            glTranslatef(1.05, 0.06, 0.0)
            lighting.material(config.GALAXY_PURPLE, specular=0.8, shininess=70)
            prim.draw_cylinder(0.11, 0.2, 16, True, 1.0)
            # hélice: transformação HIERÁRQUICA — herda o braço e gira sozinha
            glTranslatef(0.0, 0.13, 0.0)
            glRotatef(self.prop_angle * (1 if i % 2 == 0 else -1), 0, 1, 0)
            lighting.material(config.LIGHT_PINK, specular=0.6, shininess=40)
            prim.draw_propeller(0.42, 0.1)
            glPopMatrix()

    def _draw_antenna(self, t):
        lighting.material(config.METAL_GRAY, specular=0.8)
        glPushMatrix()
        glTranslatef(0.0, 0.2, 0.2)
        prim.draw_cone(0.03, 0.3, 10)
        glTranslatef(0.0, 0.3, 0.0)
        piscar = 0.5 + 0.5 * math.sin(t * 6.0)
        lighting.material(config.PINK, emission=(piscar, 0.1 * piscar, 0.3 * piscar))
        prim.draw_sphere(0.045, 10, 8)
        glPopMatrix()

    def _draw_prop_blur(self, x, y, z, player):
        """Discos translúcidos sobre as hélices (efeito de rotação rápida)."""
        lighting.emissive_begin()
        glDepthMask(GL_FALSE)
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(-player.vx * 2.2, 0, 0, 1)
        glRotatef(player.vz * 2.2, 1, 0, 0)
        glRotatef(player.yaw, 0, 1, 0)
        glColor4f(1.0, 0.75, 0.92, 0.22)
        for ang in (45, 135, 225, 315):
            glPushMatrix()
            glRotatef(ang, 0, 1, 0)
            glTranslatef(1.05, 0.19, 0.0)
            prim.draw_disc(0.42, 24)
            glPopMatrix()
        glPopMatrix()
        glDepthMask(GL_TRUE)
        lighting.emissive_end()
