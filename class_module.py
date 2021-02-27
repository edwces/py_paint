#################################
# py_paint by edwces
# 2021
# Pixel painter program
#################################

import pygame as pg
from pygame.locals import *
from py_paint_settings import *

def pos_to_grid(x,y,size):
    row = int(y / size)
    column = int(x / size)
    return row, column


class Paintable():
    """ czesc ekranu na ktorej mozna malowac """

    def __init__(self, size, color):
        self.color = color
        self.size = size
        self.surface = pg.Surface((size, size))
        self.surface.fill(color)

    def draw(self, EKRAN, x, y):
        EKRAN.blit(self.surface, (x, y))

    def update(self, color):
        self.color = color
        self.surface.fill(self.color)

class Grid():
    """ Klasa ktora tworzy miejsce do malowania """

    def __init__(self, EKRAN, pos, rows, columns, size, color=DEFAULT_COLOR):
        self.EKRAN = EKRAN
        self.pos = pos
        self.posx, self.posy = self.pos
        self.rows = int(rows)
        self.columns = int(columns)
        self.size = size
        self.grid = []

        for row in range(self.rows):
            self.grid.append([])
            for column in range(self.columns):
               self.grid[row].append(Paintable(self.size, color))

    def draw(self):
        for row in range(self.rows):
            for obj in range(self.columns):
                self.grid[row][obj].draw(self.EKRAN, self.posx + (self.size * obj), self.posy + (self.size * row))

    def getGrid(self):
        return self.grid

    def update_color(self, x, y, color):
        row, column = pos_to_grid(x, y, self.size)
        try:
            self.grid[row][column].update(color)
        except IndexError:
            pass

class Cursor():
    """ Kursor sluzacy do malowania """

    def __init__(self):
        self.posx, self.posy = pg.mouse.get_pos()
        self.click_status = pg.mouse.get_pressed()[0]

    def update_pos(self):
        self.posx, self.posy = pg.mouse.get_pos() # TODO: zrobic tak aby pygame zwracal uwage na kazda zmiane pozycji
    def is_clicked(self):
        return pg.mouse.get_pressed()[0]