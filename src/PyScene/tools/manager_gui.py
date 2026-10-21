import pygame

from ..Game import Game
from ..utils import SubScreen

class ManagerGUI:
    def __init__(self):
        Game.init(640, 360, "PyScene Tilemap Manager GUI", "darkblue")
        Game.Run(True)

