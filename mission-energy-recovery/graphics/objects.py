"""Desenho dos objetos do jogo: obstáculos, cristais e portal."""
import math

from OpenGL.GL import *

import config
from graphics import lighting
from graphics import primitives as prim
from graphics import textures


# ------------------------------------------------------------------ Obstáculos
def draw_obstacles(obstacles, tex, t):
    for o in obstacles:
        glPushMatrix()
        glTranslatef(o.x, 0.0, o.z)
        if o.kind == "container":
            _draw_container(o, tex, t)
        elif o.kind == "tank":
            _draw_tank(o, t)
        else:
            _draw_tower(o, t)
        glPopMatrix()


def _neon_ring(radius, y, t):
    """Anel de linhas neon (sem iluminação) ao redor de um obstáculo."""
    lighting.emissive_begin()
    glDisable(GL_TEXTURE_2D)
    glLineWidth(2.5)
    glColor4f(1.0, 0.3, 0.75, 0.7 + 0.3 * math.sin(t * 3.0))
    glPushMatrix()
    glTranslatef(0, y, 0)
    prim.draw_line_ring(radius, 40)
    glPopMatrix()
    lighting.emissive_end()


def _draw_container(o, tex, t):
    """Contêiner de carga: caixa texturizada com pirâmide decorativa no topo."""
    lighting.material(config.PEARL, specular=0.6, shininess=50)
    tex["tech_wall"].bind()
    glPushMatrix()
    glTranslatef(0, o.height / 2, 0)
    prim.draw_box(o.half_x * 2, o.height, o.half_z * 2, 0.5)
    glPopMatrix()
    textures.unbind()
    lighting.material(config.PINK, specular=0.8, shininess=80, emission=(0.5, 0.08, 0.25))
    glPushMatrix()
    glTranslatef(0, o.height, 0)
    prim.draw_pyramid(0.45, 0.6)
    glPopMatrix()
    # faixa neon em volta da caixa
    lighting.emissive_begin()
    glLineWidth(2.5)
    glColor4f(1.0, 0.3, 0.75, 0.9)
    glPushMatrix()
    glTranslatef(0, o.height * 0.55, 0)
    glBegin(GL_LINE_LOOP)
    h = 0.01
    for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        glVertex3f(sx * (o.half_x + h), 0, sz * (o.half_z + h))
    glEnd()
    glPopMatrix()
    lighting.emissive_end()


def _draw_tank(o, t):
    """Tanque de energia: cilindro metálico com anéis rosa."""
    lighting.material(config.LILAC, specular=0.9, shininess=100)
    glPushMatrix()
    glTranslatef(0, o.height / 2, 0)
    prim.draw_cylinder(o.radius, o.height, 28, True, 1.0)
    glPopMatrix()
    lighting.material(config.PINK, specular=0.6, emission=(0.6, 0.1, 0.3))
    for frac in (0.3, 0.7):
        glPushMatrix()
        glTranslatef(0, o.height * frac, 0)
        glRotatef(90, 1, 0, 0)
        prim.draw_torus(o.radius + 0.02, 0.05, 32, 8)
        glPopMatrix()
    lighting.material(config.GALAXY_PURPLE, specular=0.8)
    glPushMatrix()
    glTranslatef(0, o.height, 0)
    prim.draw_cone(o.radius * 0.8, 0.35, 28)
    glPopMatrix()


def _draw_tower(o, t):
    """Torre de reator em forma de cone com esfera de energia no topo."""
    lighting.material(config.LIGHT_PINK, specular=0.8, shininess=70)
    prim.draw_cone(o.radius, o.height - 0.4, 28)
    lighting.material(config.METAL_GRAY, specular=0.8)
    glPushMatrix()
    glTranslatef(0, 0.1, 0)
    prim.draw_cylinder(o.radius * 1.2, 0.2, 28, True, 1.0)
    glPopMatrix()
    pulso = 0.6 + 0.4 * math.sin(t * 3.0)
    lighting.material(config.PINK, specular=1.0, shininess=100, emission=(pulso, 0.1 * pulso, 0.4 * pulso))
    glPushMatrix()
    glTranslatef(0, o.height - 0.25, 0)
    prim.draw_sphere(0.22, 16, 12)
    glPopMatrix()


