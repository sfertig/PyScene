import pygame

from ..Math import Vector2D


class SubScreen:
    def __init__(self, x, y, w, h, bgColor: None, displaySurface: pygame.Surface = None, parent=None):
        self.pos = Vector2D(x, y)
        self.dim = Vector2D(w, h)
        self.color = bgColor
        self._screen = displaySurface
        self.parent = parent  # Reference to parent SubScreen
        if self.color == None: self.screen = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
        else: self.screen = pygame.Surface((w, h)).convert()

    def clear(self):
        if self.color == None: self.screen.fill((0, 0, 0, 0))
        else: self.screen.fill(self.color)

    def get_absolute_pos(self):
        """Recursively calculates the true global screen position."""
        if self.parent:
            return self.pos + self.parent.get_absolute_pos()
        return self.pos

    def local_mouse_pos(self, cam: Vector2D = Vector2D(0, 0)):
        # Uses absolute position so nested screens correctly account for parent offsets
        return Vector2D(*pygame.mouse.get_pos()) - (self.get_absolute_pos() - cam)

    def get_global_rect(self, rect):
        # Uses absolute position so hitboxes align on screen regardless of nesting level
        abs_pos = self.get_absolute_pos()
        return pygame.Rect((abs_pos.x + rect.x, abs_pos.y + rect.y), rect.size)

    def render(self, cam: Vector2D = Vector2D(0, 0)):
        self._screen.blit(self.screen, (self.pos - cam).to_int())