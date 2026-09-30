import pygame

#collisions generators

def _coll_gen_combination(Game): #this functions as the main function for collisions rect generation
    if not Game._update_coll: return
    # -- else start collisions generation -- #
    Game.collisions.clear() #clear existing rects

    #get rects
    rects: list[pygame.Rect] = []
    for col in Game.col: rects.append(col.rect.copy())

    #set collisions
    Game.collisions = rects

    #add dynamic rects
    for col in Game.dynamic_col: 
        if col.active: rects.append(col.rect)

    Game._update_coll = False



    


    


