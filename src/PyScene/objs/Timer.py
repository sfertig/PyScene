from .GameObj import GameObj
from ..Game import Game
from ..Math import Vector2D

class Timer(GameObj):
    def __init__(self, duration, active=True, Global=False):
        super().__init__(Vector2D(0, 0), 0, active, True, Global)
        self.duration = duration
        self.elapsed = 0.0
        self.running = False
        self.start()

    def start(self):
        self.elapsed = 0
        self.running = True

    def stop(self):
        self.running = False

    def get_time(self):
        return self.elapsed

    def update(self, dt):
        if not self.active: return
        if self.running:
            self.elapsed += dt
            if self.elapsed >= self.duration:
                self.running = False
                return True
        return False

    def is_done(self):
        return not self.running and self.elapsed >= self.duration