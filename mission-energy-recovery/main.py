"""PINK GALAXY: ENERGY RECOVERY — ponto de entrada do jogo.

Execute com:  python main.py
"""
import sys

import pygame
from OpenGL.GL import *

import config
from game.mission import Mission
from graphics import lighting, textures
from graphics.camera import Camera
from graphics.drone import DroneRenderer
from graphics.environment import Environment
from graphics.hud import Hud
from graphics.objects import draw_crystals, draw_obstacles, draw_portal_energy, draw_portal_frame


def create_window():
    """Cria a janela com contexto OpenGL (tenta antialiasing 4x e, se falhar, usa sem)."""
    pygame.init()
    pygame.display.set_caption(config.TITLE)
    flags = pygame.OPENGL | pygame.DOUBLEBUF
    tamanho = (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    try:
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        pygame.display.set_mode(tamanho, flags)
    except pygame.error:
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 0)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 0)
        pygame.display.set_mode(tamanho, flags)


def init_opengl():
    """Estado global do OpenGL."""
    glEnable(GL_DEPTH_TEST)          # teste de profundidade (objetos da frente tapam os de trás)
    glDepthFunc(GL_LEQUAL)
    glEnable(GL_BLEND)               # transparência (brilhos, portal, hélices)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POINT_SMOOTH)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    try:
        glEnable(GL_MULTISAMPLE)
    except Exception:
        pass
    glClearColor(*config.BACKGROUND_BOTTOM, 1.0)
    lighting.setup()


def main():
    create_window()
    init_opengl()
    largura, altura = config.WINDOW_WIDTH, config.WINDOW_HEIGHT

    texturas = textures.load_all()
    ambiente = Environment(texturas)
    drone = DroneRenderer()
    camera = Camera()
    hud = Hud()
    missao = Mission()

    relogio = pygame.time.Clock()
    tempo = 0.0          # tempo acumulado do jogo (base das animações periódicas)
    rodando = True

    while rodando:
        # delta time: segundos desde o último quadro (animações não dependem do FPS)
        dt = min(relogio.tick(config.FPS) / 1000.0, config.MAX_DT)
        tempo += dt

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif evento.key == pygame.K_l:
                    lighting.toggle()
                elif evento.key == pygame.K_r:
                    missao.reset()
                    camera.snap(missao.player.x, missao.player.z)

        # ------------------------------------------------ atualização (lógica)
        teclas = pygame.key.get_pressed()
        missao.update(dt,
                      teclas[pygame.K_w], teclas[pygame.K_s],
                      teclas[pygame.K_a], teclas[pygame.K_d])
        drone.update(dt)
        camera.update(dt, missao.player.x, missao.player.z)

        # ------------------------------------------------ desenho (gráficos)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        ambiente.draw_background(tempo)
        camera.apply(largura, altura)
        lighting.apply(missao.portal_open)       # luzes são posicionadas depois da câmera

        ambiente.draw_world(tempo, missao.portal_open)
        draw_obstacles(missao.obstacles, texturas, tempo)
        draw_crystals(missao.crystals, tempo)
        draw_portal_frame(missao.portal_open, tempo)
        drone.draw(missao.player, tempo)
        draw_portal_energy(missao.portal_open, tempo)   # translúcido: por último

        hud.draw(missao, largura, altura, int(relogio.get_fps()))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
