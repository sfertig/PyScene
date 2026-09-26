from src import *
import pygame


Game.init(640, 360, "Test - 01", "darkblue", fullscreen=True)

class Player(GameObj):
    def __init__(self):
        super().__init__(Vector2D(100, 100), 0)
        self.rect = pygame.Rect((0, 0), (40, 40))

    def update(self, dt, events):
        self.pos += (Keys.get_vector(Keys.left, Keys.right, Keys.up, Keys.down)*200)*Game.dt
        self.rect.topleft = self.pos.to_int()

    def render(self, cam):
        cam.draw_rect(self.rect, "lightblue")


Player()
Rect(100, 100, 40, 40, "green", 0)
Circle(100, 100, 20, "yellow", 1)
Line(100, 100, 140, 140, "red", 2)
while True:
    if Keys.is_pressed(Keys.escape): Game.quit()
    Game.cam.pos += (Keys.get_vector(Keys.a, Keys.d, Keys.w, Keys.s)*200)*Game.dt
    Game.Tick()

"""Rect(100, 100, 40, 40, "yellow", 1)
Rect(140, 100, 40, 40, "yellow", -1)

class GameTest1(Scene):
    def __init__(self):
        super().__init__("test")
        self.rect = Rect(0, 0, 10, 10, "green", 0)

    def update(self, dt, events):        
        self.rect.pos += (Keys.get_vector(Keys.a, Keys.d, Keys.w, Keys.s)*200)*Game.dt

frame = True
GameTest1()
while True:
    if Keys.is_pressed(Keys.escape): Game.quit()
    Game.Tick()"""

