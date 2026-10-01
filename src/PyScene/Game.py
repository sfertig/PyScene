import pygame
import sys

from .Keys import Keys
from .Math import Vector2D
from .Collisions import _coll_gen_combination

class _game:
    def __init__(self):
        self.__on = False
        pygame.init()
        pygame.font.init()

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
        self.cam = Camera(self)

        self.show_collisions: bool = False
        self.optimize_static_colliders: bool = False

        #screen
        if not fullscreen: self.screen = pygame.display.set_mode((self.width, self.height))
        else: self.screen = pygame.display.set_mode((width, height), pygame.SCALED | pygame.FULLSCREEN)
        pygame.display.set_caption(self.title)

        Keys._add_net(self) #to accsess events

        #game obj info
        self.objects = []
        self.queue_creation = []
        self.queue_del = []

        self.collisions: list[pygame.Rect] = [] #accual list of rects
        self.col = []
        self.queue_creation_coll = []
        self.queue_del_coll = []
        self._update_coll = False

        self.dynamic_col = []
        self.queue_creation_D_coll = []
        self.queue_del_D_coll = []

        self.render_queue = []

        self.active_scene = None
        self.scenes = {}
        self.id = 0


    def _queue_add(self, obj): 
        if self.active_scene is None: self.queue_creation.append(obj)
        else: self.active_scene._queue_add(obj)
    def _queue_remove(self, obj): 
        if obj in self.objects: self.objects.remove(obj)
        else: self.active_scene._queue_remove(obj)
    def _get_id(self):
        self.id += 1
        return self.id

    def _queue_add_coll(self, obj): self.queue_creation_coll.append(obj)
    def _queue_remove_coll(self, obj): self.queue_del_coll.append(obj)
    def _queue_add_D_coll(self, obj): self.queue_creation_D_coll.append(obj)
    def _queue_remove_D_coll(self, obj): self.queue_del_D_coll.append(obj)

    def __update_render_queue(self): #update order of the renders based on z-index
        self.render_queue = sorted(self.objects, key=lambda obj: obj.z_index)

    def __handle_queue(self):
        for obj in self.queue_creation: self.objects.append(obj)
        for obj in self.queue_del: self.objects.remove(obj)
        if len(self.queue_creation) > 0 or len(self.queue_del) > 0: self.__update_render_queue()
        self.queue_creation.clear()
        self.queue_del.clear()
        #collisions
        for obj in self.queue_creation_coll: self.col.append(obj)
        for obj in self.queue_del_coll: self.col.remove(obj)
        self.queue_creation_coll.clear()
        self.queue_del_coll.clear()
        for obj in self.queue_creation_D_coll: self.dynamic_col.append(obj)
        for obj in self.queue_del_D_coll: self.dynamic_col.remove(obj)
        self.queue_creation_D_coll.clear()
        self.queue_del_D_coll.clear()
        _coll_gen_combination(self)
        self._update_coll = False

    def __update(self):
        self.click = False
        self.dt = self.clock.tick(self.fps)/1000.0
        self.events = pygame.event.get()

        for obj in self.dynamic_col: obj.update()
        
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
        for obj in self.objects: obj.update()
        #update scene
        if self.active_scene is not None: 
            self.active_scene.update()
            self.active_scene._update()

        if _clear: self.clear_screen() #used if user is drawing objects themselves
        

    def clear_screen(self): self.screen.fill(self.bg)

    def render(self, _clear=True):
        if not self.__on: return

        if _clear: self.screen.fill(self.bg)
        #render call
        if self.active_scene is None: 
            for obj in self.render_queue: obj.render(self.cam)
        #render scene
        else: 
            self.active_scene.render(self.cam)
            self.active_scene._render(self.cam)
        if self.show_collisions: self.__render_collisions()
        #update screen
        pygame.display.flip()

    def __render_collisions(self):
        for coll in self.collisions:
            pygame.draw.rect(self.screen, "yellow", coll, 2)

    def quit(self):
        self.__on = False
        pygame.quit()
        sys.exit()

    def set_title(self, title):
        self.title = title
        pygame.display.set_caption(self.title)

    def Tick(self):
        self.update()
        self.render()
    def Run(self, _esc=False):
        while True:
            self.Tick()
            if _esc and Keys.is_pressed(pygame.K_ESCAPE): self.quit()
    def full_reset(self):
        self.objects = []
        self.queue_creation = []
        self.queue_del = []
        self.render_queue = []
        self.scenes = {}
        self.id = 0
        self.active_scene = None
        self._clear_all_collisions_()
    def _clear_all_collisions_(self):
        self.collisions = []
        self.col = []
        self.queue_creation_coll = []
        self.queue_del_coll = []
        self._update_coll = False

    def set_scene(self, scene=None):
        if self.active_scene is not None: self.active_scene.destroy()
        self._clear_all_collisions_()
        self.active_scene = self.scenes.get(scene, None)
        if self.active_scene: self.active_scene.on_change()


