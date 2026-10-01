import pygame

class _net_:
    def __init__(self):
        self.screen: pygame.Surface = None
        self.dt: float = 0.0
        self.clock: pygame.time.Clock = None
        self.width, self.height = 0, 0
        self.fps = 0

        self.events = []
        self.click = False

    def _update(self):
        self.click = False
        self.dt = self.clock.tick(self.FPS)/1000.0
        self.events = pygame.event.get()
        
        for event in self.events:
            if event.type == pygame.QUIT:
                self.shut_down()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1: 
                    self.mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP and self.mouse_down: 
                if event.button == 1: 
                    self.mouse_down = False
                    self.click = True


Net = _net_()
