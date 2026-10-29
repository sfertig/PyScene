from src.PyScene import *

Game.init(640, 360, "Test - 01", "darkblue", fullscreen=False)

class Player(GameObj):
    def __init__(self, x, y):
        super().__init__(Vector2D(x, y)) #z index is 0 by default
        self.rect = self.child(Rect(0, 0, 16, 16, "green")) #if player is destroyed so will the rect

    def update(self):
        self.pos += (Keys.get_vector(Keys.a, Keys.d, Keys.w, Keys.s, False)*150)*Game.dt
        self.rect.pos = self.pos

        #if Keys.is_pressed(Keys.enter): self.destroy()

class GameScene(Scene):
    def __init__(self):
        super().__init__("main")
        Player(Game.width/2, Game.height/2) #this will live with scene, if scene changed player will be destroyed

#Player(200, 200) This would be a global object and live through scene changes 

GameScene() #calling this will create the scene and the super will set it as the current scene

Game.Run(True) #or you can have a manual game loop with Game.Tick or using Game.update and Game.render
#Also passing true will make the window close if ascape is presed