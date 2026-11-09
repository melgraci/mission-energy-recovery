# PINK GALAXY: ENERGY RECOVERY

Jogo 3D de ficção científica feito em **Python 3.12 + Pygame + PyOpenGL (GLU)** para a disciplina de Computação Gráfica.
Você controla um pequeno drone de manutenção em uma estação espacial sem energia: recupere **5 células de energia**, desvie de **3 obstáculos** e alcance o **portal de saída**.

## Instalação (Windows + VS Code)

1. Instale o Python 3.12 (marque *Add Python to PATH*).
2. Abra a pasta `mission-energy-recovery` no VS Code e abra o terminal (`Ctrl + '`).
3. Crie e ative um ambiente virtual:
   ```powershell
   py -3.12 -m venv .venv
   .venv\Scripts\activate
   ```
   Se o PowerShell bloquear a ativação, rode uma vez: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
4. Instale as bibliotecas:
   ```powershell
   pip install -r requirements.txt
   ```
5. Execute:
   ```powershell
   python main.py
   ```

As texturas já estão em `assets/textures`. Se forem apagadas, o jogo as gera de novo automaticamente.

## Controles

| Tecla | Ação |
|-------|------|
| W / S | Frente / trás |
| A / D | Esquerda / direita |
| L | Liga/desliga a iluminação |
| R | Reinicia a partida |
| ESC | Sai |

## Como jogar

- Toque nas células rosas para coletá-las (contador no canto superior esquerdo).
- Os obstáculos (contêiner, tanque e torre) bloqueiam o drone; cada impacto é contado.
- Com as 5 células, o portal abre sozinho. Entre nele para vencer.

## Estrutura

```
main.py                 laço principal, entrada e ordem de desenho
config.py               constantes e paleta de cores
graphics/               tudo que usa OpenGL
  camera.py             projeção em perspectiva + gluLookAt
  environment.py        fundo, plataforma, paredes, pilares, decoração
  drone.py              modelo hierárquico do drone
  objects.py            obstáculos, cristais e portal
  primitives.py         primitivas (quads, triângulos, linhas, pontos) em display lists
  lighting.py           luzes e materiais
  textures.py           carregamento de texturas (Pillow)
  texture_generator.py  gera as texturas proceduralmente
  hud.py                interface 2D
game/                   lógica, sem OpenGL
  player.py  collectibles.py  obstacles.py  collisions.py  mission.py
assets/textures/        metal.png, tech_wall.png, CREDITOS.txt
docs/                   relatório, roteiro, explicação do código, checklist
```

## Origem das texturas

`metal.png` e `tech_wall.png` foram **geradas proceduralmente** pelo script `graphics/texture_generator.py` (Pillow), com autoria do grupo. Nenhuma imagem de terceiros foi usada. Detalhes em `assets/textures/CREDITOS.txt`.
