from bresenham import bresenham as line_points
from numpy import gcd, lcm, sin, cos
from math import tau

_cache = {}
def line_field(run, rise, spacing = 1):
    """ REQ: run and rise not both zero
    """
##    cd = gcd(width, abs(rise))
##    if gcd(width, abs(rise)):
##    print("line_field({}, {})".format(run, rise))
    if run < 0:
        rise, run = -rise, -run
    cd = gcd(abs(rise), abs(run))
##    print("gcd", cd)
##    print("run, rise before", run, rise)
    rise, run = rise // cd, run // cd
    if rise == 0:
        width = run = abs(run)
        height = 1
    elif run == 0:
        height= rise = abs(rise)
        width = 1
    else:
        height = abs(rise)
        width = abs(run)
    if (rise, run, spacing) in _cache:
        return _cache[rise, run, spacing]
##    print("run, rise, width, height after", run, rise, width, height)
##    print("line_points({}, {}, {}, {})".format(0, 0, run, rise))
    points = set()#tuple(line_points(0, 0, run, rise))
    if height > width: #Line closer to vertical, stacking will be horizontal
##        print("Line closer to vertical, stacking will be horizontal")
##        print("width, lcm(width, spacing+1)", width, lcm(width, spacing+1))
        width  = lcm(width, spacing+1)
        for x in range(0, width, spacing+1):
            for point in line_points(0, 0, run, rise):
                points.add(((point[0] + x) % width, point[1] % height))
    else: # Line closer to horizontal, stacking will be vertical
##        print("Line closer to horizontal, stacking will be vertical")
##        print("height, lcm(height, spacing+1)", height, lcm(height, spacing+1))
        height = lcm(height, spacing+1)
        for y in range(0, height, spacing+1):
            for point in line_points(0, 0, run, rise):
                points.add((point[0] % width, (point[1] + y) % height))
    def f(x, y):
        return (x % width, y % height) in points
    _cache[rise, run, spacing] = f
    return f
##STEPS = 12
##for n in range(STEPS):
##    x, y = int(12 * cos(tau*n/STEPS)), int(12 * sin(tau*n/STEPS))
##    print(x, y, list(line_field(x, y)))
##    print()
