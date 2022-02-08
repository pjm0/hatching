from hatching import hatch, process_image
from math import tau
from PIL import Image
from constants import *
#from line_field import line_field

##in_file = "norm_ex_small.png"
##out_file = "hatch_test.png"
##process_image(in_file, out_file)
CELL_SIZE = 100
ROWS = 1
COLS = 72
CELLS = ROWS * COLS
WIDTH = CELL_SIZE * ROWS
HEIGHT = CELL_SIZE * COLS
SPACING = 1

def test_hatching():
    im = Image.new(mode="RGB", size=(WIDTH, HEIGHT))
    ##im = Image.open("box normal.png")
    px = im.load()
##    origin_x = im.size[0]//2
##    origin_y = im.size[1]//2
    for row in range(ROWS):
        
        for col in range(COLS):
            print(col, "/", COLS)
##            print(row, col)
            cell = col * ROWS + row
            for i in range(CELL_SIZE):
                x = row * CELL_SIZE + i
                for j in range(CELL_SIZE):
                    y = col * CELL_SIZE + j
##                    print(x, y, cell)
                    angle = (cell - CELLS // 2) * tau / CELLS
                    #x[x, y] = hatch(angle, (i, j), 2)
                    px[x, y] = hatch(angle, (i, j), SPACING)
    im.save("output/test_hatching.png")
    im.close()
    print("Done")

if __name__ == "__main__":
    test_hatching()
