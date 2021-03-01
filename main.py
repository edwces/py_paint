import pygame as pg
from pygame.locals import *
from py_paint_settings import *
from class_module import *
import sys

def add_missing_points(mouse, prevx, prevy, x, y, size, grid):
    if mouse.prev_click_status == True:
        missingx = x - prevx
        missingy = y - prevy
        steps = max(abs(missingx), abs(missingy))
        try:
            dx = missingx / steps
            dy = missingy / steps
            for i in range(int(steps)):
                prevx += dx
                prevy += dy
                grid.update_color(prevx, prevy, (0,255,255))
        except ZeroDivisionError:
            pass

pg.init()

class Application():

    def __init__(self):
        """ Funkcja, ktora tworzy okno programu """
        self.WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)

    def setup(self):
        """ Stworz wszystkie obiekty """
        self.grid = Grid(self.WINDOW, (0, 0), ROWS, COLUMNS, PAINTABLE_SIZE) # stworz miejsce na rysowanie
        self.mouse = Cursor() # obiekt ktory pozwala na malowanie
        self.grid.draw()

    def update(self):
        """ Funkcja, ktora odswierza WINDOW """ # zmienic klatki na sekunde dla tej funkcji, sprawdzanie nie zawsze potrzebne
         # sprawdz pozycje myszki

        if self.mouse.is_clicked():
            self.mouse.update_pos() # jezeli myszka je
            self.grid.update_color(self.mouse.x, self.mouse.y, (0, 255, 255))
            add_missing_points(self.mouse, self.mouse.prevx, self.mouse.prevy, self.mouse.x, self.mouse.y, PAINTABLE_SIZE, self.grid)
        pg.display.flip()


    def draw_frames(self):
        """ Funkcja, która rysuje na WINDOWie """


        # licznik fps
        pg.draw.rect(self.WINDOW, WHITE, (0,0, 50, 20))
        czcionka = pg.font.SysFont('Arial', 12) # stworzenie czcionki
        tekst_fps = czcionka.render(f"{self.clock.get_fps():.2f}", True, (255,0,0)) # --> Surface   |  render tekstu
        self.WINDOW.blit(tekst_fps, (5,5)) # narysowanie tekstu na WINDOWie, osadzenie obiektu Surface na WINDOWie(też surface)



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