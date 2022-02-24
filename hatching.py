#! /usr/bin/python3
from PIL import Image
from math import *
from numpy import cross, dot
from constants import *
from random import random

#rotation = 0 # Global rotation adjust in degrees (so this property can be animated)
def f():
    pass

def normalize(v):
    magnitude = sqrt(sum(n**2 for n in v))
    return [n / magnitude for n in v]

def get_brightness(normal, contrast, angle = 90*tau/360):
    # Rotate normal around x
    x = normal[0]
    y = normal[1] * sin(angle) - normal[2] * cos(angle)
    z = (normal[1] * cos(angle) + normal[2] * sin(angle))
    light_source = 1, 0, 1
    # Rotate light source around z
    l_x = light_source[0] * sin(angle) - light_source[1] * cos(angle)#normal[0]
    l_y = (light_source[0] * cos(angle) + light_source[1] * sin(angle))
    l_z = light_source[2]#
    
    brightness = max(0, dot(normal, (l_x, l_y, l_z)))
    return (brightness - 0.5) * contrast + 0.5


def hatch(angle, coords, spacing=(1, 1), rotation=0):
    """ Does this pixel fall on a line in the hatching pattern?
    """
    width, gap = spacing
    period = (width + gap)
    angle += tau / 360 * rotation
    x, y = coords
    rise, run =  round(sin(angle), 12), round(cos(angle), 12)
    if abs(rise) > abs(run):
        x, y = y, -x
        rise, run = -run, rise
    slope = rise  / run
    if (y % (period) - (x * slope) % period) % period < width:
        return True
    else:
        return False
SPACING=5    
def hatched_shader(normal, img_coords, h_spacing=(1, 1), xor_mode=False, rotation=0):
    """ Combine vertical and horizontal hatching patterns to determine
    the color at this pixel.
    """
    brightness = round(SPACING * get_brightness(normal, 1, rotation*tau/360))
    h_spacing = SPACING - brightness, brightness
##    h_spacing = tuple(val / gcd(*h_spacing) for val in h_spacing)
    
    horizontals = normalize(cross(normal, UP))
    verticals = normalize(cross(normal, horizontals))
    on_horizontal = hatch(atan2(horizontals[1], horizontals[0]), img_coords, h_spacing, 0)
    on_vertical = hatch(atan2(verticals[1], verticals[0]), img_coords, v_spacing, 0)
    if xor_mode:
        pixel_on = on_horizontal != on_vertical
    else:
        pixel_on = on_horizontal or on_vertical
    return BLACK if pixel_on else WHITE

##def spherecoord_shader(normal, img_coords, spacing=(24, 10), xor_mode=False, rotation=0):
##    """ Outputs a spherical grid.
##    """
##    angle = -rotation*tau/360
##    divisions, width_ratio = spacing
##    # Rotate normal around x
##    x = normal[0]
##    y = -normal[1] * sin(angle) - normal[2] * cos(angle)
##    z = (-normal[1] * cos(angle) + normal[2] * sin(angle))
##
##    lat = atan2(y, x)
##    lon = acos(z)
##    on_lat_line = abs(lat % (tau / divisions)) < tau / divisions / width_ratio
##    on_lon_line = abs(lon % (tau / divisions)) < tau / divisions / width_ratio
##    return BLACK if ((on_lat_line != on_lon_line) if xor_mode else (on_lat_line or on_lon_line)
##                     ) else WHITE

def spherecoord_shader(normal, img_coords, spacing=(24, 10), xor_mode=False, rotation=0):
    """ Outputs a spherical grid.
    """
    BRIGHT_ADJUST = 0.5
    angle = rotation*tau/360
    divisions = 1000000
    
    # Rotate normal around x
    x = normal[0]
    y = normal[1] * sin(angle) - normal[2] * cos(angle)
    z = (normal[1] * cos(angle) + normal[2] * sin(angle))
    light_source = 1, 0, 1
    # Rotate light source around z
    l_x = light_source[0] * sin(angle) - light_source[1] * cos(angle)#normal[0]
    l_y = (light_source[0] * cos(angle) + light_source[1] * sin(angle))
    l_z = light_source[2]#
    
    brightness = max(0, dot(normal, (l_x, l_y, l_z)))
    brightness = (brightness - 0.5) * BRIGHT_ADJUST + 0.5
    lon = atan2(y, x)
    lat = acos(z)
    #gray=(floor(brightness*255),)*3
    on_lat_line = abs(lat % (tau / divisions)) > tau / divisions * brightness
    #on_lon_line = abs(lon % (tau / divisions)) > tau / divisions * brightness

    
    return BLACK if (on_lat_line) else WHITE

def grayscale_shader(normal, img_coords, spacing=(24, 10), xor_mode=False, rotation=0):
    """ Outputs a spherical grid.
    """
    BRIGHT_ADJUST = 0.5
    angle = rotation*tau/360
    divisions = 32
    
    # Rotate normal around x
    x = normal[0]
    y = normal[1] * sin(angle) - normal[2] * cos(angle)
    z = (normal[1] * cos(angle) + normal[2] * sin(angle))
    light_source = 1, 0, 1
    # Rotate light source around z
    l_x = light_source[0] * sin(angle) - light_source[1] * cos(angle)#normal[0]
    l_y = (light_source[0] * cos(angle) + light_source[1] * sin(angle))
    l_z = light_source[2]#
    
    brightness = max(0, dot(normal, (l_x, l_y, l_z)))
    brightness = (brightness - 0.5) * BRIGHT_ADJUST + 0.5


    
    return (int(255 * brightness),)*3

def rand_dithered_shader(normal, img_coords, spacing=(24, 10), xor_mode=False, rotation=0):
    brightness = get_brightness(normal, 0.6)
    return BLACK if brightness < random() else WHITE

def process_image(in_file, out_file, h_spacing=(1, 1), v_spacing=(0, 1), xor_mode=False, rotation=0, shader=spherecoord_shader):
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
                magnitude = sqrt(sum(n**2 for n in normal))
                normal = [n / magnitude for n in normal]
                #px[x, y] = hatched_shader(normal, (x,y), h_spacing, v_spacing)
                px[x, y] = f(normal, (x,im.size[1]-y), (8, 10), False, 0)
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
    parser.add_argument('-s', dest='spherecoord_mode', action='store_const',
                        const=True, default=False,
                        help='Use spherical coordinates to generate a grid.')
    parser.add_argument('-g', dest='greyscale_mode', action='store_const',
                        const=True, default=False,
                        help='Generate greyscale image with directional lighting.')
    parser.add_argument('-r', dest='dithered_mode', action='store_const',
                        const=True, default=False,
                        help='Generate random dithered image with directional lighting.')

    args = parser.parse_args()
    h_spacing = args.h_spacing if args.h_spacing != None else DEFAULT_H_SPACING
    v_spacing = args.v_spacing if args.v_spacing != None else DEFAULT_V_SPACING
    f = (spherecoord_shader if args.spherecoord_mode
         else grayscale_shader if args.greyscale_mode
         else rand_dithered_shader if args.dithered_mode
         else hatched_shader)
    for in_file in args.filenames:
        out_file = "{}.hatch.png".format(in_file)
        process_image(in_file, out_file, h_spacing, v_spacing, args.xor_mode)
    exit(0)

