from src.PyScene import *

Game.init(640, 360, "Test - 01", "darkblue", application=True) #init game with width, height, title, background color and application mode


Game.Run(True) #or you can have a manual game loop with Game.Tick or using Game.update and Game.render
#Also passing true will make the window close if ascape is presed