import pygame as pg
from class_module import *
from py_paint_settings import *

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

def draw_GUI():
    surface = pg.Surface((GUI_WIDTH, GUI_HEIGHT))
    background = surface.get_rect()
    pg.draw.rect(surface, GUI_BORDER, background)  # draw a border
    pg.draw.rect(surface, GUI_BACKGROUND,
                 (background[0] + 5, background[1] + 5, background[2], background[3] - 10))

    return surface

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