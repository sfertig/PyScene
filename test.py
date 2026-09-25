from src import *
import pygame

Game.init(640, 360, "Test - 01", "darkblue")

rect = pygame.Rect(100, 100, 100, 100)

while True:
    Game.update(True)

    if Keys.is_held(Keys.a): rect.x -= 5
    if Keys.is_held(Keys.d): rect.x += 5

    pygame.draw.rect(Game.screen, "red", rect)
    
    Game.render(False)