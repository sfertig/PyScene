import pygame
from ..Math import Vector2D
from ..Game import Game

class GameObj: #this will be the base class of every game obj
    def __init__(self, pos, z_index=0, active=True, visible=True, Global=False):
        self.pos: Vector2D = pos
        self.vel: Vector2D = Vector2D(0, 0)
        self.z_index = z_index
        self.active = active
        self.visible = visible
        self._id = Game._get_id()

        #add to creation
        if not Global: Game._queue_add(self)
        else: Game.queue_creation.append(self) #if obj is just global anyway

        self._global = Global

    def update(self): pass
    def render(self): pass
    def destroy(self): Game._queue_remove(self)

