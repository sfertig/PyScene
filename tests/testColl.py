from src import *
import pygame

Game.init(640, 360, "Test - 02: Collisions", "black")
Game.show_collisions = True
Game.optimize_static_colliders = True

class Player(GameObj):
    def __init__(self):
        super().__init__(Vector2D(200, 0))
        self.coll = DynamicCollisionRect(*self.pos.to_int(), 25, 25)

    def update(self):
        self.coll.vel = Keys.get_vector(Keys.a, Keys.d, Keys.w, Keys.s, False)*150

class TestDynamic(GameObj):
    def __init__(self):
        super().__init__(Vector2D(0, 0), 5)
        self.coll = DynamicCollisionRect(100, 100, 20, 40, True)
        self.coll.vel.x = 100
        self.vel.x = 100
        self.timer = 0.0

    def update(self):
        self.timer += Game.dt
        if self.timer >= 3.0: 
            self.vel.x *= -1
            self.timer = 0.0
        self.coll.vel = self.vel.copy()

StaticCollisionRect(0, 0, 50, 100, True)
StaticCollisionRect(0, 100, 50, 50, True)
StaticCollisionRect(250, 100, 50, 50, True)
StaticCollisionRect(300, 100, 50, 50, True)
TestDynamic()

Player()
Game.Run(True)

