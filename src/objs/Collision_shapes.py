import pygame
from ..Game import Game, handle_collision
from ..Math import Vector2D
from .GameObj import GameObj

class StaticCollisionRect:
    def __init__(self, x, y, w, h, active=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.active = active

        Game._update_coll = True
        Game._queue_add_coll(self)

    def set_active(self, active=True):
        self.active = active
        Game._update_coll = True
    def destroy(self):
        Game._queue_remove_coll(self)

class DynamicCollisionRect:
    def __init__(self, x, y, w, h, active=True):
        self.pos = Vector2D(x, y)
        self.dim = Vector2D(w, h)
        self.active = active
        self.vel = Vector2D(0.0, 0.0)
        self.rect = pygame.Rect(x, y, w, h)

        Game._update_coll = True
        Game._queue_add_D_coll(self)

    def update(self):
        if self.vel.to_int != (0.0, 0.0): Game._update_coll = True
        #print(self.active, len(Game.collisions), self.vel.x)
        handle_collision(self, self.dim, self.rect)
        self.rect.topleft = self.pos.to_int()

    def set_active(self, active=True):
        self.active = active
        Game._update_coll = True
    def destroy(self):
        Game._queue_remove_D_coll(self)