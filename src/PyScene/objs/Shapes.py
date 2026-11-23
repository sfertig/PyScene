import pygame
from ..Math import Vector2D
from ..Game import Game

from .GameObj import GameObj

class Rect(GameObj):
    def __init__(self, x, y, w, h, color, width=0, z_index=0, active=True, visible=True, offset=True, Global=False):
        super().__init__(Vector2D(x, y), z_index, active, visible, Global)
        self.dim = Vector2D(w, h)
        self.color = color
        self.rect = pygame.Rect((x, y), (w, h))
        self.offset = offset
        self.width = width

    def update(self):
        if self.pos.to_int() != self.rect.topleft: self.rect.topleft = self.pos.to_int()

    def render(self, screen, cam):
        r = self.rect.copy()
        if self.offset: r.topleft = (r.x - cam.x, r.y - cam.y)
        pygame.draw.rect(screen, self.color, r, self.width)


class Circle(GameObj):
    def __init__(self, x, y, r, color, width=0, z_index=0, active=True, visible=True, offset=True, Global=False):
        super().__init__(Vector2D(x, y), z_index, active, visible, Global)
        self.radius = r
        self.color = color
        self.width = width
        self.offset = offset

    def render(self, screen, cam):
        p = self.pos.copy()
        if self.offset: p -= cam
        pygame.draw.circle(screen, self.color, p.to_int(), self.r, self.width)

class Line(GameObj):
    def __init__(self, x1, y1, x2, y2, color, width=1, z_index=0, active=True, visible=True, offset=True, Global=False):
        super().__init__(Vector2D(x1, y1), z_index, active, visible, Global)
        self.end = Vector2D(x2, y2)
        self.color = color
        self.width = width
        self.offset = offset

    def render(self, screen, cam): 
        s = self.pos.copy()
        e = self.end.copy()
        if self.offset:
            s -= cam
            e -= cam
        pygame.draw.line(screen, self.color, s.to_int(), e.to_int(), self.width)
