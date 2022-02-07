from PIL import Image
from math import *
from numpy import cross
from constants import *

   
def hatch(angle, coords, spacing = 1):
    """ Return the color at this pixel
    """
    angle = atan2(sin(angle), cos(angle))
    #angle %= pi
    
##    if angle > tau:
##        angle -= tau
##    elif angle < -tau:
##        angle += tau
    slope, rise, run = (None,)*3
    try:
        x, y = coords
        rise, run =  round(sin(angle), 4), round(cos(angle), 4)
        
##        print(slope)
        ##    print(rise, run)
##        if (abs(angle) <= pi / 4 or abs(angle) >= 3 * pi / 4):
##            # Line closer to vertical. Switch axes, x dependent on y
##            x, y = y, x
##            rise, run = run, rise
        slope = rise  / run
        #print(slope)
##        if y % (spacing) == round((x)) :
        if y % spacing == round(x * slope ) % (spacing):
            return BLACK #if slope >= 0 else GREEN
        else:
            return WHITE #if slope >= 0 else BLUE
    except: # Error condition encountered
        #print(slope, rise, run)
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
                cross_a = cross(normal, (0, sin(-pi/6), cos(-pi/6)))
                #cross_b =  #cross(normal, (0, 0, 1))
                angle_a = atan2(cross_a[1], cross_a[0])
                #angle_b = 0
##                angle = atan2(normal[1], normal[0])
##                angle = atan2(normal[1], normal[0])
                #pi/2 + atan2(origin_x - x, origin_y - y)#

                result_a = hatch(angle_a, (x, y), 4)
                #result_b = hatch(angle_b, (x, y), 4)
                px[x, y] = result_a #BLACK if BLACK in (result_a ,result_b) else WHITE 
                
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
    in_file = "input/norm_ex_wp.png"
    out_file = "output/scene hatched.png"
    process_image(in_file, out_file)

