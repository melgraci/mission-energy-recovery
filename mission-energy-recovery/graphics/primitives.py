"""Primitivas geométricas desenhadas com OpenGL (modo imediato).

Usa GL_QUADS, GL_TRIANGLES, GL_TRIANGLE_FAN, GL_QUAD_STRIP, GL_LINES,
GL_LINE_LOOP e GL_POINTS. Todas as formas têm normais para a iluminação
e coordenadas de textura quando faz sentido.
"""
import math

from OpenGL.GL import *
from OpenGL.GLU import *

_quadric = None


# ------------------------------------------------------------------ Display lists
_lists = {}


def _cached(func):
    """Compila a geometria em uma display list na primeira chamada e a reutiliza depois.

    Isso evita milhares de chamadas Python por quadro (desempenho), sem mudar o
    resultado visual: a lista guarda exatamente os mesmos vértices e normais.
    """
    def wrapper(*args):
        chave = (func.__name__,) + args
        lista = _lists.get(chave)
        if lista is None:
            lista = glGenLists(1)
            glNewList(lista, GL_COMPILE)
            func(*args)
            glEndList()
            _lists[chave] = lista
        glCallList(lista)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper



def _get_quadric():
    """Cria (uma única vez) o objeto quadric da GLU usado nas esferas."""
    global _quadric
    if _quadric is None:
        _quadric = gluNewQuadric()
        gluQuadricNormals(_quadric, GLU_SMOOTH)
    return _quadric


def _normalize(v):
    length = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2) or 1.0
    return (v[0] / length, v[1] / length, v[2] / length)


def _flat_triangle(a, b, c, center=(0.0, 0.0, 0.0)):
    """Desenha um triângulo com normal de face calculada pelo produto vetorial.

    A normal é invertida se apontar para dentro do sólido (em direção ao centro).
    """
    u = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    v = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    n = _normalize((u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]))
    mid = ((a[0] + b[0] + c[0]) / 3 - center[0], (a[1] + b[1] + c[1]) / 3 - center[1],
           (a[2] + b[2] + c[2]) / 3 - center[2])
    if n[0] * mid[0] + n[1] * mid[1] + n[2] * mid[2] < 0:
        n = (-n[0], -n[1], -n[2])
    glNormal3f(*n)
    glVertex3f(*a)
    glVertex3f(*b)
    glVertex3f(*c)


# ------------------------------------------------------------------ Caixa (GL_QUADS)
@_cached
def draw_box(sx, sy, sz, tiles=None):
    """Paralelepípedo centrado na origem. `tiles` = repetições de textura por unidade."""
    hx, hy, hz = sx / 2, sy / 2, sz / 2
    faces = [
        ((0, 0, 1), [(-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz)], (sx, sy)),
        ((0, 0, -1), [(hx, -hy, -hz), (-hx, -hy, -hz), (-hx, hy, -hz), (hx, hy, -hz)], (sx, sy)),
        ((1, 0, 0), [(hx, -hy, hz), (hx, -hy, -hz), (hx, hy, -hz), (hx, hy, hz)], (sz, sy)),
        ((-1, 0, 0), [(-hx, -hy, -hz), (-hx, -hy, hz), (-hx, hy, hz), (-hx, hy, -hz)], (sz, sy)),
        ((0, 1, 0), [(-hx, hy, hz), (hx, hy, hz), (hx, hy, -hz), (-hx, hy, -hz)], (sx, sz)),
        ((0, -1, 0), [(-hx, -hy, -hz), (hx, -hy, -hz), (hx, -hy, hz), (-hx, -hy, hz)], (sx, sz)),
    ]
    glBegin(GL_QUADS)
    for normal, verts, (w, h) in faces:
        ru, rv = (w * tiles, h * tiles) if tiles else (1.0, 1.0)
        glNormal3f(*normal)
        for (u, v), vert in zip(((0, 0), (ru, 0), (ru, rv), (0, rv)), verts):
            glTexCoord2f(u, v)
            glVertex3f(*vert)
    glEnd()


@_cached
def draw_grid_plane(half, divisions, tiles, y=0.0):
    """Plano horizontal subdividido (a subdivisão melhora a luz por vértice).

    Usa repetição de textura (GL_REPEAT): `tiles` repetições por unidade.
    """
    step = 2.0 * half / divisions
    glNormal3f(0, 1, 0)
    glBegin(GL_QUADS)
    for i in range(divisions):
        for j in range(divisions):
            x0, z0 = -half + i * step, -half + j * step
            x1, z1 = x0 + step, z0 + step
            for x, z in ((x0, z1), (x1, z1), (x1, z0), (x0, z0)):
                glTexCoord2f((x + half) * tiles, (z + half) * tiles)
                glVertex3f(x, y, z)
    glEnd()


# ------------------------------------------------------------------ Pirâmide / cone (GL_TRIANGLES)
@_cached
def draw_pyramid(base_half, height):
    """Pirâmide de base quadrada com a base em y=0 e o ápice em y=height."""
    h = base_half
    apex = (0.0, height, 0.0)
    corners = [(-h, 0, h), (h, 0, h), (h, 0, -h), (-h, 0, -h)]
    center = (0.0, height * 0.3, 0.0)
    glBegin(GL_TRIANGLES)
    for i in range(4):
        _flat_triangle(corners[i], corners[(i + 1) % 4], apex, center)
    glEnd()
    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0)
    for c in reversed(corners):
        glVertex3f(*c)
    glEnd()


