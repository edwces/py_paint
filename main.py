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
from os import path, listdir

sys.setrecursionlimit(10000)

def draw_tools(WINDOW, img_tools):
    tools_button_list = []
    for i, tool in enumerate(TOOLS_ORDER): # for each tool that we have in settings.py
        button = Button(WINDOW, WIDTH - 33, 27 * ((i + 11) + 1), BUTTON_WIDTH+5, BUTTON_HEIGHT+5, "tool", img_tools[tool], tool)
        button.draw()
        tools_button_list.append(button)
    return tools_button_list

def draw_color_pallete(WINDOW):
    """ Creates color_Buttons and draws them on the window """
    color_buttons_list = []
    for i, color in enumerate(COLORS): # for each color that we have in settings.py
        button = Button(WINDOW, WIDTH - 30, 20 * (i + 1), BUTTON_WIDTH, BUTTON_HEIGHT, "color", color)
        button.draw()
        color_buttons_list.append(button)
    return color_buttons_list # return all of the buttons in the list


def add_missing_points(mouse, prevx, prevy, x, y, size):
    """ Add missing Paintable color changes for inputs that were too slow """
    if mouse.prev_click_status == True: # if last frame mouse was clicked
        missing = []
        missingx = x - prevx
        missingy = y - prevy
        steps = max(abs(missingx), abs(missingy)) + max(abs(missingx), abs(missingy)) # how many times we have to add inputs
        if steps > 0: # Gonna trigger if we have some missing inputs
            dx = missingx / steps # average of how much dx we have to add each step
            dy = missingy / steps
            for i in range(int(steps)):
                prevx += dx
                prevy += dy
                row, column = pos_to_grid(prevx, prevy, size)
                missing.append([row, column])
            return missing
        else:
            return False
                



pg.init() # Initaliaze pygame

class Application():

    def __init__(self, debug=False):
        """ Create window and create important variables"""
        self.WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)
        self.options = {"color":(0,0,0), "tool":"brush"} # App options
        self.debug = debug # debug option
        self.load_assets()

    def load_assets(self): # IMPORTANT: this method doesnt do anything right now
        """ Load assets into the app """
        directory = path.dirname(__file__)              #
        img_folder = path.join(directory, "img")        # Get all the directories
        tools_folder = path.join(img_folder, "tools")   #

        self.tools_imgs = {} # All tools surface objects
        for img in listdir(tools_folder):
            name = path.splitext(img)[0]
            surface = pg.image.load(path.join(tools_folder, img))
            print(name)
            self.tools_imgs[name] = surface


    def setup(self):
        """ Create all the objects and draw neccesary stuff"""
        self.grid = Grid(self.WINDOW, (0, 0), ROWS, COLUMNS, PAINTABLE_SIZE) # Create a grid to draw
        self.mouse = Cursor()
        self.GUI = draw_GUI()

        self.grid.draw()
        self.WINDOW.blit(self.GUI, (WIDTH-50, 0))
        self.color_pallete = draw_color_pallete(self.WINDOW)
        self.tools_buttons = draw_tools(self.WINDOW, self.tools_imgs)
        self.buttons = self.color_pallete + self.tools_buttons
       

    def update(self):
        """ Function, that updates app variables"""

        if self.mouse.is_clicked():
            self.mouse.update_pos()
            button_input = self.mouse.rect.collidelist(self.buttons) # return index of a color_pallete list if you click on color button

            if (not button_input == -1) and (not self.mouse.prev_click_status):
                if self.buttons[button_input].b_type == "color":
                    self.options["color"] = self.buttons[button_input].color # change the color you are drawing
                elif self.buttons[button_input].b_type == "tool":
                    self.options["tool"] = self.buttons[button_input].function # change your tool

            else:
                selected_row, selected_column = pos_to_grid(self.mouse.x, self.mouse.y, self.grid.size)
                if self.options["tool"] == "brush":
                    self.grid.update_color(selected_row, selected_column, (self.options["color"])) # update color of a clicked Paintable
                    missing_inputs = add_missing_points(self.mouse, self.mouse.prevx, self.mouse.prevy, self.mouse.x,
                                                        self.mouse.y, PAINTABLE_SIZE)
                    if missing_inputs:
                        for grid_pos in missing_inputs:
                            self.grid.update_color(grid_pos[0], grid_pos[1], self.options["color"])

                elif self.options["tool"] == "eraser":
                    self.grid.update_color(selected_row, selected_column, WHITE) # update color of a clicked Paintable
                    missing_inputs = add_missing_points(self.mouse, self.mouse.prevx, self.mouse.prevy, self.mouse.x,
                                                        self.mouse.y, PAINTABLE_SIZE)
                    
                    if missing_inputs:
                        for grid_pos in missing_inputs:
                            self.grid.update_color(grid_pos[0], grid_pos[1], WHITE)

                elif self.options["tool"] == "color_picker":
                    selected_color = self.grid.get_color(selected_row, selected_column)
                    if not selected_color == None:
                        self.options["color"] = selected_color # change the color you are drawing
                
                elif self.options["tool"] == "paint_bucket":
                    selected_color = self.grid.get_color(selected_row, selected_column)
                    if (selected_color != None) and (not self.mouse.prev_click_status) and (selected_color != self.options["color"]):
                        paint_bucket_action(self.grid, (selected_row, selected_column), self.options["color"], selected_color)
                        

        pg.display.flip() # Update the screen


    def draw_frames(self):
        """ Function that draws on window """
        self.grid.draw_updated_cells()
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