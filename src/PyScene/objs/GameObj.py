import pygame
from ..Math import Vector2D
from ..Game import Game

class GameObj: #this will be the base class of every game obj
    def __init__(self, pos=Vector2D(0, 0), z_index=0, active=True, visible=True, Global=False):
        self.pos: Vector2D = pos
        self.vel: Vector2D = Vector2D(0, 0)
        self.z_index = z_index
        self.active = active
        self.visible = visible
        self._id = Game._get_id()

        self.__parent: GameObj = None
        self.__children: list[GameObj] = []

        #add to creation
        if Game.always_global: Global = True
        if not Global: Game._queue_add(self)
        else: Game.queue_creation.append(self) #if obj is just global anyway

        self._global = Global

    def child(self, obj): #obj is a game object 
        self.__children.append(obj)
        obj.parent(self)
        return obj #QOF

    def parent(self, obj):
        # If we already have a parent, remove ourselves from its list first
        if self.__parent and self in self.__parent.__children:
            self.__parent.__children.remove(self)
        self.__parent = obj

    def update(self): pass
    def render(self): pass
    def destroy(self): 
        Game._queue_remove(self)
        for i in self.__children:
            i.destroy()

        if self.__parent: self.__parent.__children.remove(self)

        self.__children = []
        self.__parent = None

