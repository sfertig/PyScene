import pygame
from ..Math import Vector2D
from ..Game import Game

class GameObj: #this will be the base class of every game obj
    def __init__(self, pos, z_index, active=True, visible=True):
        self.pos: Vector2D = pos
        self.z_index = z_index
        self.active = active
        self.visible = visible
        self._id = Game._get_id()

        #add to creation
        Game._queue_add(self)

    def update(self, dt, events): pass
    def render(self, cam): pass
    def destroy(self): Game._queue_remove(self)

class Rect(GameObj): #test rect object
    def __init__(self, x, y, w, h, color, z_index=0, width=0, active=True, visible=True, offset=True):
        super().__init__(Vector2D(x, y), z_index, active, visible)
        self.dim = Vector2D(w, h)
        self.color = color
        self.rect = pygame.Rect((x, y), (w, h))
        self.offset = offset
        self.width = width

    def update(self, dt, events):
        if self.pos.to_int() != self.rect.topleft: self.rect.topleft = self.pos.to_int()

    def render(self, cam):
        cam.draw_rect(self.rect, self.color, self.width, self.offset)
