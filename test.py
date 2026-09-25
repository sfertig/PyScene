from src import *
import pygame
from random import randint as I

Game.init(640, 360, "Test - 01", "darkblue", fullscreen=True)

rect: Rect = Rect(0, 0, 10, 10, "green", 1)
Rect(100, 100, 50, 50, "red", 2)
Rect(150, 100, 50, 50, "yellow", 0)

while True:
    if Keys.is_pressed(pygame.K_ESCAPE): Game.quit()
    Game.update()
    rect.pos += (Keys.get_vector(Keys.a, Keys.d, Keys.w, Keys.s)*200)*Game.dt
    Game.render()