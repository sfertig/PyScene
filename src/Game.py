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

            self.render_queue = []

            self.active_scene = None
            self.scenes = {}
            self.id = 0

    def _queue_add(self, obj): 
        if self.active_scene is None: self.queue_creation.append(obj)
        else: self.active_scene._queue_add(obj)
    def _queue_remove(self, obj): 
        if self.active_scene is None: self.queue_del.append(obj)
        else: self.active_scene._queue_remove(obj)
    def _get_id(self):
        self.id += 1
        return self.id

    def __update_render_queue(self): #update order of the renders based on z-index
        self.render_queue = sorted(self.objects, key=lambda obj: obj.z_index)

    def __handle_queue(self):
        for obj in self.queue_creation: self.objects.append(obj)
        for obj in self.queue_del: self.objects.remove(obj)
        if len(self.queue_creation) > 0 or len(self.queue_del) > 0: self.__update_render_queue()
        self.queue_creation = []
        self.queue_del = []

    def __update(self):
        self._obj_changed_layer = False
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
        #update scene
        if self.active_scene is not None: 
            self.active_scene.update(self.dt, self.events)
            self.active_scene._update(self.dt, self.events)

        if _clear: self.clear_screen() #used if user is drawing objects themselves
        

    def clear_screen(self): self.screen.fill(self.bg)

    def render(self, _clear=True):
        if not self.__on: return

        if _clear: self.screen.fill(self.bg)
        #render call
        for obj in self.render_queue: obj.render(None)
        #render scene
        if self.active_scene is not None: 
            self.active_scene.render(None)
            self.active_scene._render(None)
        #update screen
        pygame.display.flip()

    def quit(self):
        self.__on = False
        pygame.quit()
        sys.exit()

    def set_title(self, title):
        self.title = title
        pygame.display.set_caption(self.title)

    def set_scene(self, scene=None):
        self.active_scene = self.scenes.get(scene, None)
        if self.active_scene: self.active_scene.on_change()


class Scene:
    def __init__(self, name):
        self.name = name
        Game.scenes[name] = self
        self._objects = []
        self._queue_creation = []
        self._queue_del = []
        self._render_queue = []
        self.queue_creation = []
        self.queue_del = []

    def on_change(self): pass

    def update(self, dt, events): pass #user defined
    def _update(self, dt, events): #built in method
        self.__handle_queue()
        self._obj_changed_layer = False
        for obj in self._objects: obj.update(dt, events)

    def render(self, cam): pass #user defined
    def _render(self, cam): #built in method
        for obj in self._render_queue: obj.render(cam)

    def _queue_add(self, obj): self.queue_creation.append(obj)
    def _queue_remove(self, obj): self.queue_del.append(obj)
    def __update_render_queue(self): #update order of the renders based on z-index
        self.render_queue = sorted(self.objects, key=lambda obj: obj.z_index)
    def __handle_queue(self):
        for obj in self.queue_creation: self.objects.append(obj)
        for obj in self.queue_del: self.objects.remove(obj)
        if len(self.queue_creation) > 0 or len(self.queue_del) > 0: self.__update_render_queue()
        self.queue_creation = []
        self.queue_del = []

Game: _game = _game()

