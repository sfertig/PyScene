from ..Game import Game
import pygame
from .GameObj import GameObj
from ..Math import Vector2D
from ..utils import SubScreen

class Tilemap(GameObj):
    def __init__(self, tileset, size=16, z_index=0, active=True, visible=True, Global=False ):
        super().__init__(Vector2D(0, 0), z_index, active, visible, Global)
        self.tileset: dict[tuple[int, int], pygame.surface.Surface] = tileset
        self.size: int = size

        self.tilemap: dict[tuple[int, int], tuple[int, int]] = {}
        self._cache_map: dict[tuple[int, int], tuple[int, int]] = {}

        self.subscreen = SubScreen(0, 0, Game.width, Game.height, displaySurface=Game.screen)
        self.screen = self.subscreen.screen

    def update(self):
        if not self.tilemap:
            return
        #determine if we need to re-render tilemap
        if self.tilemap==self._cache_map: return
        self._cache_map = self.tilemap.copy()

        #else update
        min_x = min(pos[0] for pos in self.tilemap.keys())
        max_x = max(pos[0] for pos in self.tilemap.keys())
        min_y = min(pos[1] for pos in self.tilemap.keys())
        max_y = max(pos[1] for pos in self.tilemap.keys())

        # 1. Determine dimensions (+1 to include the max tile itself)
        width = (max_x - min_x + 1) * self.size
        height = (max_y - min_y + 1) * self.size

        self.pos.x = min_x * self.size
        self.pos.y = min_y * self.size

        # 2. Create the SubScreen matching this exact bounding box
        # Note: Position this subscreen in world space using (min_x * self.size, min_y * self.size)
        self.subscreen = SubScreen(min_x * self.size, min_y * self.size, width, height, displaySurface=Game.screen)
        self.subscreen.clear()
        self.screen = self.subscreen.screen

        # 3. Bake the tiles by offsetting negative/arbitrary coords to (0, 0)

        for (tile_x, tile_y), tile_id in self.tilemap.items():
            # Shift coordinates so min_x/min_y lands at local pixel (0, 0)
            local_x = (tile_x - min_x) * self.size
            local_y = (tile_y - min_y) * self.size
            
            self.screen.blit(self.tileset[tile_id], (local_x, local_y))

    def render(self):
        Game.screen.blit(self.screen, (self.pos-Game.cam.pos).to_int())

