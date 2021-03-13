#################################
# py_paint by edwces
# 2021
# Drawing Program made in Python
#################################

import pygame as pg
from pygame.locals import *
from py_paint_settings import *
from class_module import *
from file_operations import *
from draw_func import *
import sys
from os import path, listdir



pg.init() # Initaliaze pygame

class Application():

    def __init__(self, debug=True):
        """ Stwórz okno i inne wazne zmienne, zaladuj pliki"""
        self.WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)
        self.options = {"color":(0,0,0), "tool":"brush"} # opcje aplikacji
        self.debug = debug # debug opcja
        self.load_assets()

    def load_assets(self):
        """ Zaladuj pliki """
        directory = path.dirname(__file__)              #
        img_folder = path.join(directory, "img")        # znajdz dane foldery
        tools_folder = path.join(img_folder, "tools")   #

        self.tools_imgs = {} # wszystkie przestrzenie z img/tools/* wraz z stringiem opisujacym ich tytuł
        for img in listdir(tools_folder):
            name = path.splitext(img)[0] # znajdz tytol pliku
            surface = pg.image.load(path.join(tools_folder, img))
            print(name)
            self.tools_imgs[name] = surface


    def setup(self):
        """ Stwórz wszystkie potzrebne obiekty i je narysuj na ekranie """
        self.grid = Grid(self.WINDOW, (0, 0), ROWS, COLUMNS, PAINTABLE_SIZE) # stworz liste pixeli
        self.mouse = Cursor()
        self.GUI = draw_GUI()

        self.grid.draw()
        self.WINDOW.blit(self.GUI, (WIDTH-50, 0))
        self.color_pallete = draw_color_pallete(self.WINDOW)
        self.tools_buttons = draw_tools(self.WINDOW, self.tools_imgs)
        self.buttons = self.color_pallete + self.tools_buttons
       

    def update(self):
        """ Funkcja, która aktualizuje logike aplikacji """

        if self.mouse.is_clicked():
            self.mouse.update_pos()
            button_input = self.mouse.rect.collidelist(self.buttons) # zwroc indeks listy przyciskow jezeli kursos przycisnal go 

            if (not button_input == -1) and (not self.mouse.prev_click_status): # sprawdzamy czy klatke wczesniej myszka nie byla przycisnieta
                if self.buttons[button_input].b_type == "color":
                    self.options["color"] = self.buttons[button_input].color # zmien kolor rysowania
                elif self.buttons[button_input].b_type == "tool":
                    self.options["tool"] = self.buttons[button_input].function # zmien narzedzie

            else:
                selected_row, selected_column = pos_to_grid(self.mouse.x, self.mouse.y, self.grid.size)
                if self.options["tool"] == "brush":
                    self.grid.update_color(selected_row, selected_column, (self.options["color"]))
                    missing_inputs = add_missing_points(self.mouse, self.mouse.prevx, self.mouse.prevy, self.mouse.x, # zwroc inputy(jexeli sa one w liscie pixeli) ktorych u nie udalo sie znalezc
                                                        self.mouse.y, PAINTABLE_SIZE) 
                    if missing_inputs: # za kazdy input narysuj zmien kolor pixela
                        for grid_pos in missing_inputs:
                            self.grid.update_color(grid_pos[0], grid_pos[1], self.options["color"])

                elif self.options["tool"] == "eraser":
                    self.grid.update_color(selected_row, selected_column, WHITE)
                    missing_inputs = add_missing_points(self.mouse, self.mouse.prevx, self.mouse.prevy, self.mouse.x,
                                                        self.mouse.y, PAINTABLE_SIZE)
                    
                    if missing_inputs:
                        for grid_pos in missing_inputs:
                            self.grid.update_color(grid_pos[0], grid_pos[1], WHITE)

                elif self.options["tool"] == "color_picker":
                    selected_color = self.grid.get_color(selected_row, selected_column) # zwroc kolor wybranego pixela
                    if not selected_color == None:
                        self.options["color"] = selected_color # zmien kolor rysowania
                
                elif self.options["tool"] == "paint_bucket":
                    selected_color = self.grid.get_color(selected_row, selected_column) # kolor ktory chcemy wypełnic
                    if (selected_color != None) and (not self.mouse.prev_click_status) and (selected_color != self.options["color"]): # 1. jezeli ten kolor jest kolorem 2. jezeli wczesniej nie kliknelismy myszka 3. jezeli kolor nie jest jeszcze wypelniony
                        paint_bucket_action(self.grid, (selected_row, selected_column), self.options["color"], selected_color) # funkcja while zamalowania danego terenu

                elif self.options["tool"] == "save": # WAZNE: narazie typem przycisku save jest tool dlatego dziala to narzaie jako narzedzie, musimy kliknac na liste pixeli aby dzialalo
                    if self.mouse.prev_click_status == False:
                        save_as_img(self.grid)

                elif self.options["tool"] == "load": # WAZNE: narazie typem przycisku load jest tool dlatego dziala to narzaie jako narzedzie, musimy kliknac na liste pixeli aby dzialalo
                    if self.mouse.prev_click_status == False:
                        load_grid_from_img(self.grid)
                        

        pg.display.flip() # Odswierz ekran


    def draw_frames(self):
        """ Funkcja ktora rysuje na ekranie """
        self.grid.draw_updated_cells()
        # FPS licznik
        if self.debug:
            pg.draw.rect(self.WINDOW, WHITE, (0,0, 50, 20)) # stworz biale tlo aby nowy text byl widzialny
            czcionka = pg.font.SysFont('Arial', 12) # stworz czcionke
            tekst_fps = czcionka.render(f"{self.clock.get_fps():.2f}", True, (255,0,0)) # zwroc surface z textem
            self.WINDOW.blit(tekst_fps, (5,5)) # narysuj text na ekranie



def main():
    """ glowna funkcja """

    app = Application()
    app.setup()
    ################### Glowna petla #######################

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()  # wyjdz pygame
                sys.exit() # wyjdz python
        app.update()
        app.draw_frames()
        dt = app.clock.tick(FPS) / 1000 # limit FPS i oblicz delta time
        #print(dt)

main()