from src import *
import pygame
from random import randint as I
while True:
    Game.full_reset()
    Game.init(640, 360, "Floppy Bird", "darkblue")
    bird = Circle(100, 25, 10, "yellow", -1) #show behind pipes
    vel = 0
    top_pipes = [Rect(400, 0, 20, I(20, 100), "green"),Rect(600, 0, 20, I(20, 100), "green"),Rect(800, 0, 20, I(20, 100), "green"),Rect(1000, 0, 20, I(20, 100), "green"),]
    bottom_pipes = [Rect(400, Game.height-I(175, 225), 20, 225, "green"),Rect(600, Game.height-I(175, 225), 20, 225, "green"),Rect(800, Game.height-I(175, 225), 20, 225, "green"),Rect(1000, Game.height-I(175, 225), 20, 225, "green"),]
    text = Text(pygame.font.Font(None, 20), "Score: 0", "white", Vector2D(3, Game.height-20), "topleft", 100)
    score = 0
    added = False
    while True:
        bird.pos.y += vel*Game.dt
        if bird.pos.y < -10 or bird.pos.y > Game.height-10: break
        vel += 4
        if Keys.is_pressed(Keys.space): vel = -150
        for pipe in top_pipes: pipe.pos.x -= 100*Game.dt
        for pipe in bottom_pipes: pipe.pos.x -= 100*Game.dt
        #lose
        if top_pipes[0].rect.collidepoint(bird.pos.to_int()): break
        elif bottom_pipes[0].rect.collidepoint(bird.pos.to_int()): break
        elif top_pipes[0].pos.x <= bird.pos.x and not added: #score
            score+=1
            text.set_text(f"Score: {score}")
            added = True
        #resetting pipes
        if top_pipes[0].pos.x < -21:
            top_pipes[0].destroy()
            top_pipes.pop(0)
            top_pipes.append(Rect(top_pipes[-1].pos.x + 200, 0, 20, I(20, 100), "green"))
            bottom_pipes[0].destroy()
            bottom_pipes.pop(0)
            bottom_pipes.append(Rect(bottom_pipes[-1].pos.x + 200, Game.height-I(175, 225), 20, 225, "green"))
            added = False
        Game.Tick()
        if Keys.is_pressed(Keys.escape): Game.quit()