@_cached
def draw_cone(radius, height, slices=24):
    """Cone com a base em y=0 e o ápice em y=height (normais suaves)."""
    glBegin(GL_TRIANGLES)
    for i in range(slices):
        a0 = 2 * math.pi * i / slices
        a1 = 2 * math.pi * (i + 1) / slices
        am = (a0 + a1) / 2
        n0 = _normalize((math.cos(a0) * height, radius, math.sin(a0) * height))
        n1 = _normalize((math.cos(a1) * height, radius, math.sin(a1) * height))
        nm = _normalize((math.cos(am) * height, radius, math.sin(am) * height))
        glNormal3f(*n0)
        glTexCoord2f(i / slices, 0)
        glVertex3f(radius * math.cos(a0), 0, radius * math.sin(a0))
        glNormal3f(*n1)
        glTexCoord2f((i + 1) / slices, 0)
        glVertex3f(radius * math.cos(a1), 0, radius * math.sin(a1))
        glNormal3f(*nm)
        glTexCoord2f((i + 0.5) / slices, 1)
        glVertex3f(0, height, 0)
    glEnd()
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0, -1, 0)
    glVertex3f(0, 0, 0)
    for i in range(slices + 1):
        a = 2 * math.pi * i / slices
        glVertex3f(radius * math.cos(a), 0, -radius * math.sin(a))
    glEnd()


# ------------------------------------------------------------------ Cilindro (GL_QUAD_STRIP)
@_cached
def draw_cylinder(radius, height, slices=24, caps=True, tiles_v=1.0):
    """Cilindro centrado na origem com eixo Y (de -height/2 a +height/2)."""
    hh = height / 2
    glBegin(GL_QUAD_STRIP)
    for i in range(slices + 1):
        a = 2 * math.pi * i / slices
        nx, nz = math.cos(a), math.sin(a)
        glNormal3f(nx, 0, nz)
        glTexCoord2f(i / slices * 2, tiles_v)
        glVertex3f(radius * nx, hh, radius * nz)
        glTexCoord2f(i / slices * 2, 0)
        glVertex3f(radius * nx, -hh, radius * nz)
    glEnd()
    if caps:
        for sign in (1, -1):
            glBegin(GL_TRIANGLE_FAN)
            glNormal3f(0, sign, 0)
            glVertex3f(0, sign * hh, 0)
            for i in range(slices + 1):
                a = 2 * math.pi * i / slices * sign
                glVertex3f(radius * math.cos(a), sign * hh, radius * math.sin(a))
            glEnd()


# ------------------------------------------------------------------ Cristal (GL_TRIANGLES)
@_cached
def draw_crystal(radius, height, sides=6, lower_ratio=0.6):
    """Cristal facetado: bipirâmide alongada com faces planas (normais por face)."""
    top = (0.0, height, 0.0)
    bottom = (0.0, -height * lower_ratio, 0.0)
    ring = [(radius * math.cos(2 * math.pi * i / sides), 0.0, radius * math.sin(2 * math.pi * i / sides))
            for i in range(sides)]
    glBegin(GL_TRIANGLES)
    for i in range(sides):
        p0, p1 = ring[i], ring[(i + 1) % sides]
        _flat_triangle(p0, p1, top)
        _flat_triangle(p1, p0, bottom)
    glEnd()


# ------------------------------------------------------------------ Toro (GL_QUAD_STRIP)
@_cached
def draw_torus(major, minor, segments=36, sides=12):
    """Anel (toro) no plano XY, com eixo em Z."""
    for i in range(segments):
        a0 = 2 * math.pi * i / segments
        a1 = 2 * math.pi * (i + 1) / segments
        glBegin(GL_QUAD_STRIP)
        for j in range(sides + 1):
            b = 2 * math.pi * j / sides
            for a in (a0, a1):
                glNormal3f(math.cos(b) * math.cos(a), math.cos(b) * math.sin(a), math.sin(b))
                r = major + minor * math.cos(b)
                glVertex3f(r * math.cos(a), r * math.sin(a), minor * math.sin(b))
        glEnd()


# ------------------------------------------------------------------ Esfera (GLU)
@_cached
def draw_sphere(radius, slices=24, stacks=16):
    gluSphere(_get_quadric(), radius, slices, stacks)


# ------------------------------------------------------------------ Disco e hélice
@_cached
def draw_disc(radius, slices=32):
    """Disco horizontal (leque de triângulos) com normal para cima."""
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    for i in range(slices + 1):
        a = 2 * math.pi * i / slices
        glVertex3f(radius * math.cos(a), 0, radius * math.sin(a))
    glEnd()


@_cached
def draw_propeller(length, width):
    """Hélice de duas pás afuniladas (triângulos), no plano XZ."""
    glBegin(GL_TRIANGLES)
    glNormal3f(0, 1, 0)
    for sign in (1, -1):
        a = (sign * 0.06, 0, -width * 0.5)
        b = (sign * length, 0, -width * 0.2)
        c = (sign * length, 0, width * 0.2)
        d = (sign * 0.06, 0, width * 0.5)
        for tri in ((a, b, c), (a, c, d)):
            for vert in tri:
                glVertex3f(*vert)
    glEnd()


# ------------------------------------------------------------------ Linhas
@_cached
def draw_line_ring(radius, segments=48):
    """Anel de linhas (GL_LINE_LOOP) no plano XZ."""
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        a = 2 * math.pi * i / segments
        glVertex3f(radius * math.cos(a), 0, radius * math.sin(a))
    glEnd()
