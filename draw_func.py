import pygame as pg
from class_module import *
from py_paint_settings import *

def draw_tools(WINDOW, img_tools):
    tools_button_list = []
    for i, tool in enumerate(TOOLS_ORDER): # za kazde narzedzie ktore mamy w setting.py
        button = Button(WINDOW, WIDTH - 33, 27 * ((i + 11) + 1), BUTTON_WIDTH+5, BUTTON_HEIGHT+5, "tool", img_tools[tool], tool) # nazwy w TOOLS_ORDER musza sie idealnie zgadzac z nazwami plikow
        button.draw()
        tools_button_list.append(button)
    return tools_button_list # zwoc kazdy obiekt przycisku

def draw_color_pallete(WINDOW):
    color_buttons_list = []
    for i, color in enumerate(COLORS): # za kazde kolor ktore mamy w setting.py
        button = Button(WINDOW, WIDTH - 30, 20 * (i + 1), BUTTON_WIDTH, BUTTON_HEIGHT, "color", color)
        button.draw()
        color_buttons_list.append(button)
    return color_buttons_list

def draw_GUI():
    surface = pg.Surface((GUI_WIDTH, GUI_HEIGHT))
    background = surface.get_rect()
    pg.draw.rect(surface, GUI_BORDER, background)  # narysuj obramowanie
    pg.draw.rect(surface, GUI_BACKGROUND,
                 (background[0] + 5, background[1] + 5, background[2], background[3] - 10))

    return surface

def add_missing_points(mouse, prevx, prevy, x, y, size):
    """ zwroc liste brakujacych inputow dla ktorych myszka.update_pos byla za wolna """
    if mouse.prev_click_status == True: # jezeli w czasie ostatniej klatki rysowalismy
        missing = [] # lista brakujacych inputow
        missingx = x - prevx # dx do kolejnego punktu
        missingy = y - prevy # dy do kolejnego punktu
        steps = max(abs(missingx), abs(missingy)) + max(abs(missingx), abs(missingy)) # ile razy musimy zarejestrowac input
        if steps > 0: # jezeli jest odleglosc miedzy poprzednim a nowym punktem w rysowaniu
            dx = missingx / steps # srednia ile musimy dodac podczas kazdego stepu
            dy = missingy / steps # srednia ile musimy dodac podczas kazdego stepu
            for i in range(int(steps)): 
                prevx += dx 
                prevy += dy
                row, column = pos_to_grid(prevx, prevy, size) # zamien x,y na pozycje listy pixeli
                missing.append([row, column])
            return missing
        else:
            return False