#################################
# py_paint by edwces
# 2021
# Drawing Program made in Python
#################################

import pygame as pg
from pygame.locals import *
from py_paint_settings import *


def pos_to_grid(x,y,size):
    row = int(y / size)
    column = int(x / size)
    return row, column

def draw_GUI():
    surface = pg.Surface((GUI_WIDTH, GUI_HEIGHT))
    background = surface.get_rect()
    pg.draw.rect(surface, GUI_BORDER, background) # draw a border
    pg.draw.rect(surface, GUI_BACKGROUND, (background[0] + 5, background[1] + 5, background[2], background[3] - 10))

    return surface


class Paintable():
    """ Cell with changeble color """

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
    """ Space, where you paint"""

    def __init__(self, WINDOW, pos, rows, columns, size, color=DEFAULT_COLOR):
        self.WINDOW = WINDOW
        self.pos = pos
        self.posx, self.posy = self.pos
        self.rows = int(rows)
        self.columns = int(columns)
        self.size = size
        self.grid = []

        for row in range(self.rows): # Create grid of Paintable objects
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
            if self.grid[row][column].color == color: # if Paintable already has that color value pass
                pass
            else:
                self.grid[row][column].update(color) # change color of given Paintable
        except IndexError: # if you are beyond the grid space
            pass


class Cursor():
    """ Cursor variables """

    def __init__(self):
        self.x, self.y = (0,0)
        self.prevx, self.prevy = (0,0)
        self.click_status = bool
        self.prev_click_status = bool
        self.rect = pg.Rect(self.x, self.y, 1, 1)

    def update_pos(self):
        self.prevx, self.prevy = self.x, self.y
        self.x, self.y = pg.mouse.get_pos()
        self.rect.topleft = (self.x, self.y)

    def is_clicked(self):
        self.prev_click_status = self.click_status
        self.click_status = pg.mouse.get_pressed()[0]
        return self.click_status


class Button():
    """ Buttons which are placen on the GUI surface """

    def __init__(self, WINDOW, x, y, w, h, b_type, var, function=None):
        self.pos = (x, y)
        self.WINDOW = WINDOW
        self.width = w
        self.height = h
        self.b_type = b_type
        if b_type == "color":
            self.color = var
            self.surface = pg.Surface((w, h))
            self.surface.fill(self.color)
        elif b_type == "tool":
            self.function = function
            self.surface = pg.transform.smoothscale(var, (w, h)).convert_alpha()
        self.rect = pg.Rect(self.pos, (w,h))

    def draw(self):
        pg.draw.rect(self.WINDOW, BUTTON_BACKGROUND, (self.rect[0] - 3, self.rect[1] - 3, self.rect[2] + 6, self.rect[3] + 6)) # Button border
        self.WINDOW.blit(self.surface, self.pos)

class Color_Button(Button):
    """ Color pallete buttons """

    def __init__(self, WINDOW, x, y, w, h, color):
        super().__init__(WINDOW, x, y, w, h) # Initialize the Button class
        self.color = color
        self.surface.fill(color)