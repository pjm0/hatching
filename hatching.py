from PIL import Image
from math import *
from numpy import cross
from constants import *
from line_field import line_field

RADIUS = 60
   
def hatch(angle, coords, spacing = 1):
    """ Return the color at this pixel
    """
    angle = -round(angle, 10)
    run, rise  = round(RADIUS * cos(angle)), round(RADIUS * sin(angle))
    return BLACK if line_field(run, rise, spacing)(*coords) else WHITE

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
                normal = [n -128 for n in pixel[:4]]
                #normal[1] = -normal[1]
                #cross_p = cross((0, normal[1], normal[2]), (normal[0], 0, normal[2]))
                #cross_a = cross(normal, (0, sin(-pi/6), cos(-pi/6)))
                #cross_b =  #cross(normal, (0, 0, 1))
                #angle_a = atan2(cross_a[1], cross_a[0])
                #angle_a = 3#atan2(normal[1], normal[0])
                #angle_b = atan2(normal[0], normal[1])
                angle_b = atan2(normal[0], -normal[1])
                #angle_b = 0
##                angle = atan2(normal[1], normal[0])
##                angle = atan2(normal[1], normal[0])
                #pi/2 + atan2(origin_x - x, origin_y - y)#

                result_a = hatch(angle_b, (x, y), 3)
                #result_b = hatch(angle_b, (x, y), 3)
                px[x, y] = result_a#BLACK if BLACK in (result_a ,result_b) else WHITE 
                
    #processed_im = im.point(invert)
    im.save(out_file)
    im.close()
    print("Done")
# "scene normal.png"
# "norm_ex_wp.png"
# "example_normals.png"
# "sphere_normal.jpg"
if __name__ == "__main__":
##    from test_hatching import test_hatching
##    test_hatching()
    in_file = "input/sphere_300.normal.png"
    out_file = "output/scene hatched.png"
    process_image(in_file, out_file)

