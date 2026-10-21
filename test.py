from src.PyScene import *
import pygame


Game.init(640, 360, "Test - 01", "darkblue", fullscreen=False)

class Player(GameObj):
    def __init__(self):
        super().__init__(Vector2D(0, 0), 0)
        self.rect = Rect(0, 0, 16, 16, "green")

    def update(self):
        self.vel = (Keys.get_vector(Keys.a, Keys.d, Keys.w, Keys.s, False)*150)*Game.dt
        self.pos += self.vel
        self.rect.pos = self.pos

Game.cam.pos.x = -Game.width/2
Game.cam.pos.y = -Game.height/2
Player()

Assets.new_tileset("tests/tileset.png", "tileset")
t = Tilemap(Assets.get_tileset("tileset"), 16, -1)

t.tilemap[(0, 0)] = (1, 0)
t.tilemap[(0, 1)] = (1, 1)

Game.Run(True)
