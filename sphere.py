#!usr/bin/python3
from numpy import sqrt
from math import atan2, pi
from constants import TRANSPARENT
from PIL import Image
from hatching import hatch

def normal_shader(normal, img_coords):
    """ Outputs a normal map.
    """
    x, y, z = normal
    return (int(x*128)+128, int(y*128)+128, int(z*128)+128)

def hatched_shader(normal, img_coords):
    """
    """
    return hatch(2*atan2(normal[1], normal[0]), img_coords, 10)
    

def sphere(size, shader):
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
                px[i, j] = shader((x, y, z), (i, j))
    if shader == normal_shader:
        path = "input/sphere_{}.normal.png".format(size)
    elif shader == hatched_shader:
        path = "output/sphere_{}.hatched.png".format(size)
    try:
        im.save(path)
        print(path)
    except:
        print("Failed to write to", path)

if __name__ == "__main__":
    from sys import argv
    sphere(1000, hatched_shader)

    
