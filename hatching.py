#! /usr/bin/python3
from PIL import Image
from math import *
from numpy import cross
from constants import *

#rotation = 0 # Global rotation adjust in degrees (so this property can be animated)

def quantize(angle):
    return tau/36*round(36 * angle/tau)

def hatch(angle, coords, spacing=(1, 1), rotation=0):
    """ Does this pixel fall on a line in the hatching pattern?
    """
    width, gap = spacing
    period = (width + gap)
    angle += tau / 360 * rotation
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
    
def hatched_shader(normal, img_coords, h_spacing=(1, 1), v_spacing=(0, 1), xor_mode=False, rotation=0):
    """ Combine vertical and horizontal hatching patterns to determine
    the color at this pixel.
    """
    horizontals = cross(normal, UP)
    verticals = cross(normal, horizontals)
    on_horizontal = hatch(atan2(horizontals[1], horizontals[0]), img_coords, h_spacing, rotation)
    on_vertical = hatch(atan2(verticals[1], verticals[0]), img_coords, v_spacing, rotation)
    if xor_mode:
        pixel_on = on_horizontal != on_vertical
    else:
        pixel_on = on_horizontal or on_vertical
    return BLACK if pixel_on else WHITE    

def process_image(in_file, out_file, h_spacing=(1, 1), v_spacing=(0, 1), xor_mode=False, rotation=0):
    """ Process a normal map image and output an image shaded with hatching lines.
    """
    im = Image.open(in_file)
    px = im.load()
    origin_x = im.size[0]//2
    origin_y = im.size[1]//2
    for x in range(im.size[0]):
        if x % 10 == 0:
            print("Line {} / {}".format(x, im.size[0]))
        for y in range(im.size[1]):
            if len(px[x, y])<4 or px[x, y][3] != 0: # Process only non-transparent pixels
                normal = [n -128 for n in px[x, y][:3]]
                px[x, y] = hatched_shader(normal, (x,y), h_spacing, v_spacing)
    im.save(out_file)
    im.close()
    print("Done")

if __name__ == "__main__":
    from sys import argv, stderr
    import argparse

    parser = argparse.ArgumentParser(description='Convert a normal map image to crosshatched pixel art.')
    parser.add_argument('filenames', metavar='filename', type=str, nargs='+',
                        help='An image file representing a normal map')
    parser.add_argument('-x', '--xor', dest='xor_mode', action='store_const',
                        const=True, default=False,
                        help='Combine vertical and horizontal line fields with XOR. Default is OR.')
    parser.add_argument('--h_spacing', metavar=('line_width', 'line_gap'), type=int, nargs=2,
                        help='Spacing of horizontal lines and gaps.')
    parser.add_argument('--v_spacing', metavar=('line_width', 'line_gap'), type=int, nargs=2,
                        help='Spacing of vertical lines and gaps.')

    args = parser.parse_args()
    h_spacing = args.h_spacing if args.h_spacing != None else DEFAULT_H_SPACING
    v_spacing = args.v_spacing if args.v_spacing != None else DEFAULT_V_SPACING
    
    for in_file in args.filenames:
        out_file = "{}.hatch.png".format(in_file)
        process_image(in_file, out_file, h_spacing, v_spacing, args.xor_mode)
    exit(0)

