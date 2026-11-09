"""Gera proceduralmente as texturas do jogo com Pillow.

As imagens são criadas por este próprio código (autoria do grupo), portanto não
dependem de arquivos de terceiros. Se os PNGs não existirem em assets/textures,
o jogo chama estas funções automaticamente.
"""
import os
import random

from PIL import Image, ImageDraw

SIZE = 256


def _clamp(v):
    return max(0, min(255, v))


def generate_metal(path):
    """Textura de metal escovado com painéis, rebites e linha lilás."""
    rng = random.Random(11)
    img = Image.new("RGB", (SIZE, SIZE))
    px = img.load()
    base = (170, 162, 190)
    for y in range(SIZE):
        faixa = rng.randint(-12, 12)          # variação por linha = riscos horizontais
        for x in range(SIZE):
            ruido = rng.randint(-7, 7) + faixa
            px[x, y] = (_clamp(base[0] + ruido), _clamp(base[1] + ruido), _clamp(base[2] + ruido))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, SIZE - 1, SIZE - 1], outline=(92, 80, 126), width=4)      # junta do painel
    d.rectangle([5, 5, SIZE - 6, SIZE - 6], outline=(228, 218, 245), width=1)    # brilho do chanfro
    d.rectangle([12, 12, SIZE - 13, SIZE - 13], outline=(200, 140, 255), width=1)  # linha tecnológica
    for cx, cy in ((22, 22), (SIZE - 23, 22), (22, SIZE - 23), (SIZE - 23, SIZE - 23)):
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(120, 110, 150), outline=(70, 60, 100))
        d.ellipse([cx - 2, cy - 3, cx, cy - 1], fill=(235, 230, 250))
    d.line([(SIZE // 2, 12), (SIZE // 2, SIZE - 13)], fill=(150, 125, 190), width=1)
    d.line([(12, SIZE // 2), (SIZE - 13, SIZE // 2)], fill=(150, 125, 190), width=1)
    img.save(path)


def generate_tech_wall(path):
    """Textura tecnológica: painel roxo com trilhas de circuito rosa/lilás e LEDs."""
    rng = random.Random(23)
    img = Image.new("RGB", (SIZE, SIZE))
    px = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            n = rng.randint(-6, 6)
            g = int(12 * y / SIZE)   # leve degradê vertical
            px[x, y] = (_clamp(96 + n + g), _clamp(68 + n + g), _clamp(142 + n + g))
    d = ImageDraw.Draw(img)
    cores = [(255, 110, 190), (200, 160, 255), (255, 190, 225)]
    for _ in range(14):
        x, y = rng.randrange(24, SIZE - 24, 8), rng.randrange(24, SIZE - 24, 8)
        cor = rng.choice(cores)
        for _ in range(rng.randint(2, 4)):
            if rng.random() < 0.5:
                nx = max(16, min(SIZE - 16, x + rng.choice((-1, 1)) * rng.randrange(16, 64, 8)))
                d.line([(x, y), (nx, y)], fill=cor, width=2)
                x = nx
            else:
                ny = max(16, min(SIZE - 16, y + rng.choice((-1, 1)) * rng.randrange(16, 64, 8)))
                d.line([(x, y), (x, ny)], fill=cor, width=2)
                y = ny
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=cor, outline=(255, 255, 255))
    for _ in range(6):
        x, y = rng.randrange(24, SIZE - 40, 8), rng.randrange(24, SIZE - 30, 8)
        d.rectangle([x, y, x + 14, y + 8], fill=(60, 40, 100), outline=(230, 200, 255))
    d.rectangle([0, 0, SIZE - 1, SIZE - 1], outline=(52, 36, 90), width=4)
    d.rectangle([5, 5, SIZE - 6, SIZE - 6], outline=(255, 120, 200), width=1)
    img.save(path)


def ensure_textures(directory):
    """Cria a pasta e gera as texturas que ainda não existirem."""
    os.makedirs(directory, exist_ok=True)
    metal = os.path.join(directory, "metal.png")
    wall = os.path.join(directory, "tech_wall.png")
    if not os.path.exists(metal):
        generate_metal(metal)
    if not os.path.exists(wall):
        generate_tech_wall(wall)


if __name__ == "__main__":
    ensure_textures(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "textures"))
    print("Texturas geradas em assets/textures")
