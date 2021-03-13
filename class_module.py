#################################
# py_paint by edwces
# 2021
# Drawing Program made in Python
#################################

import pygame as pg
from pygame.locals import *
from py_paint_settings import *
import sys


def pos_to_grid(x, y, size):
    """ zamien x,y ekranu na pozycje w liscie pixeli """
    row = round(y / size)
    column = round(x / size)
    return row, column



def paint_bucket_action(grid, grid_pos, color, color_to_be_filled):
    """ funkcja ktora sluzy do malowania kubelkiem """
    Stack = [] 
    Stack.append(grid.grid_list[grid_pos[0]][grid_pos[1]])
    while (len(Stack)):
        new_cell = Stack.pop() # usuwamy pixel z listy stack i sprawdzamy czy mamy go pokolorowac
        if (new_cell.color == color_to_be_filled): # jezeli kolor pixela jest kolorem ktrory musimy pokolorowac zmien kolor pixela
            grid.update_color(
                new_cell.grid_pos[0], new_cell.grid_pos[1], color)
        else:
            continue

        for cell in new_cell.get_neighbours(grid): # jezeli pixel dalo sie pokolorowac dodaj do stacku jego sasiadow 

            Stack.append(cell)


class Paintable():
    """ Pixel ktory moze zmienic kolor """

    def __init__(self, size, color, pos, grid_pos, WINDOW):
        self.color = color
        self.size = size
        self.pos = pos # pozycja w x,y
        self.grid_pos = grid_pos # pozycja w row, column
        self.WINDOW = WINDOW
        self.surface = pg.Surface((size, size))
        self.surface.fill(color)

    def get_neighbours(self, grid):
        """ zwroc liste sasiadow danego pixela """
        neighbours = []
        if self.grid_pos[1] < grid.columns - 1:  # Prawo
            neighbours.append(
                grid.grid_list[self.grid_pos[0]][self.grid_pos[1] + 1])
        if self.grid_pos[1] > 0:  # Lewo
            neighbours.append(
                grid.grid_list[self.grid_pos[0]][self.grid_pos[1] - 1])
        if self.grid_pos[0] < grid.rows - 1:  # Góra
            neighbours.append(
                grid.grid_list[self.grid_pos[0] + 1][self.grid_pos[1]])
        if self.grid_pos[0] > 0:  # Dół
            neighbours.append(
                grid.grid_list[self.grid_pos[0] - 1][self.grid_pos[1]])
        return neighbours

    def draw(self):
        self.WINDOW.blit(self.surface, self.pos)

    def update(self, color):
        self.color = color
        self.surface.fill(self.color)


class Grid():
    """ Miejsce na ktorym malujesz, posiada liste pixeli """

    def __init__(self, WINDOW, pos, rows, columns, size, color=DEFAULT_COLOR):
        self.WINDOW = WINDOW
        self.pos = pos
        self.posx, self.posy = self.pos
        self.rows = int(rows)
        self.columns = int(columns)
        self.size = size
        self.grid_list = [] # lista pixeli
        self.updated_cells = []

        for row in range(self.rows):  # Stworz liste obiektow pixeli
            self.grid_list.append([])
            for column in range(self.columns):
                self.grid_list[row].append(Paintable(self.size, color, (self.posx + (
                    self.size * column), self.posy + (self.size * row)), (row, column), self.WINDOW))

    def draw(self):
        for row in range(self.rows):
            for obj in range(self.columns):
                self.grid_list[row][obj].draw()
        print("full_drawing")

    def draw_updated_cells(self):
        """ narysuj pixele ktore zmienily kolor """
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
            return selected_color # zwroc atrybut koloru danego pixela

    def get_grid(self):
        return self.grid_list

    def update_color(self, selected_row, selected_column, new_color):

        if self.is_in_grid((selected_row, selected_column)):
            updated = self.grid_list[selected_row][selected_column]
            if not updated.color == new_color:  # jezeli pixel nie ma danego kolor 
                updated.update(new_color)  # zmien kolor pixela
                self.updated_cells.append(updated) # dodaj go do listy pixeli ktore zmienily kolor


class Cursor():
    """ atrybuty myszki """

    def __init__(self):
        self.x, self.y = (0, 0)
        self.prevx, self.prevy = (0, 0)
        self.click_status = bool
        self.prev_click_status = bool
        self.rect = pg.Rect(self.x, self.y, 1, 1)

    def update_pos(self):
        self.prevx, self.prevy = self.x, self.y # zmien atrybut /poprzedniej pozycji myszki/
        self.x, self.y = pg.mouse.get_pos()
        self.rect.topleft = (self.x, self.y)

    def is_clicked(self):
        self.prev_click_status = self.click_status # zmien atrybut /poprzedniego klikniecia myszki/
        self.click_status = pg.mouse.get_pressed()[0]
        return self.click_status


class Button():
    """ Przyciski """

    def __init__(self, WINDOW, x, y, w, h, b_type, var, function=None):
        self.pos = (x, y)
        self.WINDOW = WINDOW
        self.width = w
        self.height = h
        self.b_type = b_type
        if b_type == "color": # jezeli typ przycisku to /kolor/ to przestrzen bedzie wypelniona danym kolorem
            self.color = var
            self.surface = pg.Surface((w, h))
            self.surface.fill(self.color)
        elif (b_type == "tool") or (b_type == "click"): # jezeli typ przycisku to /narzedzie/ to jego przestrzen bedzie obrazkiem z img/tools/*
            self.function = function
            self.surface = pg.transform.smoothscale(
                var, (w, h)).convert_alpha()
        self.rect = pg.Rect(self.pos, (w, h))

    def draw(self):
        pg.draw.rect(self.WINDOW, BUTTON_BACKGROUND,
                     (self.rect[0] - 3, self.rect[1] - 3, self.rect[2] + 6, self.rect[3] + 6))  # Button border
        self.WINDOW.blit(self.surface, self.pos)
        
