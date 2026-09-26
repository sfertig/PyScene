import pygame

from ..Math import Vector2D

class Animation:
    def __init__(self, image: pygame.Surface, size: int, fps: float, loop:bool=True):
        self.image = image
        self.size = size
        self.fps = fps
        self.images = []
        self.index = 0.0
        self.loop=loop
        self.done=False

        # Automatically calculate frames based on image width
        total_frames = image.get_width() // size

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

    def update(self, dt: float):
        if self.done:
            return

        self.index += self.fps * dt
        
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
        return Animation(self.image, self.size, self.fps, self.loop)

class AnimationManager:
    def __init__(self, animations: dict[str, Animation], current_anim=None):
        self.animations = animations
        self.current_anim = current_anim

    def new_anim(self, name, anim):
        self.animations[name] = anim

    def new_anim_set(self, anims: dict[str, Animation]):
        #add new anims to existing ones
        self.animations.update(anims)

    def flip_v(self):
        for name in self.animations:
            self.animations[name].flip_v()

    def flip_h(self):
        for name in self.animations:
            self.animations[name].flip_h()

    def change_anim(self, name):
        self.current_anim = name

    def update(self, dt: float):
        if self.current_anim is None and self.current_anim in self.animations:
            return
        self.animations[self.current_anim].update(dt)
    def get_image(self) -> pygame.Surface:
        if self.current_anim is None and self.current_anim in self.animations:
            return
        return self.animations[self.current_anim].get_image()
    def get_animation(self) -> Animation:
        if self.current_anim is None and self.current_anim in self.animations:
            return
        return self.animations[self.current_anim]