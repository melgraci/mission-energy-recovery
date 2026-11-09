# Explicação dos principais trechos (para responder ao professor)

## 1. Laço principal (`main.py`)
A cada quadro: calcula `dt = relogio.tick(60) / 1000` (segundos desde o quadro anterior, limitado a 0,05); trata eventos (ESC, L, R); lê W/A/S/D; atualiza a lógica (`missao.update`); limpa as telas (`glClear`); desenha cenário e objetos; desenha o HUD; troca os buffers (`flip`). **Pergunta típica: "como a animação não depende do FPS?"** Tudo é multiplicado por `dt`, ex.: `angulo += velocidade * dt`.

## 2. Projeção e câmera (`graphics/camera.py`)
`gluPerspective(fov, aspecto, near, far)` cria a perspectiva (objetos distantes ficam menores). `gluLookAt(olho, alvo, cima)` posiciona a câmera. Ela segue o drone com suavização exponencial. **Depth test:** `glEnable(GL_DEPTH_TEST)` em `main.py` faz o buffer de profundidade decidir qual pixel fica na frente.

## 3. Pilha de matrizes e hierarquia (`graphics/drone.py`)
`glPushMatrix()` guarda a matriz atual e `glPopMatrix()` a restaura. No drone: `glTranslatef` (posição) → `glRotatef` (inclinação/direção) → para cada braço `glRotatef(ang)` → `glTranslatef` até a ponta → `glRotatef(prop_angle)` para a hélice. Como a hélice vem depois das transformações do braço, ela herda a posição e gira por conta própria. **Escala:** `glScalef(1, 0.5, 1)` achata a esfera do corpo.

## 4. Primitivas (`graphics/primitives.py`)
- Caixa: 6 faces com `GL_QUADS`.
- Pirâmide, cone, cristal e hélice: `GL_TRIANGLES`. Em sólidos facetados, a normal vem do produto vetorial `(b-a) × (c-a)` (`_flat_triangle`), invertida se apontar para dentro.
- Cilindro e toro: `GL_QUAD_STRIP`; discos: `GL_TRIANGLE_FAN`.
- Linhas: `GL_LINE_LOOP` e `GL_LINES`; estrelas: `GL_POINTS`.
- **Display lists:** `@_cached` compila a forma uma vez (`glNewList`/`glEndList`) e a reaproveita (`glCallList`), reduzindo chamadas por quadro.

## 5. Texturas (`graphics/textures.py`)
Pillow abre o PNG; `transpose(FLIP_TOP_BOTTOM)` ajusta a origem; `glGenTextures` e `glBindTexture` criam o objeto; `GL_REPEAT` repete a textura quando as coordenadas passam de 1; `gluBuild2DMipmaps` gera os mipmaps. Nos planos, as coordenadas `glTexCoord2f` vão até `tamanho * 0.5`, ou seja, repetem a imagem várias vezes. `GL_MODULATE` multiplica textura, cor e luz.

## 6. Iluminação (`graphics/lighting.py`)
- Ambiente: luz que atinge tudo igualmente (evita preto total).
- Difusa: depende do ângulo entre a normal e a direção da luz (`N · L`).
- Especular: brilho concentrado, depende da posição do observador; `GL_SHININESS` controla o tamanho do ponto de brilho.
- `GL_COLOR_MATERIAL` faz `glColor` virar a cor do material.
- As posições das luzes são definidas **depois** da câmera, pois `glLightfv(GL_POSITION)` passa pela matriz atual.
- Tecla L: `lighting.toggle()` alterna `GL_LIGHTING` em `lighting.apply`.
- Objetos emissivos (neon, portal) chamam `emissive_begin()` para ignorar a luz.

## 7. Animações
- `DroneRenderer.update`: `prop_angle += 1400 * dt`.
- `draw_crystals`: `altura = 1.15 + 0.22 * sin(t*2 + fase)` e escala pulsando.
- Evento de coleta: `Crystal.collect_timer += dt`; `progress` vai de 0 a 1; escala diminui, altura e giro aumentam.
- Portal: `Mission.portal_open += PORTAL_OPEN_SPEED * dt` até 1; controla a escala do campo, o brilho do anel e a luz rosa.

## 8. Colisões (`game/collisions.py`)
Todas no plano XZ. Círculo × círculo: se `distância < r1 + r2`, empurra o jogador ao longo da direção entre os centros. Círculo × retângulo: acha o ponto do retângulo mais próximo do círculo e compara a distância com o raio. Coleta: distância ≤ 0,95. Limites: `abs(x) > 10 - raio` trava a posição.

## 9. Missão (`game/mission.py`)
Estados `playing` e `won`. O portal só vence se `all_collected` e `portal_open >= 0.95`. `reset()` recria jogador, cristais e obstáculos, zerando portal, contador e colisões.

## 10. HUD (`graphics/hud.py`)
Muda para projeção ortográfica (`glOrtho`) com origem no canto superior esquerdo; desliga profundidade e luz; desenha retângulos translúcidos (`GL_QUADS` com blending) e textos renderizados pelo `pygame.font` em texturas (com cache); depois restaura as matrizes.

## Perguntas prováveis
- **Por que `glPushMatrix` em volta de cada parte?** Para que a transformação de uma parte não afete as seguintes.
- **Por que `GL_NORMALIZE`?** `glScalef` altera o comprimento das normais; ele as renormaliza para a luz continuar correta.
- **Por que desligar `glDepthMask` nos translúcidos?** Para não bloquearem o que for desenhado atrás deles.
- **Onde fica a perspectiva?** `gluPerspective` na matriz GL_PROJECTION.
