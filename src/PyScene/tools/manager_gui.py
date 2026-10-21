import pygame
import os

from ..Game import Game, Scene
from ..utils import SubScreen
from ..Math import Vector2D
from ..Keys import Keys
from ..objs import *

class GUI(Scene):
    def __init__(self):
        super().__init__("GUI")
        Text(pygame.font.Font(None, 25), "PyScene Tilemaps:", (141, 144, 148), Vector2D(10, 10), "topleft", 1)
        Rect(Game.width-200, 35, 190, Game.height-40, (35, 35, 35), 0, 5)
        Text(pygame.font.Font(None, 25), "Tilemap Options:", (141, 144, 148), Vector2D(Game.width-200, 10), "topleft", 1)
        FileWin()


class ManagerGUI:
    def __init__(self):
        Game.init(640, 360, "PyScene Tilemap Manager GUI", (53, 56, 59))
        GUI()
        Game.Run()

class FileWin(GameObj):
    def __init__(self):
        super().__init__(Vector2D(10, 35), 1)
        self.subscreen = SubScreen(10, 35, 200, Game.height-40, (35, 35, 35), Game.screen)
        self.screen = self.subscreen.screen

        self.files: list[FileDefined] = []
        self.__load()

    def __load(self):
        y = 10
        #scan the files in .pyscene/tilemaps
        for file in os.listdir(".pyscene/tilemaps"):
            name = file.split(".")[0]
            self.files.append(FileDefined(y, name))
            y += self.files[-1].rect.height+5

    def update(self):
        for file in self.files:
            file.update(self.subscreen)
        #using mouse wheel to scroll through files, or arrow keys
        change = 0
        for event in Game.events:
            if event.type == pygame.MOUSEWHEEL: change = event.y
        if Keys.is_held(Keys.down): change = 1
        elif Keys.is_held(Keys.up): change = -1
        change*=5
        if change != 0:
            for file in self.files:
                file.move_y(change)


    def render(self):
        self.subscreen.clear()
        for file in self.files:
            file.render(self.subscreen.screen)
        self.subscreen.render()

class FileDefined():
    def __init__(self, y, name, w=150, h=30):
        self.pos = Vector2D(25, y)
        self.name = name
        self.rect = pygame.Rect(self.pos.x, self.pos.y, w, h)
        self.text = Text(pygame.font.Font(None, 25), self.name, (141, 144, 148), Vector2D(self.rect.centerx, self.rect.centery), "center", 1, visible=False)
        self.w = 3
        self.hovered = False
        self.selected = False

        self.options: FileOptions = None

    def move_y(self, addition):
        self.pos.y += addition
        self.rect.y += addition
        self.text.set_pos(Vector2D(self.text.pos.x, self.text.pos.y+addition))

    def update(self, sub: SubScreen):
        if not self.selected:
            mpos = sub.local_mouse_pos().to_int()
            self.hovered = self.rect.collidepoint(mpos)
            if self.hovered: self.w = 5
            else: self.w = 3 
            if Game.click and self.hovered:
                self.selected = True
                self.w = 0
                self.options = FileOptions(self.name)
                return
        else: #selected
            if (Game.click and sub.screen.get_rect().collidepoint(pygame.mouse.get_pos())) or (Keys.is_pressed(Keys.escape) and self.options.renameWidth == 2):
                self.selected = False
                self.w = 3
                self.options._destroy()
                self.options = None
            else:
                if self.options.RENAME:
                    new = self.options.renameName.text
                    old = self.name
                    self.name = new
                    self.text.set_text(new)
                    self.options.RENAME = False
                    self.options.renameName.set_text("")
                    self.options.name.set_text(f"Name: {new}")
                    #rename file
                    os.rename(f".pyscene/tilemaps/{old}.json", f".pyscene/tilemaps/{new}.json")
                elif self.options.DUPE:
                    self.options.DUPE = False


    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect, self.w)
        self.text.render_to(screen)

class FileOptions(GameObj):
    def __init__(self, name):
        super().__init__(Vector2D(Game.width-200, 35), 1)
        self.sub = SubScreen(Game.width-200, 35, 190, Game.height-40, (35, 35, 35), Game.screen)

        #name text and details
        self.name = Text(pygame.font.Font(None, 25), f"Name: {name}", (141, 144, 148), Vector2D(5, 10), "topleft", 1, visible=False)
        self.line = Line(5, 30, self.sub.screen.get_rect().width-10, 30, (0, 0, 0), 1, visible=False)
        #rename
        self.renameText = Text(pygame.font.Font(None, 25), "Rename:", (141, 144, 148), Vector2D(5, 40), "topleft", 1, visible=False)
        self.renameRect = pygame.Rect(10, 60, self.sub.screen.get_rect().width-20, 30)
        self.renameWidth = 2
        self.renameName = Text(pygame.font.Font(None, 25), "", (141, 144, 148), Vector2D(self.renameRect.centerx, self.renameRect.centery), "center", 1, visible=False)
        self.RENAME = False
        self.renameLine = Line(5, 100, self.sub.screen.get_rect().width-10, 100, (0, 0, 0), 1, visible=False)
        #dupe
        self.dupeRect = pygame.Rect(10, 110, self.sub.screen.get_rect().width-20, 30)
        self.dupeWidth = 2
        self.dupeText = Text(pygame.font.Font(None, 25), "Duplicate", (141, 144, 148), Vector2D(self.dupeRect.centerx, self.dupeRect.centery), "center", 1, visible=False)
        self.DUPE = False

    def update(self):
        #rename
        if Game.click:
            mpos = self.sub.local_mouse_pos().to_int()
            if self.renameRect.collidepoint(mpos):
                self.renameWidth = 5
            else:
                self.renameWidth = 2
        elif Keys.is_pressed(Keys.escape):
            if self.renameWidth == 5:
                self.renameWidth = 2
        if self.renameWidth == 5:
            text = self.renameName.text
            done = False
            for event in Game.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(text) > 0: done = True
                    else:
                        if len(text) > 15: continue
                        text += event.unicode
            self.renameName.set_text(text)
            if done: self.RENAME = True
        #dupe
        mpos = self.sub.local_mouse_pos().to_int()
        if self.dupeRect.collidepoint(mpos):
            self.dupeWidth = 5
        else:
            self.dupeWidth = 2
        if self.dupeWidth == 5 and Game.click:
            self.DUPE = True

    def render(self):
        self.sub.clear()

        self.name.render_to(self.sub.screen)
        self.line.render_to(self.sub.screen)

        self.renameText.render_to(self.sub.screen)
        pygame.draw.rect(self.sub.screen, (0, 0, 0), self.renameRect, self.renameWidth)
        self.renameName.render_to(self.sub.screen)
        self.renameLine.render_to(self.sub.screen)

        pygame.draw.rect(self.sub.screen, (0, 0, 0), self.dupeRect, self.dupeWidth)
        self.dupeText.render_to(self.sub.screen)

        self.sub.render()

    def _destroy(self): #destroys self and all objects used
        self.destroy()
        self.name.destroy()
        self.line.destroy()
        self.renameText.destroy()



