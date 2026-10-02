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
        self.surface = self.font.render(str(self.text), False, self.color)  # False for sharp pixel fonts!
        # Dynamically set rect based on alignment (topleft, center, topright, etc.)
        self.rect = self.surface.get_rect(**{self.align: self.pos.to_int()})

    def set_text(self, new_text, color=None):
        """Only call this when the string actually changes!"""
        if color is not None:
            self.color = color
        if new_text != self.text:
            self.text = new_text
            self._update_surface()

    def set_pos(self, new_pos):
        self.pos = new_pos
        self.rect = self.surface.get_rect(**{self.align: self.pos})

    def render(self):
        if not self.visible: return
        Game.cam.draw_text(self.surface, self.rect, self.offset)

class Image(GameObj):
    def __init__(self, image, pos=Vector2D(0, 0), z_index=0, active=True, visible=True, offset=True, Global=False):
        super().__init__(pos, z_index, active, visible, Global)
        self.image = image
        self.offset = offset

    def render(self):
        if not self.visible: return
        Game.cam.draw_image(self.image, self.pos, self.offset)

