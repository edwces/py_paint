import pygame as pg
from pygame.locals import *
from py_paint_settings import *
from class_module import *
import sys


pg.init()

class Application():

    def __init__(self):
        """ Funkcja, ktora tworzy okno programu """
        self.EKRAN = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)

    def setup(self):
        """ Stworz wszystkie obiekty """
        self.grid = Grid(self.EKRAN, (0, 0), ROWS, COLUMNS, PAINTABLE_SIZE) # stworz miejsce na rysowanie
        self.mouse = Cursor() # obiekt ktory pozwala na malowanie
        self.grid.draw()

    def update(self):
        """ Funkcja, ktora odswierza ekran """ # zmienic klatki na sekunde dla tej funkcji, sprawdzanie nie zawsze potrzebne
         # sprawdz pozycje myszki

        if self.mouse.is_clicked():
            self.mouse.update_pos() # jezeli myszka je
            self.grid.update_color(self.mouse.posx, self.mouse.posy, (0, 255, 255))
        pg.display.flip()


    def draw_frames(self):
        """ Funkcja, która rysuje na ekranie """


        # licznik fps
        pg.draw.rect(self.EKRAN, BIALY, (0,0, 50, 20))
        czcionka = pg.font.SysFont('Arial', 12) # stworzenie czcionki
        tekst_fps = czcionka.render(f"{self.clock.get_fps():.2f}", True, (255,0,0)) # --> Surface   |  render tekstu
        self.EKRAN.blit(tekst_fps, (5,5)) # narysowanie tekstu na ekranie, osadzenie obiektu Surface na Ekranie(też surface)



def main():
    """ Glowna funkcja """

    app = Application()
    app.setup()
    ################### Główna Petla #######################

    while True: # Pętla aplikacji
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()  # powiedz aplikacji aby sie wylaczyla
                sys.exit() # powiedz systemowi ze program sie wylaczyl
        app.update()
        app.draw_frames()
        dt = app.clock.tick(FPS) / 1000
        print(dt) # limit FPS

main()