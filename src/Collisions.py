import pygame

#collisions generators

def _coll_gen_combination(Game): #this functions as the main function for collision rect generation
    if not Game._update_coll: return
    # -- else start collisions generation -- #
    Game.collisions.clear() #clear existing rects

    #get rects
    rects: list[pygame.Rect] = []
    for col in Game.col: rects.append(col.rect.copy())

    if Game.optimize_static_colliders: rects = _optimize_static_colliders(Game, rects)

    #set collisions
    Game.collisions = rects

    #add dynamic rects
    for col in Game.dynamic_col: 
        if col.active: rects.append(col.rect)

    Game._update_coll = False

def _optimize_static_colliders(Game, colliders: list[pygame.Rect]):
    if not colliders:
        return []

    rects = sorted([r.copy() for r in colliders], key=lambda r: (r.y, r.x))
    merged = []

    # 2. Horizontal Merge Pass
    while rects:
        current = rects.pop(0)
        i = 0
        while i < len(rects):
            other = rects[i]
            if current.top == other.top and current.height == other.height and current.right == other.x:
                current.width += other.width
                rects.pop(i)
            else:
                i += 1
        merged.append(current)

    # 3. Vertical Merge Pass
    final_rects = []
    merged = sorted(merged, key=lambda r: (r.x, r.y))
    while merged:
        current = merged.pop(0)
        i = 0
        while i < len(merged):
            other = merged[i]
            if current.left == other.left and current.width == other.width and current.bottom == other.y:
                current.height += other.height
                merged.pop(i)
            else:
                i += 1
        final_rects.append(current)

    return final_rects


