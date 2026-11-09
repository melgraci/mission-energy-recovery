"""Regras da missão: coleta, obstáculos, portal e vitória."""
import config
from game import collisions
from game.collectibles import create_crystals
from game.obstacles import create_obstacles
from game.player import Player

PLAYING = "playing"
WON = "won"


class Mission:
    def __init__(self):
        self.player = Player()
        self.reset()

    def reset(self):
        """Reinicia a partida e restaura todos os objetos coletáveis."""
        self.player.reset()
        self.crystals = create_crystals()
        self.obstacles = create_obstacles()
        self.state = PLAYING
        self.portal_open = 0.0        # 0 = fechado; 1 = totalmente aberto (animação por evento)
        self.hits = 0
        self.was_colliding = False
        self.message = ""
        self.message_timer = 0.0
        self.win_timer = 0.0
        self.say("Colete as 5 células de energia!")

    # -------------------------------------------------------------- propriedades
    @property
    def collected(self):
        return sum(1 for c in self.crystals if c.collected)

    @property
    def total(self):
        return config.CRYSTAL_TOTAL

    @property
    def all_collected(self):
        return self.collected >= self.total

    @property
    def won(self):
        return self.state == WON

    def say(self, texto, duracao=config.MESSAGE_TIME):
        self.message = texto
        self.message_timer = duracao

    # -------------------------------------------------------------- atualização
    def update(self, dt, forward, back, left, right):
        self.message_timer = max(0.0, self.message_timer - dt)
        for cristal in self.crystals:
            cristal.update(dt)

        # o portal abre aos poucos depois da 5ª célula (animação baseada em dt)
        if self.all_collected:
            self.portal_open = min(1.0, self.portal_open + config.PORTAL_OPEN_SPEED * dt)

        if self.won:
            self.win_timer += dt
            return

        p = self.player
        p.update(dt, forward, back, left, right)
        p.clamp_to_platform()

        colidindo = collisions.resolve_player_vs_obstacles(p, self.obstacles, config.DRONE_RADIUS)
        if colidindo and not self.was_colliding:   # conta só no instante do impacto
            self.hits += 1
            self.say("Colisão com obstáculo! Desvie!", 1.2)
        self.was_colliding = colidindo
        p.clamp_to_platform()

        for cristal in self.crystals:
            if cristal.can_collect(p.x, p.z):
                cristal.collected = True
                cristal.collect_timer = 0.0
                if self.all_collected:
                    self.say("Todas as células coletadas! O portal está abrindo!", 4.0)
                else:
                    self.say("Célula coletada! %d/%d" % (self.collected, self.total), 1.5)

        px, pz = config.PORTAL_POS
        if collisions.distance_xz(p.x, p.z, px, pz) <= config.PORTAL_TRIGGER_RADIUS:
            if self.all_collected and self.portal_open >= 0.95:
                self.state = WON
                self.win_timer = 0.0
            elif not self.all_collected and self.message_timer <= 0.0:
                self.say("Portal bloqueado: faltam %d célula(s)." % (self.total - self.collected), 2.0)
