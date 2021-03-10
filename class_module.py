#################################
# py_paint by edwces
# 2021
# Drawing Program made in Python
#################################

import pygame as pg
from pygame.locals import *
from py_paint_settings import *
import sys

def pos_to_grid(x,y,size):
    row = round(y / size)
    column = round(x / size)
    return row, column

def draw_GUI():
    surface = pg.Surface((GUI_WIDTH, GUI_HEIGHT))
    background = surface.get_rect()
    pg.draw.rect(surface, GUI_BORDER, background) # draw a border
    pg.draw.rect(surface, GUI_BACKGROUND, (background[0] + 5, background[1] + 5, background[2], background[3] - 10))

    return surface


  

def paint_bucket_action(grid, grid_pos, color, color_to_be_filled): # TODO: make this a while loop function
    Stack = []
    Stack.append(grid.grid_list[grid_pos[0]][grid_pos[1]])
    while (len(Stack)):
        new_cell = Stack.pop()
        if (new_cell.color == color_to_be_filled):
            grid.update_color(new_cell.grid_pos[0], new_cell.grid_pos[1], color)
        else:
            continue

        for cell in grid.get_neighbours(new_cell.grid_pos[0], new_cell.grid_pos[1]):
        
            Stack.append(cell)
    



class Paintable():
    """ Cell with changeble color """

    def __init__(self, size, color, pos, grid_pos, WINDOW):
        self.color = color
        self.size = size
        self.pos = pos
        self.grid_pos = grid_pos
        self.WINDOW = WINDOW
        self.surface = pg.Surface((size, size))
        self.surface.fill(color)

    def draw(self):
        self.WINDOW.blit(self.surface, self.pos)

    def update(self, color):
        self.color = color
        self.surface.fill(self.color)
        


class Grid():
    """ Space, where you paint"""

    def __init__(self, WINDOW, pos, rows, columns, size, color=DEFAULT_COLOR):
        self.WINDOW = WINDOW
        self.pos = pos
        self.posx, self.posy = self.pos
        self.rows = int(rows)
        self.columns = int(columns)
        self.size = size
        self.grid_list = []
        self.updated_cells = []

        for row in range(self.rows): # Create grid of Paintable objects
            self.grid_list.append([])
            for column in range(self.columns):
               self.grid_list[row].append(Paintable(self.size, color, (self.posx + (self.size * column), self.posy + (self.size * row)), (row, column), self.WINDOW))

    def draw(self):
        for row in range(self.rows):
            for obj in range(self.columns):
                self.grid_list[row][obj].draw()

    def get_neighbours(self, selected_row, selected_column):
        neighbours = []
        if selected_column < self.columns - 1: #Right
            neighbours.append(self.grid_list[selected_row][selected_column + 1])
        if selected_column > 0: #Left
            neighbours.append(self.grid_list[selected_row][selected_column - 1])
        if selected_row < self.rows - 1: #Up
            neighbours.append(self.grid_list[selected_row + 1][selected_column])
        if selected_row > 0 : #Down
            neighbours.append(self.grid_list[selected_row - 1][selected_column])
        return neighbours


    def draw_updated_cells(self):
        for paintable in self.updated_cells:
            paintable.draw()
        self.updated_cells = []

    def is_in_grid(self, grid_pos):
        occurrence = True
        try:
            self.grid_list[grid_pos[0]][grid_pos[1]]
        except IndexError:
            occurrence = False
        return occurrence

    def get_color(self, selected_row, selected_column):
        if self.is_in_grid((selected_row, selected_column)):
            selected_color = self.grid_list[selected_row][selected_column].color
            return selected_color


    def get_grid(self):
        return self.grid_list

    

    def update_color(self, selected_row, selected_column, new_color):

        if self.is_in_grid((selected_row, selected_column)):
            updated = self.grid_list[selected_row][selected_column]
            if not updated.color == new_color: # if Paintable already has that color value pass
                updated.update(new_color) # change color of given Paintable
                self.updated_cells.append(updated)


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