# ------------------------------------------------------------------ Cristais de energia
def draw_crystals(crystals, t):
    """Desenha cristais com flutuação, pulso e animação de coleta."""
    for c in crystals:
        if not c.visible:
            continue
        p = c.progress
        # MOVIMENTO PERIÓDICO: flutua com seno e pulsa a escala (usa o tempo t acumulado de dt)
        altura = 1.15 + 0.22 * math.sin(t * 2.0 + c.phase)
        escala = 1.0 + 0.08 * math.sin(t * 4.0 + c.phase)
        giro = t * 70.0 + c.phase * 30.0
        if c.collected:
            # ANIMAÇÃO POR EVENTO: ao coletar, o cristal gira rápido, sobe e encolhe até sumir
            altura += p * 1.6
            escala = (1.0 - p) * 1.4
            giro += p * 720.0
        _draw_crystal_glow(c, t, p)
        glPushMatrix()
        glTranslatef(c.x, altura, c.z)
        glRotatef(giro, 0, 1, 0)
        glScalef(escala, escala, escala)
        brilho = 0.55 + 0.25 * math.sin(t * 3.0 + c.phase)
        lighting.material(config.PINK, specular=1.0, shininess=110, emission=(brilho, 0.08, 0.35 * brilho))
        prim.draw_crystal(0.3, 0.55, 6, 0.6)
        glPopMatrix()
        # anel de linhas orbitando o cristal
        lighting.emissive_begin()
        glLineWidth(2.0)
        glColor4f(1.0, 0.8, 0.95, 0.8 * (1.0 - p))
        glPushMatrix()
        glTranslatef(c.x, altura, c.z)
        glRotatef(-giro * 1.5, 0, 1, 0)
        glRotatef(70, 1, 0, 0)
        glScalef(escala + p * 1.5, escala + p * 1.5, escala + p * 1.5)
        prim.draw_line_ring(0.5, 36)
        glPopMatrix()
        lighting.emissive_end()


def _draw_crystal_glow(c, t, p):
    """Halo rosa translúcido no chão, embaixo do cristal."""
    lighting.emissive_begin()
    glDepthMask(GL_FALSE)
    alpha = (0.28 + 0.12 * math.sin(t * 3.0 + c.phase)) * (1.0 - p)
    glColor4f(1.0, 0.3, 0.75, alpha)
    glPushMatrix()
    glTranslatef(c.x, 0.035, c.z)
    prim.draw_disc(0.75, 28)
    glPopMatrix()
    glDepthMask(GL_TRUE)
    lighting.emissive_end()


# ------------------------------------------------------------------ Portal
def draw_portal_frame(open_progress, t):
    """Estrutura do portal (parte opaca): base, colunas e anel."""
    px, pz = config.PORTAL_POS
    glPushMatrix()
    glTranslatef(px, 0.0, pz)
    lighting.material(config.METAL_GRAY, specular=0.8, shininess=70)
    glPushMatrix()
    glTranslatef(0, 0.12, 0)
    prim.draw_cylinder(3.0, 0.24, 40, True, 1.0)
    glPopMatrix()
    for sx in (-2.15, 2.15):
        lighting.material(config.PEARL, specular=0.9, shininess=90)
        glPushMatrix()
        glTranslatef(sx, 2.0, 0)
        prim.draw_cylinder(0.25, 3.5, 20, True, 1.0)
        glPopMatrix()
        lighting.material(config.PINK, specular=1.0, emission=(0.5 + 0.5 * open_progress, 0.08, 0.35))
        glPushMatrix()
        glTranslatef(sx, 3.85, 0)
        prim.draw_cone(0.3, 0.55, 16)
        glPopMatrix()
    # anel principal: o brilho neon cresce conforme o portal abre
    e = 0.25 + 0.75 * open_progress
    lighting.material(config.PINK, specular=1.0, shininess=100, emission=(e, 0.10 * e, 0.45 * e))
    glPushMatrix()
    glTranslatef(0, 2.2, 0)
    prim.draw_torus(2.1, 0.17, 48, 14)
    glPopMatrix()
    glPopMatrix()


def draw_portal_energy(open_progress, t):
    """Campo de energia translúcido do portal (desenhado por último, com blending)."""
    px, pz = config.PORTAL_POS
    lighting.emissive_begin()
    glDepthMask(GL_FALSE)
    glPushMatrix()
    glTranslatef(px, 2.2, pz)
    # ANIMAÇÃO POR EVENTO: o campo cresce de uma fresta (fechado) até o tamanho total (aberto)
    escala = 0.12 + 0.88 * open_progress
    glScalef(escala, escala, 1.0)
    brilho = 0.35 + 0.65 * open_progress
    pulso = 0.9 + 0.1 * math.sin(t * 4.0)
    raio = 1.95
    glBegin(GL_TRIANGLE_FAN)
    glColor4f(1.0, 0.85, 0.95, 0.65 * brilho)
    glVertex3f(0, 0, 0)
    glColor4f(1.0, 0.25, 0.7, 0.30 * brilho * pulso)
    for i in range(49):
        a = 2 * math.pi * i / 48
        glVertex3f(raio * math.cos(a), raio * math.sin(a), 0)
    glEnd()
    # espiral de linhas girando
    glLineWidth(2.0)
    glRotatef(t * 60.0, 0, 0, 1)
    glColor4f(1.0, 0.9, 1.0, 0.7 * brilho)
    glBegin(GL_LINES)
    for k in range(8):
        a = 2 * math.pi * k / 8
        glVertex3f(0.15 * math.cos(a), 0.15 * math.sin(a), 0.01)
        glVertex3f(raio * 0.9 * math.cos(a + 0.9), raio * 0.9 * math.sin(a + 0.9), 0.01)
    glEnd()
    glPopMatrix()
    glDepthMask(GL_TRUE)
    lighting.emissive_end()
