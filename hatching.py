#! /usr/bin/python3
from PIL import Image
from math import *
from numpy import cross
from constants import *

def quantize(angle):
    return tau/36*round(36 * angle/tau)

def hatch(angle, coords, spacing=(1, 1)):
    """ Return the color at this pixel
    """
    width, gap = spacing
    period = (width + gap)
    #angle = atan2(sin(angle), cos(angle))
    x, y = coords
    rise, run =  round(sin(angle), 12), -round(cos(angle), 12)
    if abs(rise) > abs(run):
        x, y = y, -x
        rise, run = -run, rise
    slope = rise  / run
    if (y % (period) - (x * slope) % period) % period < width:
        return True
    else:
        return False
    
def hatched_shader(normal, img_coords, spacing = (1, 1)):
    """
    """
    horizontals = cross(normal, UP)
    verticals = cross(normal, horizontals)
    return BLACK if (hatch(atan2(horizontals[1], horizontals[0]), img_coords, spacing)
                     or hatch(atan2(verticals[1], verticals[0]), img_coords, spacing)) else WHITE    
##    return BLACK if (hatch(quantize(atan2(horizontals[1], horizontals[0])), img_coords, spacing)
##                     or hatch(quantize(atan2(verticals[1], verticals[0])), img_coords, spacing)) else WHITE    

def process_image(in_file, out_file, spacing=(1, 1)):
    im = Image.open(in_file)
    px = im.load()
    origin_x = im.size[0]//2
    origin_y = im.size[1]//2
    for x in range(im.size[0]):
        if x % 10 == 0:
            print("Line {} / {}".format(x, im.size[0]))
        for y in range(im.size[1]):
            normal = [n -128 for n in px[x, y][:3]]
            px[x, y] = hatched_shader(normal, (x,y), spacing)
    im.save(out_file)
    im.close()
    print("Done")

if __name__ == "__main__":
    from sys import argv, stderr
    try:
        line_width = int(argv[1])
        line_gap = int(argv[2])
    except:
        print("Usage: {} line_width line_gap file ...", file=stderr)
        exit(-1)
    for in_file in argv[3:]:
        try:
            out_file = "{}.hatch.png".format(in_file)
            process_image(in_file, out_file, (line_width, line_gap))
        except:
            exit(-1)
    exit(0)

