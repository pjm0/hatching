from hatching import hatch, process_image
from math import tau
from PIL import Image
from constants import *
#from line_field import line_field

##in_file = "norm_ex_small.png"
##out_file = "hatch_test.png"
##process_image(in_file, out_file)
CELL_SIZE = 80
ROWS = 4
COLS = 360
CELLS = ROWS
WIDTH = CELL_SIZE * ROWS
HEIGHT = CELL_SIZE * COLS
#SPACING = 10

def test_hatching():
    im = Image.new(mode="RGB", size=(WIDTH, HEIGHT))
    ##im = Image.open("box normal.png")
    px = im.load()
##    origin_x = im.size[0]//2
##    origin_y = im.size[1]//2
    for col in range(COLS):
        for row in range(ROWS):
            spacing = row+1
            print(col, "/", COLS)
##            print(row, col)
            cell = col
            for i in range(CELL_SIZE):
                x = row * CELL_SIZE + i
                for j in range(CELL_SIZE):
                    y = col * CELL_SIZE + j
##                    print(x, y, cell)
                    angle = (col - COLS // 2) * tau / COLS
                    #x[x, y] = hatch(angle, (i, j), 2)
                    px[x, y] = BLACK if hatch(angle, (i, j), (spacing, spacing)) else WHITE
    im.save("output/test_hatching.png")
    im.close()
    print("Done")

if __name__ == "__main__":
    test_hatching()
    print("\a")
