from PIL import Image
from math import *
from numpy import cross
from constants import *

   
def hatch(angle, coords, spacing = 1):
    """ Return the color at this pixel
    """
    if angle > tau:
        angle -= tau
    elif angle < -tau:
        angle += tau
    try:
        x, y = coords
        rise, run =  sin(angle), cos(angle)
        slope = rise / run
        ##    print(rise, run)
        if not (abs(angle) <= pi / 4 or abs(angle) >= 3 * pi / 4):
            # Line closer to vertical. Switch axes, x dependent on y
            x, y = y, x
            rise, run = run, rise
        if y % (spacing) == round((x% (spacing / (slope))) * slope):
            return BLACK
        else:
            return WHITE
    except: # Error condition encountered
        return RED

def process_image(in_file, out_file):
    im = Image.open(in_file)
    ##im = Image.open("box normal.png")
    px = im.load()
    origin_x = im.size[0]//2
    origin_y = im.size[1]//2
    for x in range(im.size[0]):
        if x % 10 == 0:
            print("Line {} / {}".format(x, im.size[0]))
        for y in range(im.size[1]):
            pixel = px[x, y]
            if pixel[0] == pixel[1] == pixel[2]:
                px[x, y] = (0,)*4

            else:
                normal = [n -180 for n in pixel[:3]]
                xp = cross(normal, (0, sin(-pi/6), cos(-pi/6)))
                angle = atan2(xp[1], xp[0])
                #pi/2 + atan2(origin_x - x, origin_y - y)#

                px[x, y] = hatch(angle, (x, y), 3)
                
    #processed_im = im.point(invert)
    im.save(out_file)
    im.close()
    print("Done")
# "scene normal.png"
# "norm_ex_wp.png"
# "example_normals.png"
# "sphere_normal.jpg"
if __name__ == "__main__":
    in_file = "norm_ex_small.png"
    out_file = "scene hatched.png"
    process_image(in_file, out_file)

