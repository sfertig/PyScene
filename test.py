from src import *
import pygame
from random import randint as I

Game.init(640, 360, "Test - 01", "darkblue", fullscreen=True)

class GameTest1(Scene):
    def __init__(self):
        super().__init__("test")
        self.rect = Rect(0, 0, 10, 10, "green", 0)

    def update(self, dt, events):
        if Keys.is_pressed(pygame.K_ESCAPE): Game.quit()
        self.rect.pos += (Keys.get_vector(Keys.a, Keys.d, Keys.w, Keys.s)*200)*Game.dt
class GameTest2(Scene):
    def __init__(self):
        super().__init__("test2")
        self.rect = Rect(0, 0, 10, 10, "red", 0)

    def update(self, dt, events):
        if Keys.is_pressed(pygame.K_ESCAPE): Game.quit()
        self.rect.pos += (Keys.get_vector(Keys.a, Keys.d, Keys.w, Keys.s)*200)*Game.dt

t1 = GameTest1()
t2 = GameTest2()

Game.set_scene("test")
frame = True
while True:
    if Keys.is_pressed(Keys.q): Game.quit()

    if Keys.is_pressed(Keys.left): Game.set_scene("test")
    elif Keys.is_pressed(Keys.right): Game.set_scene("test2")

    Game.update()
    Game.render()

    if frame:
        frame = False
        print(Game.objects)
        print(t1._objects)
        print(t2._objects)
