"""Iluminação do OpenGL: luz ambiente, difusa e especular.

- GL_LIGHT0: luz principal branco-lilás, vinda de cima.
- GL_LIGHT1: luz rosa neon posicionada no portal (intensidade cresce quando ele abre).
A tecla L liga/desliga todo o sistema (glEnable/glDisable(GL_LIGHTING)).
"""
from OpenGL.GL import *

import config

_enabled = True


def is_enabled():
    return _enabled


def toggle():
    global _enabled
    _enabled = not _enabled
    return _enabled


def setup():
    """Configuração fixa da iluminação (chamada uma vez)."""
    glEnable(GL_NORMALIZE)                      # renormaliza normais após glScalef
    glShadeModel(GL_SMOOTH)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.36, 0.28, 0.44, 1.0))   # ambiente global
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)                    # luz nos dois lados
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
    glLightModeli(GL_LIGHT_MODEL_COLOR_CONTROL, GL_SEPARATE_SPECULAR_COLOR)  # especular sobre textura
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.28, 0.22, 0.34, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 0.93, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

    glLightfv(GL_LIGHT1, GL_AMBIENT, (0.0, 0.0, 0.0, 1.0))
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.07)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.008)


def apply(portal_open):
    """Posiciona as luzes (após a câmera!) e liga/desliga o sistema conforme a tecla L."""
    if not _enabled:
        glDisable(GL_LIGHTING)
        return
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT0, GL_POSITION, (4.0, 14.0, 8.0, 1.0))
    # luz rosa do portal: fraca fechado, forte aberto
    forca = 0.35 + 1.4 * portal_open
    glLightfv(GL_LIGHT1, GL_POSITION, (config.PORTAL_POS[0], 3.0, config.PORTAL_POS[1] + 1.0, 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (1.0 * forca, 0.22 * forca, 0.62 * forca, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (1.0 * forca, 0.45 * forca, 0.8 * forca, 1.0))


def material(color, specular=0.5, shininess=48.0, emission=(0.0, 0.0, 0.0), alpha=1.0):
    """Define a cor/material do próximo objeto (sempre redefine tudo para não vazar)."""
    glColor4f(color[0], color[1], color[2], alpha)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (specular, specular, specular, 1.0))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, shininess)
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (emission[0], emission[1], emission[2], 1.0))


def emissive_begin():
    """Objetos que brilham (linhas neon, portal) são desenhados sem iluminação."""
    glDisable(GL_LIGHTING)


def emissive_end():
    if _enabled:
        glEnable(GL_LIGHTING)
