import pygame

from ..Math import Vector2D
from .GameObj import GameObj
from ..Game import Game

class Animation(GameObj):
    def __init__(self, image, size, fps, loop=True, pos=Vector2D(0, 0), z_index=0, active=True, visible=True, offset=True, Global=False):
        super().__init__(pos, z_index, active, visible, Global)
        self.offset = offset
        self.image = image
        self.size = size
        self.fps = fps
        self.images = []
        self.index = 0.0
        self.loop=loop
        self.done=False

        # Automatically calculate frames based on image width
        total_frames = int(image.get_width() // size)

        img_rect = image.get_rect()
        
        for i in range(total_frames):
            # Slice each frame from the sheet
            frame_rect = pygame.Rect(i * size, 0, size, size)
            #checks
            #if frame_rect.height > img_rect.height: frame_rect.height = img_rect.height
            self.images.append(self.image.subsurface(frame_rect))

    def last_frame(self):
        return int(self.index) >= (len(self.images) - 1)
    def reset(self):
        self.index = 0
        self.done = False

    def update(self):
        if self.done:
            return

        self.index += self.fps * Game.dt
        
        if self.index >= len(self.images):
            if self.loop:
                # Wrap around using modulo so fractional progress carries over smoothly
                self.index %= len(self.images)
            else:
                # Clamp to the exact last frame index and mark as finished
                self.index = float(len(self.images) - 1)
                self.done = True

    def get_image(self):
        # Safe indexing guard
        idx = min(int(self.index), len(self.images) - 1)
        return self.images[idx]

    def flip_v(self):
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.flip(self.images[i], False, True)

    def flip_h(self):
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.flip(self.images[i], True, False)

    def copy(self):
        return Animation(self.image, self.size, self.fps, self.loop, self.pos, self.z_index, self.active, self.visible, self.offset, self._global)
    def render(self):
        if not self.visible: return
        Game.cam.draw_image(self.get_image(), self.pos, self.offset)

class AnimationManager(GameObj):
    def __init__(self, animations: dict[str, Animation], current_anim=None, z_index=0, active=True, visible=True, offset=True, Global=False):
        super().__init__(Vector2D(0, 0), z_index, active, visible, Global)
        self.animations = animations
        self.current_anim = current_anim

        for anim in self.animations.values():
            anim.destroy() #remove from global or scene calls

    def new_anim(self, name, anim):
        self.animations[name] = anim
        anim.destroy()

    def new_anim_set(self, anims: dict[str, Animation]):
        #add new anims to existing ones
        self.animations.update(anims)
        for anim in anims:
            anims[anim].destroy()

    def flip_v(self):
        for name in self.animations:
            self.animations[name].flip_v()

    def flip_h(self):
        for name in self.animations:
            self.animations[name].flip_h()

    def change_anim(self, name):
        self.current_anim = name

    def update(self):
        if self.current_anim is None and self.current_anim in self.animations:
            return
        self.animations[self.current_anim].update(Game.dt)
    def get_image(self) -> pygame.Surface:
        if self.current_anim is None and self.current_anim in self.animations:
            return
        return self.animations[self.current_anim].get_image()
    def get_animation(self) -> Animation:
        if self.current_anim is None and self.current_anim in self.animations:
            return
        return self.animations[self.current_anim]

    def render(self):
        if not self.visible: return
        self.get_animation().render()