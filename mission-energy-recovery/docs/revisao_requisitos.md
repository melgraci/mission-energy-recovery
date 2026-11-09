# Revisão dos requisitos: onde cada um foi implementado

| Requisito | Onde |
|---|---|
| Python, Pygame, PyOpenGL, GLU, Pillow | `requirements.txt`; `main.py`; `graphics/textures.py` (Pillow) |
| Plataforma 3D | `environment.py` → `_draw_platform` |
| Paredes/estrutura de estação, pilares, decoração | `environment.py` → `_draw_walls`, `_draw_pillars`, `_draw_floating_decor`, `_draw_far_decor` |
| Drone controlável | `game/player.py`; `graphics/drone.py` |
| 5 células de energia | `game/collectibles.py`; `graphics/objects.py` → `draw_crystals` |
| 3 obstáculos físicos | `game/obstacles.py`; `graphics/objects.py` → `draw_obstacles` |
| Portal de saída | `graphics/objects.py` → `draw_portal_frame`, `draw_portal_energy` |
| Drone em várias partes (corpo, visor, 4 braços, hélices, detalhes) | `drone.py` → `_draw_body`, `_draw_visor`, `_draw_arms_and_props`, `_draw_antenna` |
| Triângulos, quadriláteros, linhas (e mais) | `primitives.py`: GL_QUADS (caixa), GL_TRIANGLES (pirâmide, cone, cristal, hélice), GL_LINE_LOOP/GL_LINES (anéis, grade), GL_QUAD_STRIP, GL_TRIANGLE_FAN, GL_POINTS (estrelas) |
| Coordenadas 3D (X, Y, Z) | todos os `glVertex3f` |
| Formas variadas (não só cubos) | cone, cilindro, toro, esfera, pirâmide, cristal facetado |
| Perspectiva | `camera.py` → `gluPerspective` |
| Câmera acompanhando o drone | `camera.py` → `update`, `apply` (`gluLookAt`) |
| GL_DEPTH_TEST | `main.py` → `init_opengl` |
| Atualização da tela | `pygame.display.flip()` + `glClear` em `main.py` |
| Translação, rotação, escala | `glTranslatef`, `glRotatef`, `glScalef` em `drone.py`, `objects.py`, `environment.py` |
| Transformações hierárquicas | `drone.py` → `_draw_arms_and_props` (braço → motor → hélice) |
| glPushMatrix / glPopMatrix | em todos os módulos de desenho |
| Animação 1: rotação contínua | hélices: `DroneRenderer.update` |
| Animação 2: movimento periódico | cristais flutuando e pulsando: `draw_crystals` |
| Animação 3: por evento | cristal some ao ser coletado; portal abre ao coletar a 5ª célula (`Mission.portal_open`) |
| Uso de dt | `main.py` (`dt`); `player.py`, `mission.py`, `collectibles.py`, `drone.py`, `camera.py` |
| 2+ texturas | `metal.png` (plataforma), `tech_wall.png` (paredes e contêiner) |
| Repetição de textura | `GL_REPEAT` em `textures.py`; `draw_grid_plane` e `draw_box` com `tiles` |
| Origem das texturas e pasta | `assets/textures/CREDITOS.txt`; README |
| Luz ambiente | `lighting.setup` → `GL_LIGHT_MODEL_AMBIENT` e `GL_AMBIENT` |
| 1+ fonte de luz | `GL_LIGHT0` (principal) e `GL_LIGHT1` (rosa, no portal) |
| Normais coerentes | `glNormal3f` em todas as primitivas; `_flat_triangle` usa produto vetorial |
| Luz difusa e especular | `GL_DIFFUSE`, `GL_SPECULAR`, `lighting.material` |
| Tecla L | `main.py` → `lighting.toggle()` |
| W/A/S/D, R, ESC | `main.py`; `player.py` |
| Limites da plataforma | `Player.clamp_to_platform` |
| Coleta por proximidade | `Crystal.can_collect` |
| Contador de células | HUD `_top_left` |
| Colisão com obstáculos | `collisions.py`; `Obstacle.resolve`; `Mission.update` |
| Portal só após 5 células | `Mission.update` (`all_collected` e `portal_open >= 0.95`) |
| Mensagem de vitória | `hud.py` → `_victory` |
| R reinicia e restaura os coletáveis | `Mission.reset` |
| Instruções na tela | `hud.py` → `_bottom`, `_top_left` |
| Separação lógica x gráficos | pastas `game/` (sem OpenGL) e `graphics/` |
