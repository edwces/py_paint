#################################
# py_paint by edwces
# 2021
# Drawing Program made in Python
#################################

import pygame as pg
from pygame.locals import *
from py_paint_settings import *
from class_module import *
import sys


def draw_color_pallete(WINDOW):
    """ Creates color_Buttons and draws them on the window """
    buttons_list = []
    for color in range(len(COLORS)): # for each color that we have in settings.py
        button = Color_Button(WINDOW, WIDTH - 30, 20 * (color + 1), 15, 15, COLORS[color])
        button.draw()
        buttons_list.append(button)
    return buttons_list # return all of the buttons in the list


def GUI():
    surface = pg.Surface((GUI_WIDTH, GUI_HEIGHT))
    background = surface.get_rect()
    pg.draw.rect(surface, GUI_BORDER, background) # draw a border
    pg.draw.rect(surface, GUI_BACKGROUND, (background[0] + 5, background[1] + 5, background[2], background[3] - 10))

    return surface


def add_missing_points(mouse, prevx, prevy, x, y, size, grid, color):
    """ Add missing Paintable color changes for inputs that were too slow """
    if mouse.prev_click_status == True: # if last frame mouse was clicked
        missingx = x - prevx
        missingy = y - prevy
        steps = max(abs(missingx), abs(missingy)) # how many times we have to add inputs
        try:
            dx = missingx / steps # average of how much dx we have to add each step
            dy = missingy / steps
            for i in range(int(steps)):
                prevx += dx
                prevy += dy
                grid.update_color(prevx, prevy, color) # update Paintable color for that input
        except ZeroDivisionError: # Gonna trigger if we haven't got any missing inputs
            pass

pg.init() # Initaliaze pygame

class Application():

    def __init__(self, debug=False):
        """ Create window and create important variables"""
        self.WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)
        self.options = {"color":(0,0,0)} # App options
        self.debug = debug # debug option

    def setup(self):
        """ Create all the objects and draw neccesary stuff"""
        self.grid = Grid(self.WINDOW, (0, 0), ROWS, COLUMNS, PAINTABLE_SIZE) # Create a grid to draw
        self.mouse = Cursor()
        self.GUI = GUI()

        self.grid.draw()
        self.WINDOW.blit(self.GUI, (WIDTH-50, 0))
        self.color_pallete = draw_color_pallete(self.WINDOW)

    def update(self):
        """ Function, that updates app variables"""


        if self.mouse.is_clicked():
            self.mouse.update_pos()
            color_input = self.mouse.rect.collidelist(self.color_pallete) # return index of a color_pallete list if you click on color button
            if (not color_input == -1) and (not self.mouse.prev_click_status):
                self.options["color"] = self.color_pallete[color_input].color # change the color you are drawing
            else:
                self.grid.update_color(self.mouse.x, self.mouse.y, (self.options["color"])) # update color of a clicked Paintable
                add_missing_points(self.mouse, self.mouse.prevx, self.mouse.prevy, self.mouse.x,
                                   self.mouse.y, PAINTABLE_SIZE, self.grid, self.options["color"])

        pg.display.flip() # Update the screen


    def draw_frames(self):
        """ Function that draws on window """


        # FPS counter
        if self.debug:
            pg.draw.rect(self.WINDOW, WHITE, (0,0, 50, 20)) # make new text visible
            czcionka = pg.font.SysFont('Arial', 12) # create font
            tekst_fps = czcionka.render(f"{self.clock.get_fps():.2f}", True, (255,0,0)) # return surface and render text
            self.WINDOW.blit(tekst_fps, (5,5)) # draw text on window



def main():
    """ Main function """

    app = Application()
    app.setup()
    ################### Main Loop #######################

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()  # quit pygame
                sys.exit() # quit python
        app.update()
        app.draw_frames()
        dt = app.clock.tick(FPS) / 1000 # limit FPS and calculate delta time

main()