# PINK GALAXY: ENERGY RECOVERY — Relatório de desenvolvimento

**Disciplina:** Computação Gráfica  
**Integrantes:** _(preencher)_  
**Tecnologias:** Python 3.12, Pygame, PyOpenGL e GLU, Pillow

## 1. Introdução

PINK GALAXY: ENERGY RECOVERY é um jogo 3D em que o jogador controla um drone de manutenção em uma estação espacial abandonada. A missão é coletar cinco células de energia, desviar de três obstáculos e entrar no portal de saída, que só se abre depois da última célula. A identidade visual usa rosa pink, rosa claro, lilás, roxo galáctico, branco perolado e cinza metálico, com fundo roxo claro para o cenário não ficar escuro.

O objetivo acadêmico foi aplicar os conceitos da disciplina diretamente em código OpenGL, sem motores prontos. Todos os objetos são construídos vértice a vértice com primitivas.

## 2. Arquitetura

O código separa **lógica** e **gráficos**. A pasta `game/` (jogador, colisões, cristais, obstáculos e missão) não usa OpenGL e pode ser testada sozinha. A pasta `graphics/` desenha o que a lógica informa (câmera, cenário, drone, objetos, iluminação, texturas e HUD). O `main.py` executa o laço: eventos, atualização com *delta time*, desenho e `flip`. As constantes ficam em `config.py`.

## 3. Modelagem e primitivas

Os modelos usam coordenadas 3D e primitivas do OpenGL: `GL_QUADS` (caixas, painéis), `GL_TRIANGLES` (pirâmides, cones, cristais, hélices), `GL_QUAD_STRIP` (cilindros e toros), `GL_TRIANGLE_FAN` (discos), `GL_LINES` e `GL_LINE_LOOP` (grade, anéis neon) e `GL_POINTS` (estrelas). A esfera vem da GLU (`gluSphere`). Para não repetir milhares de chamadas por quadro, cada forma é compilada uma vez em uma *display list* (`glNewList`) e reaproveitada com `glCallList`.

O **drone** é composto por corpo (esfera achatada), anel metálico, calota cônica, visor, quatro braços em caixa, quatro motores cilíndricos, quatro hélices de duas pás, luzes e antena. O cenário tem plataforma com casco inferior piramidal, paredes de estação, pilares com anéis neon, satélites cristalinos, planeta com anel e estrelas. Os obstáculos são um contêiner (caixa), um tanque (cilindro com toros) e uma torre (cone com esfera).

## 4. Câmera e projeção

A projeção em perspectiva usa `gluPerspective` (FOV 55°) e a visão usa `gluLookAt`, posicionando a câmera acima e atrás do drone. A câmera o segue com suavização exponencial (`1 - exp(-4·dt)`), então o movimento é fluido em qualquer FPS. `GL_DEPTH_TEST` está ativo, e os elementos translúcidos (brilhos, campo do portal) são desenhados no fim com `glDepthMask(GL_FALSE)` para não corromper o buffer de profundidade.

## 5. Transformações geométricas

- **Translação:** posiciona drone, cristais, obstáculos e portal.
- **Rotação:** direção e inclinação do drone, giro dos cristais, rotação das hélices e do espiral do portal.
- **Escala:** achatamento do corpo do drone, pulso dos cristais, abertura do portal e encolhimento do cristal coletado.

As transformações são **hierárquicas** com `glPushMatrix`/`glPopMatrix`: o drone aplica translação e rotação; cada braço gira em torno do corpo; o motor fica na ponta do braço; a hélice herda a posição do braço e gira sozinha. Assim cada hélice é controlada individualmente (sentidos alternados) sem afetar o resto.

## 6. Animações

Todas usam o tempo decorrido entre quadros (`dt`, limitado a 0,05 s), sem depender do FPS.

1. **Rotação contínua:** as hélices somam `1400 · dt` graus por quadro.
2. **Movimento periódico:** os cristais flutuam e pulsam com `sin(t)`, com fase diferente para cada um. As luzes do drone e a antena também pulsam.
3. **Animação por evento:** ao coletar uma célula, o cristal gira rápido, sobe, encolhe e some em 0,6 s. Ao coletar a quinta, o portal abre gradualmente: o campo de energia cresce, o anel brilha mais e a luz rosa do portal aumenta.

## 7. Texturas

Foram criadas duas texturas com Pillow (`graphics/texture_generator.py`): `metal.png`, metal escovado com juntas e rebites, usada na plataforma; e `tech_wall.png`, painel roxo com trilhas de circuito, usada nas paredes e no contêiner. Nenhuma imagem de terceiros foi usada. O carregamento (`textures.py`) inverte a imagem verticalmente, configura `GL_REPEAT`, filtros com mipmaps (`gluBuild2DMipmaps`) e `GL_MODULATE`, de modo que textura, cor e luz se combinam. A **repetição** aparece na plataforma, onde cada unidade de mundo recebe 0,5 repetição de textura, formando uma malha de painéis.

## 8. Iluminação

O modelo de iluminação do OpenGL está ativo com:

- **Ambiente:** luz ambiente global e da `GL_LIGHT0`, para que nada fique preto.
- **Difusa:** `GL_LIGHT0`, luz branco-lilás posicional acima da plataforma.
- **Especular:** brilho `GL_SPECULAR` nas luzes e materiais com `GL_SHININESS`; `GL_SEPARATE_SPECULAR_COLOR` mantém o brilho visível sobre texturas.
- **Segunda luz:** `GL_LIGHT1`, rosa neon no portal, com atenuação; sua intensidade cresce conforme o portal abre.
- **Normais:** definidas em todas as primitivas; nos sólidos facetados (cristais, pirâmides) são calculadas por produto vetorial, e `GL_NORMALIZE` as renormaliza após `glScalef`.

A tecla **L** liga e desliga a iluminação (`GL_LIGHTING`). Desligada, as superfícies ficam chapadas, sem volume nem brilho, o que torna a diferença evidente. Linhas neon, campo do portal, estrelas e HUD são desenhados sem iluminação por serem emissivos.

## 9. Mecânicas

O drone se move com W/A/S/D com velocidade suavizada e fica limitado à plataforma. A coleta usa proximidade no plano XZ (raio 0,95). Os obstáculos usam colisão círculo × retângulo (contêiner) ou círculo × círculo (tanque e torre) com correção de posição: o drone é empurrado para fora e o impacto conta no HUD. O portal exige as cinco células e a abertura completa; sem elas, exibe aviso. A vitória mostra "MISSÃO CONCLUÍDA" e a orientação para reiniciar com **R**, que restaura células, portal, contador e posição. O HUD (Pygame renderizando texto em texturas sobre projeção ortográfica) mostra título, energia 0/5, objetivo, estado da luz, controles e mensagens.

## 10. Conclusão

O projeto cobre perspectiva, depth test, primitivas, transformações hierárquicas, animações com dt, texturas com repetição e iluminação ambiente, difusa e especular, em um jogo jogável e visualmente coeso. Como evolução possível: sombras reais, mais fases e efeitos de partículas.
