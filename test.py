from src import *
import pygame
from random import randint as I

Game.init(640, 360, "Test - 01", "darkblue", fullscreen=False)

Rect(100, 100, 40, 40, "yellow", 1)
Rect(140, 100, 40, 40, "yellow", -1)

class GameTest1(Scene):
    def __init__(self):
        super().__init__("test")
        self.rect = Rect(0, 0, 10, 10, "green", 0)
        Game.bg = "darkblue"

    def update(self, dt, events):
        self.rect.pos += (Keys.get_vector(Keys.a, Keys.d, Keys.w, Keys.s)*200)*Game.dt

frame = True
GameTest1()
while True:
    if Keys.is_pressed(Keys.q): Game.quit()

    if Keys.is_pressed(Keys.up): GameTest1()

    Game.Tick()

