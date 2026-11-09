"""Cenário: fundo galáctico, plataforma, paredes, pilares e elementos decorativos."""
import math
import random

from OpenGL.GL import *

import config
from graphics import lighting
from graphics import primitives as prim
from graphics import textures

H = config.PLATFORM_HALF
T = config.PLATFORM_THICKNESS


class Environment:
    def __init__(self, tex):
        self.tex = tex
        rng = random.Random(5)
        self.stars = []
        for _ in range(450):
            azimute = rng.uniform(0, 2 * math.pi)
            elevacao = rng.uniform(-0.35, 1.4)
            r = 140.0
            self.stars.append((r * math.cos(elevacao) * math.cos(azimute),
                               r * math.sin(elevacao) + 10.0,
                               r * math.cos(elevacao) * math.sin(azimute) - 30.0,
                               rng.uniform(0, 6.28), rng.choice((1.5, 2.0, 2.5, 3.0))))

    # ------------------------------------------------------------ fundo
    def draw_background(self, t):
        """Gradiente roxo galáctico em tela cheia + estrelas piscando."""
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glBegin(GL_QUADS)
        glColor3f(*config.BACKGROUND_BOTTOM)
        glVertex2f(-1, -1)
        glVertex2f(1, -1)
        glColor3f(*config.BACKGROUND_TOP)
        glVertex2f(1, 1)
        glVertex2f(-1, 1)
        glEnd()
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

    def draw_stars(self, t):
        """Estrelas distantes (GL_POINTS). Deve ser chamado depois da câmera."""
        glDisable(GL_LIGHTING)
        glDepthMask(GL_FALSE)
        for tamanho in (1.5, 2.0, 2.5, 3.0):
            glPointSize(tamanho)
            glBegin(GL_POINTS)
            for x, y, z, fase, s in self.stars:
                if s == tamanho:
                    b = 0.65 + 0.35 * math.sin(t * 2.0 + fase)
                    glColor4f(1.0, 0.9 + 0.1 * b, 1.0, b)
                    glVertex3f(x, y, z)
            glEnd()
        glDepthMask(GL_TRUE)
        lighting.emissive_end()

    # ------------------------------------------------------------ mundo
    def draw_world(self, t, portal_open):
        self.draw_stars(t)
        self._draw_far_decor(t)
        self._draw_platform()
        self._draw_walls()
        self._draw_pillars(t)
        self._draw_floating_decor(t)
        self._draw_glow_lines(t, portal_open)

    def _draw_platform(self):
        # topo: plano subdividido com textura metálica REPETIDA (GL_REPEAT)
        lighting.material((0.95, 0.9, 1.0), specular=0.85, shininess=70)
        self.tex["metal"].bind()
        prim.draw_grid_plane(H, 20, 0.5, 0.0)
        # lateral da plataforma
        glPushMatrix()
        glTranslatef(0, -T / 2 - 0.01, 0)
        prim.draw_box(2 * H, T, 2 * H, 0.5)
        glPopMatrix()
        textures.unbind()
        # casco inferior: pirâmide invertida (triângulos)
        lighting.material(config.GALAXY_PURPLE, specular=0.6, shininess=40)
        glPushMatrix()
        glTranslatef(0, -T - 3.5, 0)
        prim.draw_pyramid(H * 0.98, 3.5)
        glPopMatrix()

    def _draw_walls(self):
        lighting.material((0.88, 0.82, 1.0), specular=0.5, shininess=40)
        self.tex["tech_wall"].bind()
        # parede dos fundos (alta)
        glPushMatrix()
        glTranslatef(0, 2.25, -H - 0.3)
        prim.draw_box(2 * H + 1.2, 4.5, 0.6, 0.4)
        glPopMatrix()
        # paredes laterais e frontal (baixas, para não bloquear a câmera)
        for sx in (-1, 1):
            glPushMatrix()
            glTranslatef(sx * (H + 0.3), 0.75, 0)
            prim.draw_box(0.6, 1.5, 2 * H, 0.4)
            glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 0.35, H + 0.3)
        prim.draw_box(2 * H + 1.2, 0.7, 0.6, 0.4)
        glPopMatrix()
        textures.unbind()

    def _draw_pillars(self, t):
        for sx in (-1, 1):
            for sz in (-1, 1):
                glPushMatrix()
                glTranslatef(sx * (H + 0.3), 0, sz * (H + 0.3))
                lighting.material(config.PEARL, specular=0.9, shininess=90)
                glPushMatrix()
                glTranslatef(0, 1.6, 0)
                prim.draw_cylinder(0.45, 3.2, 20, True, 1.0)
                glPopMatrix()
                lighting.material(config.PINK, specular=0.9, emission=(0.45, 0.07, 0.25))
                glPushMatrix()
                glTranslatef(0, 2.0, 0)
                glRotatef(90, 1, 0, 0)
                prim.draw_torus(0.47, 0.06, 24, 8)
                glPopMatrix()
                lighting.material(config.LILAC, specular=0.9, shininess=90)
                glPushMatrix()
                glTranslatef(0, 3.2, 0)
                prim.draw_cone(0.45, 0.6, 20)
                glPopMatrix()
                b = 0.6 + 0.4 * math.sin(t * 3.0 + sx + 2 * sz)
                lighting.material(config.PINK, emission=(b, 0.1 * b, 0.4 * b))
                glPushMatrix()
                glTranslatef(0, 3.95, 0)
                prim.draw_sphere(0.12, 12, 10)
                glPopMatrix()
                glPopMatrix()

    def _draw_floating_decor(self, t):
        """Satélites cristalinos girando e antenas na parede dos fundos."""
        for i, (x, y, z) in enumerate(((-14, 4, -4), (14, 5, -2), (-15, 6, 6), (15, 3.5, 7))):
            glPushMatrix()
            glTranslatef(x, y + 0.5 * math.sin(t * 1.2 + i), z)
            glRotatef(t * 25.0 + i * 40, 0, 1, 0)
            glRotatef(20, 1, 0, 0)
            lighting.material(config.LILAC, specular=1.0, shininess=100, emission=(0.12, 0.08, 0.25))
            prim.draw_crystal(0.7, 1.3, 6, 0.8)
            glPopMatrix()
        for sx in (-7.5, 7.5):
            glPushMatrix()
            glTranslatef(sx, 4.5, -H - 0.3)
            lighting.material(config.METAL_GRAY, specular=0.8)
            glPushMatrix()
            glTranslatef(0, 0.9, 0)
            prim.draw_cylinder(0.06, 1.8, 10, True, 1.0)
            glPopMatrix()
            b = 0.5 + 0.5 * math.sin(t * 5.0 + sx)
            lighting.material(config.PINK, emission=(b, 0.1 * b, 0.4 * b))
            glTranslatef(0, 1.9, 0)
            prim.draw_sphere(0.1, 10, 8)
            glPopMatrix()

    def _draw_far_decor(self, t):
        """Planeta rosa-lilás com anel e uma lua ao fundo."""
        glPushMatrix()
        glTranslatef(-28, 13, -55)
        lighting.material((0.95, 0.55, 0.85), specular=0.4, shininess=30)
        prim.draw_sphere(10.0, 40, 28)
        glRotatef(70, 1, 0, 0)
        glRotatef(t * 4.0, 0, 0, 1)
        lighting.material(config.LILAC, specular=0.4, shininess=30)
        glScalef(1.0, 1.0, 0.05)
        prim.draw_torus(15.0, 1.6, 60, 12)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(32, 9, -45)
        lighting.material(config.LILAC, specular=0.5, shininess=40)
        prim.draw_sphere(3.5, 28, 20)
        glPopMatrix()

    # ------------------------------------------------------------ linhas neon
    def _draw_glow_lines(self, t, portal_open):
        """Linhas luminosas rosas e lilases (sem iluminação, com pulso)."""
        lighting.emissive_begin()
        pulso = 0.65 + 0.35 * math.sin(t * 2.0)
        glLineWidth(2.5)
        # contorno rosa da plataforma
        glColor4f(1.0, 0.3, 0.75, pulso)
        b = H - 0.4
        glBegin(GL_LINE_LOOP)
        for x, z in ((-b, -b), (b, -b), (b, b), (-b, b)):
            glVertex3f(x, 0.03, z)
        glEnd()
        # grade lilás
        glLineWidth(1.0)
        glColor4f(0.78, 0.62, 1.0, 0.35)
        glBegin(GL_LINES)
        for v in range(-8, 9, 4):
            glVertex3f(v, 0.03, -b)
            glVertex3f(v, 0.03, b)
            glVertex3f(-b, 0.03, v)
            glVertex3f(b, 0.03, v)
        glEnd()
        # trilha tracejada animada do ponto de partida até o portal
        glLineWidth(3.0)
        glColor4f(1.0, 0.55, 0.85, 0.85)
        glBegin(GL_LINES)
        deslocamento = (t * 1.5) % 1.0
        z = config.DRONE_START[1] - 2.0 - deslocamento
        while z > config.PORTAL_POS[1] + 3.5:
            glVertex3f(0, 0.04, z)
            glVertex3f(0, 0.04, z - 0.5)
            z -= 1.0
        glEnd()
        # anéis no chão: base do portal e ponto de partida
        glLineWidth(2.5)
        glColor4f(1.0, 0.3, 0.75, 0.6 + 0.4 * portal_open)
        glPushMatrix()
        glTranslatef(config.PORTAL_POS[0], 0.27, config.PORTAL_POS[1])
        prim.draw_line_ring(2.7, 48)
        glPopMatrix()
        glColor4f(0.78, 0.62, 1.0, 0.9)
        glPushMatrix()
        glTranslatef(config.DRONE_START[0], 0.03, config.DRONE_START[1])
        prim.draw_line_ring(1.3, 36)
        glPopMatrix()
        # topo das paredes e painéis luminosos da parede dos fundos
        glLineWidth(2.5)
        glColor4f(1.0, 0.3, 0.75, pulso)
        glBegin(GL_LINES)
        glVertex3f(-H - 0.6, 4.51, -H - 0.3)
        glVertex3f(H + 0.6, 4.51, -H - 0.3)
        for sx in (-H - 0.3, H + 0.3):
            glVertex3f(sx, 1.51, -H)
            glVertex3f(sx, 1.51, H)
        glEnd()
        zf = -H + 0.02
        for cx in (-6.5, 6.5):          # janelas translúcidas
            glBegin(GL_QUADS)
            glColor4f(0.75, 0.55, 1.0, 0.45)
            glVertex3f(cx - 2.2, 2.2, zf)
            glVertex3f(cx + 2.2, 2.2, zf)
            glColor4f(1.0, 0.55, 0.9, 0.45)
            glVertex3f(cx + 2.2, 3.7, zf)
            glVertex3f(cx - 2.2, 3.7, zf)
            glEnd()
            glColor4f(1.0, 0.85, 0.95, 0.9)
            glBegin(GL_LINE_LOOP)
            glVertex3f(cx - 2.2, 2.2, zf)
            glVertex3f(cx + 2.2, 2.2, zf)
            glVertex3f(cx + 2.2, 3.7, zf)
            glVertex3f(cx - 2.2, 3.7, zf)
            glEnd()
        glColor4f(1.0, 0.3, 0.75, 0.9)   # faixa rosa luminosa
        glBegin(GL_QUADS)
        glVertex3f(-H, 0.9, zf)
        glVertex3f(H, 0.9, zf)
        glVertex3f(H, 1.05, zf)
        glVertex3f(-H, 1.05, zf)
        glEnd()
        lighting.emissive_end()
