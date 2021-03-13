from py_paint_settings import *
from PIL import Image
import numpy as np
from tkinter import filedialog, Tk
root = Tk()
root.withdraw() # schowaj okno tkinkera

def save_as_img(grid):
    """ WAZNE: zapisuje tylko w 128x128 """
    filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("png files","*.png"),  ('All files', '*.*'))) # zwroc sciezka do pliku.png
    if filepath != '': # jezeli wybralismy prawdilowa sciezke
        rgb_array = np.zeros((ROWS, COLUMNS, 3), 'uint8') # stworz liste numpy
        for row in range(ROWS):
            for column in range(COLUMNS):
                rgb_array[row][column] = grid.grid_list[row][column].color # przydziel danemu miejscu w liscie dany kolor z listy pixeli

        img = Image.fromarray(rgb_array) # stworz obraz z listy
        img.save(filepath, 'PNG') # zapisz plik.png
        return filepath
    else:
        return False

def load_grid_from_img(grid):
    """ WAZNE: obsluguje tylko pliki 128x128 """
    imgfile = filedialog.askopenfile(filetypes=(("png files","*.png"),  ('All files', '*.*'))) # zwroc sciezke do pliku.png
    if imgfile != '': # jezeli wybralismy prawdilowa sciezke
        print(imgfile)
        with Image.open(imgfile.name) as img: # otworz plik jako PIL.Image
            rgb_array = list(img.getdata()) # wez dane pixeli z obrazka 
        
        for row in range(ROWS):
            for column in range(COLUMNS):
                
                my_new = (row*ROWS) + column # WAZNE: rgb_array nie jest podzielony na warstwy , to po prostu jedna dluga lista
                print(my_new)
                grid.update_color(row, column, rgb_array[my_new]) # zmien kolor kazdego pixela, aby powstal obraz ktory zaladowalismy
        return imgfile
    return False

        

    