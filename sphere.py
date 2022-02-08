from numpy import sqrt
from math import atan2
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
    return hatch(atan2(-normal[0], normal[1]), img_coords, 3)
    

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
##                print(x, y, z, "!")
##            else:
##                print(x, y)
##                px[i, j] = (int((x-1)*128), int((y-1)*128), int((z-1)*128))
    if shader == normal_shader:
        im.save("input/sphere_{}.normal.png".format(size))
    elif shader == hatched_shader:
        im.save("output/sphere_{}.hatched.png".format(size))
    print("Done")

sphere(300, hatched_shader)
##if __name__ == "__main__":
##    from sys import argv
##    print(argv)
##    ##im = Image.open("box normal.png")
##    im = Image.new(mode="RGBA", size=(size, size))
    
            


    
