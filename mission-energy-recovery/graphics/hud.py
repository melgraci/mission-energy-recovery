"""Interface 2D (HUD) desenhada com Pygame (texto) sobre o OpenGL (projeção ortográfica)."""
import math

import pygame
from OpenGL.GL import *

import config
from graphics import lighting


class TextRenderer:
    """Renderiza texto com pygame.font, converte para textura OpenGL e guarda em cache."""

    def __init__(self):
        self.fonts = {}
        self.cache = {}

    def _font(self, size, bold):
        chave = (size, bold)
        if chave not in self.fonts:
            self.fonts[chave] = pygame.font.SysFont("segoeui,arial,calibri,dejavusans", size, bold=bold)
        return self.fonts[chave]

    def _texture(self, text, size, color, bold):
        chave = (text, size, color, bold)
        if chave in self.cache:
            return self.cache[chave]
        if len(self.cache) > 300:                         # evita crescer sem limite
            glDeleteTextures([t[0] for t in self.cache.values()])
            self.cache.clear()
        superficie = self._font(size, bold).render(text, True, color)
        largura, altura = superficie.get_size()
        dados = pygame.image.tostring(superficie, "RGBA", False)
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0, GL_RGBA, GL_UNSIGNED_BYTE, dados)
        self.cache[chave] = (tex, largura, altura)
        return self.cache[chave]

    def draw(self, text, x, y, size=18, color=(255, 255, 255), bold=False, align="left", alpha=1.0):
        """Desenha o texto em (x, y) da tela. align: left, center ou right. Retorna a largura."""
        tex, w, h = self._texture(text, size, color, bold)
        if align == "center":
            x -= w / 2
        elif align == "right":
            x -= w
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex)
        glColor4f(1, 1, 1, alpha)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x, y)
        glTexCoord2f(1, 0); glVertex2f(x + w, y)
        glTexCoord2f(1, 1); glVertex2f(x + w, y + h)
        glTexCoord2f(0, 1); glVertex2f(x, y + h)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
        return w


def _rect(x, y, w, h, color, alpha):
    glColor4f(color[0], color[1], color[2], alpha)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()


def _rect_outline(x, y, w, h, color, alpha, width=2.0):
    glLineWidth(width)
    glColor4f(color[0], color[1], color[2], alpha)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()


class Hud:
    def __init__(self):
        self.text = TextRenderer()

    def draw(self, mission, width, height, fps):
        # projeção ortográfica 2D com origem no canto superior esquerdo
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, width, height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        self._top_left(mission)
        self._top_right(mission, width, fps)
        self._bottom(mission, width, height)
        if mission.message_timer > 0 and not mission.won:
            self._message(mission, width, height)
        if mission.won:
            self._victory(mission, width, height)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        lighting.emissive_end()

    def _top_left(self, m):
        _rect(16, 16, 520, 118, config.GALAXY_PURPLE, 0.72)
        _rect_outline(16, 16, 520, 118, config.PINK, 0.9)
        self.text.draw("PINK GALAXY: ENERGY RECOVERY", 30, 24, 26, (255, 150, 215), True)
        self.text.draw("Energia: %d/%d" % (m.collected, m.total), 30, 62, 24, (255, 255, 255), True)
        for i in range(m.total):                      # barra de 5 segmentos
            cor = config.PINK if i < m.collected else (0.35, 0.25, 0.5)
            _rect(215 + i * 52, 66, 44, 18, cor, 1.0)
            _rect_outline(215 + i * 52, 66, 44, 18, config.LIGHT_PINK, 0.8, 1.0)
        objetivo = "Objetivo: colete as células de energia" if not m.all_collected \
            else "Portal aberto! Vá até o portal rosa!"
        self.text.draw(objetivo, 30, 100, 18, (235, 215, 255))

    def _top_right(self, m, width, fps):
        _rect(width - 286, 16, 270, 82, config.GALAXY_PURPLE, 0.72)
        _rect_outline(width - 286, 16, 270, 82, config.LILAC, 0.9)
        luz = "LIGADA" if lighting.is_enabled() else "DESLIGADA"
        self.text.draw("Iluminação [L]: %s" % luz, width - 276, 24, 18, (255, 255, 255), True)
        self.text.draw("Colisões: %d" % m.hits, width - 276, 50, 17, (235, 215, 255))
        self.text.draw("FPS: %d" % fps, width - 276, 72, 15, (200, 180, 230))

    def _bottom(self, m, width, height):
        _rect(16, height - 64, 640, 48, config.GALAXY_PURPLE, 0.72)
        _rect_outline(16, height - 64, 640, 48, config.PINK, 0.9)
        self.text.draw("W/A/S/D: mover   |   L: luz   |   R: reiniciar   |   ESC: sair",
                       30, height - 52, 19, (255, 235, 250))

    def _message(self, m, width, height):
        alpha = min(1.0, m.message_timer / 0.5)
        tex_w = self.text._texture(m.message, 26, (255, 255, 255), True)[1]
        _rect(width / 2 - tex_w / 2 - 22, 150, tex_w + 44, 48, config.GALAXY_PURPLE, 0.75 * alpha)
        _rect_outline(width / 2 - tex_w / 2 - 22, 150, tex_w + 44, 48, config.PINK, alpha)
        self.text.draw(m.message, width / 2, 158, 26, (255, 255, 255), True, "center", alpha)

    def _victory(self, m, width, height):
        alpha = min(1.0, m.win_timer / 0.6)
        _rect(0, 0, width, height, (0.20, 0.08, 0.35), 0.55 * alpha)
        cx, cy = width / 2, height / 2
        _rect(cx - 400, cy - 130, 800, 260, config.GALAXY_PURPLE, 0.9 * alpha)
        _rect_outline(cx - 400, cy - 130, 800, 260, config.PINK, alpha, 3.0)
        pulso = 0.85 + 0.15 * math.sin(m.win_timer * 4.0)
        self.text.draw("MISSÃO CONCLUÍDA!", cx, cy - 105, 52, (255, int(130 * pulso + 40), 215), True, "center", alpha)
        self.text.draw("VITÓRIA! A energia da estação foi restaurada.", cx, cy - 30, 28, (255, 255, 255),
                       True, "center", alpha)
        self.text.draw("Células coletadas: %d/%d   |   Colisões: %d" % (m.collected, m.total, m.hits),
                       cx, cy + 20, 22, (235, 215, 255), False, "center", alpha)
        self.text.draw("Pressione R para reiniciar a partida", cx, cy + 70, 26, (255, 190, 235), True,
                       "center", alpha)
