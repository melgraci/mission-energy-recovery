"""Carregamento de texturas com Pillow e envio para o OpenGL."""
import os

from OpenGL.GL import *
from OpenGL.GLU import gluBuild2DMipmaps
from PIL import Image

import config
from graphics.texture_generator import ensure_textures


class Texture:
    """Textura 2D do OpenGL com repetição (GL_REPEAT) e mipmaps."""

    def __init__(self, path, repeat=True):
        imagem = Image.open(path).convert("RGBA")
        imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)  # o OpenGL espera a origem embaixo
        largura, altura = imagem.size
        dados = imagem.tobytes()

        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id)
        modo = GL_REPEAT if repeat else GL_CLAMP_TO_EDGE
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, modo)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, modo)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, largura, altura, GL_RGBA, GL_UNSIGNED_BYTE, dados)
        glBindTexture(GL_TEXTURE_2D, 0)

    def bind(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)  # textura x cor x luz


def unbind():
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)


def load_all():
    """Garante que os PNGs existem e carrega todas as texturas do jogo."""
    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", config.TEXTURE_DIR)
    ensure_textures(pasta)
    return {
        "metal": Texture(os.path.join(pasta, "metal.png")),
        "tech_wall": Texture(os.path.join(pasta, "tech_wall.png")),
    }
