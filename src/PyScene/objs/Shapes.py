import pygame
from ..Math import Vector2D
from ..Game import Game

from .GameObj import GameObj

class Rect(GameObj):
    def __init__(self, x, y, w, h, color, z_index=0, width=0, active=True, visible=True, offset=True, Global=False):
        super().__init__(Vector2D(x, y), z_index, active, visible, Global)
        self.dim = Vector2D(w, h)
        self.color = color
        self.rect = pygame.Rect((x, y), (w, h))
        self.offset = offset
        self.width = width

    def update(self):
        if self.pos.to_int() != self.rect.topleft: self.rect.topleft = self.pos.to_int()

    def render(self):
        if not self.visible: return
        Game.cam.draw_rect(self.rect, self.color, self.width, self.offset)

class Circle(GameObj):
    def __init__(self, x, y, r, color, z_index=0, width=0, active=True, visible=True, offset=True, Global=False):
        super().__init__(Vector2D(x, y), z_index, active, visible, Global)
        self.radius = r
        self.color = color
        self.width = width
        self.offset = offset

    def render(self):
        if not self.visible: return
        Game.cam.draw_circle(self.pos, self.radius, self.color, self.width, self.offset)

class Line(GameObj):
    def __init__(self, x1, y1, x2, y2, color, z_index=0, width=1, active=True, visible=True, offset=True, Global=False):
        super().__init__(Vector2D(x1, y1), z_index, active, visible, Global)
        self.end = Vector2D(x2, y2)
        self.color = color
        self.width = width
        self.offset = offset

    def render(self): 
        if not self.visible: return
        Game.cam.draw_line(self.pos, self.end, self.color, self.width, self.offset)
