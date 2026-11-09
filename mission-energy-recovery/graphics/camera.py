"""Câmera em perspectiva que acompanha o drone suavemente."""
import math

from OpenGL.GL import *
from OpenGL.GLU import *

import config


class Camera:
    def __init__(self):
        self.x = 0.0
        self.z = 0.0
        self.snap(*config.DRONE_START)

    def snap(self, tx, tz):
        """Posiciona a câmera imediatamente (usado ao iniciar/reiniciar)."""
        self.x = tx * 0.5
        self.z = tz * 0.7

    def update(self, dt, tx, tz):
        """Segue o alvo com suavização exponencial independente do FPS."""
        k = 1.0 - math.exp(-4.0 * dt)
        self.x += (tx * 0.5 - self.x) * k
        self.z += (tz * 0.7 - self.z) * k

    def apply(self, width, height):
        """Define a projeção em perspectiva e a visão (gluLookAt)."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(config.FOV, width / float(height), config.NEAR_PLANE, config.FAR_PLANE)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.x, 8.5, self.z + 11.0,       # posição do olho
                  self.x, 0.5, self.z - 1.0,        # ponto observado
                  0.0, 1.0, 0.0)                    # vetor "para cima"
