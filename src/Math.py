import pygame

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def to_int(self): return (int(self.x), int(self.y))
    def to_tuple(self): return (tuple(self.x), tuple(self.y))
    def copy(self): return Vector2D(self.x, self.y)
    def int(self):
        self.x = int(self.x)
        self.y = int(self.y)

    def length(self):
        return (self.x**2 + self.y**2)**0.5

    def normalize(self):
        length = self.length()
        self.x /= length
        self.y /= length
        return self

    def __add__(self, other):
        if type(other) == Vector2D:
            return Vector2D(self.x + other.x, self.y + other.y)
        else:
            return Vector2D(self.x + other, self.y + other)

    def __sub__(self, other):
        if type(other) == Vector2D:
            return Vector2D(self.x - other.x, self.y - other.y)
        else:
            return Vector2D(self.x - other, self.y - other)

    def __mul__(self, other):
        if type(other) == Vector2D:
            return Vector2D(self.x * other.x, self.y * other.y)
        else:
            return Vector2D(self.x * other, self.y * other)

    def __truediv__(self, other):
        if type(other) == Vector2D:
            return Vector2D(self.x / other.x, self.y / other.y)
        else:
            return Vector2D(self.x / other, self.y / other)

def clamp(value, min, max):
    if value < min: return min
    if value > max: return max
    return value

def handle_collision(self, rects, Net) -> dict: #mey replace in near future
    """self must have a rect() method"""
    returns = {"on_floor": False, "on_wall": False}

    # 1. Horizontal Collisions
    self.pos.x += self.vel.x * Net.dt
    player_rect = self.rect()
    for rect in rects:
        if player_rect.colliderect(rect):
            returns["on_wall"] = True
            self.pos.x -= self.vel.x * Net.dt
            self.vel.x = 0
            break 

    # 2. Vertical Collisions
    self.pos.y += self.vel.y * Net.dt
    player_rect = self.rect() 
    for rect in rects:
        if player_rect.colliderect(rect):
            # Step back first
            self.pos.y -= self.vel.y * Net.dt

            if self.vel.y > 0 and player_rect.bottom >= rect.top and player_rect.top < rect.top:
                returns["on_floor"] = True
                
            self.vel.y = 0
            break

    return returns

