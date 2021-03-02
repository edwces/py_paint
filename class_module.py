#################################
# py_paint by edwces
# 2021
# Pixel painter program
#################################

import pygame as pg
from pygame.locals import *
from py_paint_settings import *
import math


def pos_to_grid(x,y,size):
    row = int(y / size)
    column = int(x / size)
    return row, column


class Paintable(): # TODO
    """ czesc WINDOWu na ktorej mozna malowac """

    def __init__(self, size, color, pos, WINDOW):
        self.color = color
        self.size = size
        self.pos = pos
        self.WINDOW = WINDOW
        self.surface = pg.Surface((size, size))
        self.surface.fill(color)

    def draw(self):
        self.WINDOW.blit(self.surface, self.pos)

    def update(self, color):
        self.color = color
        self.surface.fill(self.color)
        self.draw()


class Grid():
    """ Klasa ktora tworzy miejsce do malowania """

    def __init__(self, WINDOW, pos, rows, columns, size, color=DEFAULT_COLOR):
        self.WINDOW = WINDOW
        self.pos = pos
        self.posx, self.posy = self.pos
        self.rows = int(rows)
        self.columns = int(columns)
        self.size = size
        self.grid = []

        for row in range(self.rows):
            self.grid.append([])
            for column in range(self.columns):
               self.grid[row].append(Paintable(self.size, color, (self.posx + (self.size * column), self.posy + (self.size * row)), self.WINDOW))

    def draw(self):
        for row in range(self.rows):
            for obj in range(self.columns):
                self.grid[row][obj].draw()

    def getGrid(self):
        return self.grid

    def update_color(self, x, y, color):
        row, column = pos_to_grid(x, y, self.size)

        try:
            if self.grid[row][column].color == color:
                pass
            else:
                self.grid[row][column].update(color)
        except IndexError:
            pass


class Cursor():
    """ Kursor sluzacy do malowania """

    def __init__(self):
        self.x, self.y = (0,0)
        self.prevx, self.prevy = (0,0)
        self.click_status = bool
        self.prev_click_status = bool
        self.rect = pg.Rect(self.x, self.y, 1, 1)

    def update_pos(self):
        self.prevx, self.prevy = self.x, self.y
        self.x, self.y = pg.mouse.get_pos() # TODO: zrobic tak aby pygame zwracal uwage na kazda zmiane pozycji
        self.rect.topleft = (self.x, self.y)

    def is_clicked(self):
        self.prev_click_status = self.click_status
        self.click_status = pg.mouse.get_pressed()[0]
        return self.click_status


class Button():
    """ Buttons which are placen on the GUI surface """

    def __init__(self, WINDOW, x, y, w, h):
        self.pos = (x, y)
        self.WINDOW = WINDOW
        self.width = w
        self.height = h
        self.surface = pg.Surface((w, h))
        self.rect = self.surface.get_rect()
        self.rect.topleft = self.pos

class Color_Button(Button):
    """ Color pallete buttons """

    def __init__(self, WINDOW, x, y, w, h, color):
        super().__init__(WINDOW, x, y, w, h)
        self.color = color
        self.surface.fill(color)

    def draw(self):
        pg.draw.rect(self.WINDOW, BUTTON_BACKGROUND, (self.rect[0] - 3, self.rect[1] - 3, self.rect[2] + 6, self.rect[3] + 6))
        self.WINDOW.blit(self.surface, self.pos)