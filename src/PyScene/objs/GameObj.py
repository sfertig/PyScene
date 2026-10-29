import pygame
from ..Math import Vector2D
from ..Game import Game

class GameObj: #this will be the base class of every game obj
    def __init__(self, pos=Vector2D(0, 0), z_index=0, active=True, visible=True, Global=False):
        self.pos: Vector2D = pos
        self.vel: Vector2D = Vector2D(0, 0)
        self.z_index = z_index
        self._active = active
        self.visible = visible
        self._id = Game._get_id()

        self._parent: GameObj = None
        self._children: list[GameObj] = []

        #add to creation
        if Game.always_global: Global = True
        if not Global: Game._queue_add(self)
        else: Game.queue_creation.append(self) #if obj is just global anyway

        self._global = Global

    def child(self, obj): #obj is a game object 
        self._children.append(obj)
        obj.parent(self)
        return obj #QOF

    def parent(self, obj):
        # If we already have a parent, remove ourselves from its list first
        if self._parent and self in self._parent._children:
            self._parent._children.remove(self)
        self._parent = obj

    def update(self): pass
    def render(self): pass
    def destroy(self): 
        Game._queue_remove(self)
        for i in self._children:
            i.destroy()

        if self._parent: 
            if self in self._parent._children: self._parent._children.remove(self)

        self._children = []
        self._parent = None

