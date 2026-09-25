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

            #game obj info
            self.objects = []
            self.queue_creation = []
            self.queue_del = []

            self.id = 0

    def _queue_add(self, obj): self.queue_creation.append(obj)
    def _queue_remove(self, obj): self.queue_del.append(obj)
    def _get_id(self):
        self.id += 1
        return self.id

    def __handle_queue(self):
        for obj in self.queue_creation: self.objects.append(obj)
        for obj in self.queue_del: self.objects.remove(obj)
        self.queue_creation = []
        self.queue_del = []

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
        self.__handle_queue()

        #update objs
        for obj in self.objects: obj.update(self.dt, self.events)

        if _clear: self.clear_screen() #used if user is drawing objects themselves
        

    def clear_screen(self): self.screen.fill(self.bg)

    def render(self, _clear=True):
        if not self.__on: return

        if _clear: self.screen.fill(self.bg)
        #render call
        for obj in self.objects: obj.render(None)
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
