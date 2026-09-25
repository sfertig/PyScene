import pygame
import sys

from .Keys import Keys

class _game:
    def __init__(self):
        self.__on = False

    def init(self, width, height, title, bg="black", fps=60, fullscreen=False):
            self.__on = True
            self.width = width
            self.height = height
            self.title = title
            self.bg = bg
            self.fps = fps
            self.clock = pygame.time.Clock()
            self.dt = 0.0
            self.mouse_down = False
            self.click = False
            self.events = []
    
            #screen
            if not fullscreen: self.screen = pygame.display.set_mode((self.width, self.height))
            else: self.screen = pygame.display.set_mode((width, height), pygame.SCALED | pygame.FULLSCREEN)
            pygame.display.set_caption(self.title)

            Keys._add_net(self) #to accsess events

    def __update(self):
        self.click = False
        self.dt = self.clock.tick(self.fps)/1000.0
        self.events = pygame.event.get()
        
        for event in self.events:
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1: 
                    self.mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP and self.mouse_down: 
                if event.button == 1: 
                    self.mouse_down = False
                    self.click = True

    def update(self, _clear=True):
        if not self.__on: return
        self.__update()

        if _clear: self.clear_screen() #used if user is drawing objects themselves
        

    def clear_screen(self): self.screen.fill(self.bg)

    def render(self, _clear=True):
        if not self.__on: return

        if _clear: self.screen.fill(self.bg)
        #render call

        #update screen
        pygame.display.flip()

    def quit(self):
        self.__on = False
        pygame.quit()
        sys.exit()

    def set_title(self, title):
        self.title = title
        pygame.display.set_caption(self.title)


Game: _game = _game()
