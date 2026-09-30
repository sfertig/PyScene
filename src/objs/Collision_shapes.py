import pygame
from ..Game import Game

class StaticCollisionRect:
    def __init__(self, x, y, w, h, active=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.active = active

        self._update_coll = True
        Game._queue_add_coll(self)

    def set_active(self, active=True):
        self.active = active
        if not active: self._update_coll = True
    def destroy(self):
        Game._queue_remove_coll(self)