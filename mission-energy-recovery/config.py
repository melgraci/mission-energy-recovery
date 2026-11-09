"""Configurações globais do jogo PINK GALAXY: ENERGY RECOVERY.

Todas as constantes ficam aqui para facilitar ajustes e explicações na apresentação.
"""

# ---------------------------------------------------------------- Janela
TITLE = "PINK GALAXY: ENERGY RECOVERY"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
MAX_DT = 0.05  # limite do delta time (evita saltos se o jogo travar)

# ---------------------------------------------------------------- Câmera / projeção
FOV = 55.0
NEAR_PLANE = 0.1
FAR_PLANE = 300.0

# ---------------------------------------------------------------- Cenário
PLATFORM_HALF = 10.0        # a plataforma vai de -10 a +10 em X e Z
PLATFORM_THICKNESS = 1.0
PORTAL_POS = (0.0, -8.0)    # posição (x, z) do portal de saída

# ---------------------------------------------------------------- Drone
DRONE_RADIUS = 0.6          # raio de colisão no plano XZ
DRONE_HEIGHT = 1.15         # altura de voo (eixo Y)
DRONE_SPEED = 6.5           # unidades por segundo
DRONE_RESPONSE = 12.0       # suavização da aceleração
DRONE_START = (0.0, 8.0)
PROPELLER_SPEED = 1400.0    # graus por segundo

# ---------------------------------------------------------------- Missão
CRYSTAL_TOTAL = 5
CRYSTAL_PICKUP_RADIUS = 0.95
CRYSTAL_COLLECT_TIME = 0.6      # duração da animação de coleta (s)
PORTAL_TRIGGER_RADIUS = 1.6
PORTAL_OPEN_SPEED = 0.7         # progresso de abertura por segundo (0 a 1)
MESSAGE_TIME = 2.5

# ---------------------------------------------------------------- Paleta (RGB 0..1)
PINK = (1.00, 0.20, 0.65)
LIGHT_PINK = (1.00, 0.72, 0.88)
LILAC = (0.78, 0.62, 1.00)
GALAXY_PURPLE = (0.32, 0.18, 0.52)
PEARL = (0.96, 0.94, 0.98)
METAL_GRAY = (0.62, 0.62, 0.70)

# Fundo (gradiente roxo galáctico, propositalmente claro)
BACKGROUND_TOP = (0.22, 0.12, 0.42)
BACKGROUND_BOTTOM = (0.58, 0.32, 0.68)

# ---------------------------------------------------------------- Texturas
TEXTURE_DIR = "assets/textures"
