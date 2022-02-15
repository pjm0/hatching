#! /usr/bin/python3
from numpy import sqrt, cross
from math import acos, atan2, pi, tau
from constants import *
from PIL import Image
import hatching
from hatching import hatch, hatched_shader, spherecoord_shader
TICKS = 3600
def normal_shader(normal, img_coords, h_spacing=None, v_spacing=None):
    """ Outputs a normal map.
    """
    x, y, z = normal
    return (int(x*128)+128, int(y*128)+128, int(z*128)+128)


##    return hatched_shader(Z, (lon, lat), h_spacing, v_spacing, xor_mode, 0)


def sphere(size, shader, h_spacing=(1, 1), v_spacing=(0, 1), xor_mode=False, rotation=0):
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
                if shader == spherecoord_shader:
                    px[i, j] = shader((x, y, z), (i, j), (60, 2), xor_mode, rotation)
                else:
                    px[i, j] = shader((x, y, z), (i, j), h_spacing, v_spacing, xor_mode, rotation)
    if shader == normal_shader:
        path = "sphere_{}.normal.png".format(size)
    elif shader == hatched_shader:
        path = "sphere.{}.h{}.v{}{}{}.png".format(size, h_spacing, v_spacing,
                                                ".xor" if xor_mode else "",
                                                  ".r{:03d}".format(rotation))
    elif shader == spherecoord_shader:
        path = "sphere.{}{}.png".format(size, ".r{:03d}".format(rotation))
    try:
        im.save(path)
        print(path)
    except:
        print("Failed to write to", path)

if __name__ == "__main__":
    from sys import argv, stderr
    import argparse

    parser = argparse.ArgumentParser(description='Generate an image representing a 3d sphere.')
    parser.add_argument('size', type=int,
                        help='Side length of the generated image.')
    parser.add_argument('-r', dest='rotation', type=int, default=0,
                        help='Rotation of hatch lines in degrees.')
    parser.add_argument('--h_spacing', metavar=('line_width', 'line_gap'), type=int, nargs=2,
                        help='Spacing of horizontal lines and gaps.')
    parser.add_argument('--v_spacing', metavar=('line_width', 'line_gap'), type=int, nargs=2,
                        help='Spacing of vertical lines and gaps.')
    parser.add_argument('-x', '--xor', dest='xor_mode', action='store_const',
                        const=True, default=False,
                        help='Combine vertical and horizontal line fields with XOR. Default is OR.')
    parser.add_argument('-n', dest='normal_mode', action='store_const',
                        const=True, default=False,
                        help='Output a normal map image. Default is to generate a crosshatched image.')
    parser.add_argument('-s', dest='spherecoord_mode', action='store_const',
                        const=True, default=False,
                        help='Output a spherical grid.')

    args = parser.parse_args()
    rotation = args.rotation
    shader = (normal_shader if args.normal_mode \
              else spherecoord_shader if args.spherecoord_mode \
              else hatched_shader)
    h_spacing = args.h_spacing if args.h_spacing != None else DEFAULT_H_SPACING
    v_spacing = args.v_spacing if args.v_spacing != None else DEFAULT_V_SPACING
    sphere(args.size, shader, tuple(h_spacing), tuple(v_spacing), True, args.rotation)

                                              
                                    


    
