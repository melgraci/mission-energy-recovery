# Roteiro de apresentação (≈ 5 minutos)

Divisão sugerida para três integrantes. Ajuste os nomes.

**0:00–0:30 · Abertura (Pessoa 1)**  
"Apresentamos PINK GALAXY: ENERGY RECOVERY. Um drone de manutenção precisa recuperar 5 células de energia, desviar de 3 obstáculos e chegar ao portal." Abra o jogo e mostre o HUD.

**0:30–1:30 · Jogo ao vivo (Pessoa 1)**  
Mova com W/A/S/D, colete uma célula (mostre o cristal subindo e sumindo), encoste num obstáculo (aviso e contador de colisões) e tente o portal fechado (aviso).

**1:30–2:30 · Modelagem e transformações (Pessoa 2)**  
Abra `graphics/drone.py`. Explique: o drone é feito de várias partes, tudo com primitivas (`primitives.py`). Mostre `_draw_arms_and_props`: braço → motor → hélice com `glPushMatrix/glPopMatrix`; translação, rotação e escala. Câmera: `camera.py` com `gluPerspective` e `gluLookAt`; depth test em `main.py`.

**2:30–3:30 · Animações e texturas (Pessoa 2)**  
Hélices: rotação contínua com `dt`. Cristais: flutuam com `sin`. Evento: cristal some ao ser coletado e o portal abre na 5ª célula. Texturas: `metal.png` na plataforma com repetição; `tech_wall.png` nas paredes; ambas geradas por código.

**3:30–4:30 · Iluminação (Pessoa 3)**  
Pressione **L** ao vivo, ligando e desligando. Explique ambiente, difusa e especular em `lighting.py`, as duas luzes (principal e rosa do portal) e as normais.

**4:30–5:00 · Fechamento (Pessoa 3)**  
Colete tudo, entre no portal e mostre a vitória. Pressione **R** para reiniciar. Agradeça e abra para perguntas.

**Dicas:** ensaie o percurso; deixe o VS Code aberto em `drone.py` e `lighting.py`; teste o jogo antes da apresentação.
