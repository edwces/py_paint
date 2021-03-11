from py_paint_settings import *
from PIL import Image
import numpy as np
from tkinter import filedialog, Tk
root = Tk()
root.withdraw()

def save_as_img(grid):

    filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("png files","*.png"),  ('All files', '*.*')))
    if filepath != '':
        rgb_array = np.zeros((ROWS, COLUMNS, 3), 'uint8')
        for row in range(ROWS):
            for column in range(COLUMNS):
                rgb_array[row][column] = grid.grid_list[row][column].color

        img = Image.fromarray(rgb_array)
        img.save(filepath, 'PNG')
        return filepath
    else:
        return False

def load_grid_from_img(grid):
    imgfile = filedialog.askopenfile(filetypes=(("png files","*.png"),  ('All files', '*.*')))
    if imgfile:
        print(imgfile)
        with Image.open(imgfile.name) as img:
            rgb_array = list(img.getdata())
        
        for row in range(ROWS):
            for column in range(COLUMNS):
                
                my_new = (row*ROWS) + column
                print(my_new)
                grid.update_color(row, column, rgb_array[my_new])
        return imgfile
    return False

        

    