from src import *
import pygame

Game.init(640, 360, "Test - 01", "darkblue")

rect = Rect(0, 0, 100, 100, "green")

while True:
    Game.update()
    rect.pos += (Keys.get_vector(Keys.a, Keys.d, Keys.w, Keys.s)*200)*Game.dt
    Game.render()