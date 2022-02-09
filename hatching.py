from PIL import Image
from math import *
from numpy import cross
from constants import *

def hatch(angle, coords, spacing = 1):
    """ Return the color at this pixel
    """
    angle = atan2(sin(angle), cos(angle))
    x, y = coords
    rise, run =  round(sin(angle), 12), -round(cos(angle), 12)
    if abs(rise) > abs(run):
        x, y = y, -x
        rise, run = -run, rise
    slope = rise  / run
    if y % (spacing+1) == (round(x * slope ))% (spacing+1):
        return BLACK
    else:
        return WHITE


    
def process_image(in_file, out_file, f):
    im = Image.open(in_file)
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
                normal = [n -128 for n in pixel[:3]]
                #normal[1] = -normal[1]
                #cross_p = cross((0, normal[1], normal[2]), (normal[0], 0, normal[2]))
                #cross_a = cross(normal, (0, sin(-pi/6), cos(-pi/6)))
                #cross_b =  #cross(normal, (0, 0, 1))
                #angle_a = atan2(cross_a[1], cross_a[0])
                #angle_a = 3#atan2(normal[1], normal[0])
                #angle_b = atan2(normal[0], normal[1])
                #angle_b = atan2(normal[0], -normal[1])
                #angle_b = 0
##                angle = atan2(normal[1], normal[0])
##                angle = atan2(normal[1], normal[0])
                #pi/2 + atan2(origin_x - x, origin_y - y)#
                angle = f(normal)
                result_a = hatch(angle, (x, y), 3)
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
##    test_hatching("
    def f(normal):
        return atan2(normal[0], -normal[1])
    def f2(normal):
        product = cross(normal, UP)
        return atan2(product[0], -product[1])
    def f3(normal):
        product = cross(normal, S)
        return atan2(product[0], -product[1])
    def f4(normal):
        product = cross(normal, SW)
        return atan2(product[0], -product[1])
    name = "example_normals_xs"
    in_file = "input/{}.png".format(name)
    out_file = "output/{}.hatched.png".format(name)
    process_image(in_file, out_file, f4)

