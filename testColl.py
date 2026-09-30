from src import *
import pygame

Game.init(640, 360, "Test - 02: Collisions", "black")

class Player(GameObj):
    def __init__(self):
        super().__init__(Vector2D(100, 100))
        self.rect = Rect(0, 0, 25, 25, "green")

    def update(self):
        self.vel = Keys.get_vector(Keys.a, Keys.d, Keys.w, Keys.s, False)*150
        handle_collision(self, Vector2D(25, 25))
        self.rect.pos = self.pos

Rect(0, 0, 50, 50, "red", 1)
StaticCollisionRect(0, 0, 50, 50, True)


Player()
Game.Run(True)

