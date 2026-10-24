from ..Math import Vector2D
from ..Game import Game
from .GameObj import GameObj
import pygame

class Text(GameObj):
    def __init__(self, font, text, color, pos=Vector2D(0, 0), align="center", z_index=0, active=True, visible=True, offset=True, Global=False):
        super().__init__(pos, z_index, active, visible, Global)
        self.font = font
        self.text = text
        self.color = color
        self.align = align
        self.surface = None
        self.rect = None
        self.offset = offset

        self._update_surface()

    def _update_surface(self):
        """Internal method to re-render surface only when text changes."""
        self.surface = self.font.render(str(self.text), False, self.color)
        self._apply_alignment()

    def _apply_alignment(self):
        """Safely positions the rect based on single or multi-coordinate alignment."""
        xy = self.pos.to_int()  # Assuming this returns (x, y)
        
        # Group single-coordinate attributes by which axis they care about
        x_aligns = {"left", "right", "centerx", "x"}
        y_aligns = {"top", "bottom", "centery", "y"}

        if self.align in x_aligns:
            # Create a default rect at (0,0), then assign the specific X coordinate
            self.rect = self.surface.get_rect()
            setattr(self.rect, self.align, xy[0])
        elif self.align in y_aligns:
            # Create a default rect at (0,0), then assign the specific Y coordinate
            self.rect = self.surface.get_rect()
            setattr(self.rect, self.align, xy[1])
        else:
            # Multi-coordinate alignments (center, topleft, etc.) safely accept the full tuple
            self.rect = self.surface.get_rect(**{self.align: xy})

    def set_text(self, new_text, color=None):
        """Only call this when the string actually changes!"""
        if color is not None:
            self.color = color
        if new_text != self.text:
            self.text = new_text
            self._update_surface()

    def set_pos(self, new_pos: Vector2D):
        self.pos = new_pos
        self._apply_alignment()

    def render(self):
        Game.cam.draw_text(self.surface, self.rect, self.offset)
        
    def render_to(self, surface):
        surface.blit(self.surface, self.rect)


class Image(GameObj):
    def __init__(self, image, pos=Vector2D(0, 0), z_index=0, active=True, visible=True, offset=True, Global=False):
        super().__init__(pos, z_index, active, visible, Global)
        self.image = image
        self.offset = offset

    def render(self):
        Game.cam.draw_image(self.image, self.pos, self.offset)
    def render_to(self, surface):
        surface.blit(self.image, self.pos.to_int())

