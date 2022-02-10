#! /usr/bin/python3
from numpy import sqrt, cross
from math import atan2, pi
from constants import *
from PIL import Image
from hatching import hatch, hatched_shader

def normal_shader(normal, img_coords):
    """ Outputs a normal map.
    """
    x, y, z = normal
    return (int(x*128)+128, int(y*128)+128, int(z*128)+128)


def sphere(size, shader, spacing=(1, 1)):
    im = Image.new(mode="RGBA", size=(size, size))
    px = im.load()
    for i in range(size):
        print("Row {} / {}".format(i, size))
        x=2*i/size - 1
        x_2 = x**2
        for j in range(size):
            y=-(2*j/size-1)
            y_2 = y**2
            #print(x, y)
            if x_2+y_2<1:
                z=sqrt(1-(x_2+y_2))
                px[i, j] = shader((x, y, z), (i, j), spacing)
    if shader == normal_shader:
        path = "sphere_{}.normal.png".format(size)
    elif shader == hatched_shader:
        path = "sphere_{}.hatched.png".format(size)
    try:
        im.save(path)
        print(path)
    except:
        print("Failed to write to", path)

if __name__ == "__main__":
    from sys import argv, stderr
    try:
        sphere(int(argv[1]), hatched_shader, (int(argv[2]), int(argv[3])))
    except:
        print("Usage: {} size line_width line_gap".format(argv[0]))
                                              
                                    


    