class Scene:
    def __init__(self, name):
        self.name = name
        Game.scenes[name] = self
        self._objects = []
        self._render_queue = []
        self.queue_creation = []
        self.queue_del = []
        Game.scenes[name] = self

    def on_change(self): pass

    def update(self): pass #user defined
    def _update(self): #built in method
        self.__handle_queue()
        for obj in self._objects: obj.update()

    def render(self, cam): pass #user defined
    def _render(self, cam): #built in method
        #update render queue based on global objects
        _length = len(self._objects)+len(Game.objects)
        if _length != len(self._render_queue): self.__update_render_queue()
        #render
        for obj in self._render_queue: obj.render(cam)

    def _queue_add(self, obj): self.queue_creation.append(obj)
    def _queue_remove(self, obj): self.queue_del.append(obj)
    def __update_render_queue(self):
        objs = self._objects + Game.objects
        self._render_queue = sorted(objs, key=lambda obj: obj.z_index)
    def __handle_queue(self):
        for obj in self.queue_creation: self._objects.append(obj)
        for obj in self.queue_del: self._objects.remove(obj)
        if len(self.queue_creation) > 0 or len(self.queue_del) > 0: self.__update_render_queue()
        self.queue_creation = []
        self.queue_del = []

    def destroy(self):
        for obj in self._objects: obj.destroy()
        self._objects = []
        self._render_queue = []
        self.queue_creation = []
        self.queue_del = []

Game: _game = _game()

class Camera:
    def __init__(self, game):
        self.pos = Vector2D(0, 0)
        self.game = game

    #rendering helpers
    def draw_rect(self, rect, color, width=0, offset=True):
        r = rect.copy()
        if offset: r.topleft = (r.x - self.pos.x, r.y - self.pos.y)
        pygame.draw.rect(self.game.screen, color, r, width)
    def draw_circle(self, pos, r, color, width=0, offset=True):
        p = pos.copy()
        if offset: p -= self.pos
        pygame.draw.circle(self.game.screen, color, p.to_int(), r, width)
    def draw_line(self, start, end, color, width=1, offset=True):
        s = start.copy()
        e = end.copy()
        if offset:
            s -= self.pos
            e -= self.pos
        pygame.draw.line(self.game.screen, color, s.to_int(), e.to_int(), width)
    def draw_text(self, surface, rect, offset=True):
        r = rect.copy()
        if offset: r.topleft = (r.x - self.pos.x, r.y - self.pos.y)
        self.game.screen.blit(surface, r)
    def draw_image(self, image, pos, offset=True):
        p = pos.copy()
        if offset: p -= self.pos
        self.game.screen.blit(image, p.to_int())

def handle_collision(self, dim: Vector2D, Rect=None, ignore_self=True) -> dict:
    returns = {"on_floor": False, "on_wall": False}

    # 1. Horizontal Collisions
    self.pos.x += self.vel.x * Game.dt
    player_rect = pygame.Rect(self.pos.to_int(), dim.to_int())
    for rect in Game.collisions:
        if ignore_self and Rect is not None: 
            if rect == Rect: continue
        if player_rect.colliderect(rect):
            returns["on_wall"] = True
            self.pos.x -= self.vel.x * Game.dt
            self.vel.x = 0
            break 

    # 2. Vertical Collisions
    self.pos.y += self.vel.y * Game.dt
    player_rect = pygame.Rect(self.pos.to_int(), dim.to_int())
    for rect in Game.collisions:
        if ignore_self and Rect is not None: 
            if rect == Rect: continue
        if player_rect.colliderect(rect):
            # Step back first
            self.pos.y -= self.vel.y * Game.dt

            if self.vel.y > 0 and player_rect.bottom >= rect.top and player_rect.top < rect.top:
                returns["on_floor"] = True
                
            self.vel.y = 0
            break

    return returns

