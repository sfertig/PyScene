import pygame
import os

from ..Game import Game
from ..utils import SubScreen
from ..Math import Vector2D
from ..objs import *

class ManagerGUI:
    def __init__(self):
        Game.init(640, 360, "PyScene Tilemap Manager GUI", "darkgray")

        Text(pygame.font.Font(None, 30), "Tilemaps:", "black", Vector2D(5, 5), "topleft", 5)

        Rect(0, 40, 300, Game.height-40, "black", -1)

        self.files: list[FileDefined] = []

        self.__load()

        Game.Run(True)

    def __load(self):
        
        y = 50
        #scan the files in .pyscene/tilemaps
        for file in os.listdir(".pyscene/tilemaps"):
            name = file.split(".")[0]
            self.files.append(FileDefined(y, name))
            y += self.files[-1].rect.height+5

class FileDefined(GameObj):
    def __init__(self, y, name):
        super().__init__(Vector2D(10, y), 1)
        self.name = name
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 300-self.pos.x*2, 50)
        self.text = Text(pygame.font.Font(None, 25), self.name, "black", Vector2D(self.rect.centerx, self.rect.centery), "center", 1, visible=False)

    def update(self): pass

    def render(self):
        pygame.draw.rect(Game.screen, "gray", self.rect)
        self.text.render_to(Game.screen)


