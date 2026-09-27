from src import *
import pygame


Game.init(640, 360, "Test - 01", "darkblue", fullscreen=False)

class player(GameObj):
    def __init__(self):
        super().__init__(Vector2D(0, 0), 0)
        #create animation
        Assets.new_anim_nIMG("player", 8, 2, "tests/pause.png", (0, 0, 16, 8), colorKey=None, scale=3.0)
        self.anim = Assets.get_animation("player")

    def update(self, dt, events):
        self.pos += (Keys.get_vector(Keys.a, Keys.d, Keys.w, Keys.s, False)*150)*dt
        self.anim.pos = self.pos #positions stay linked

player()

Game.Run()

