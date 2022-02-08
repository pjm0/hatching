from bresenham import bresenham as line_points
from numpy import gcd, lcm, sin, cos
from math import tau

_cache = {}
def line_field(run, rise, spacing = 1):
    """ REQ: run and rise not both zero
    """
    if run < 0:
        rise, run = -rise, -run
    cd = gcd(abs(rise), abs(run))
    rise, run = rise // cd, run // cd
    if rise == 0: # Horizontal
        run = 2
    elif run == 0: # Vertical
        rise = 2
    elif rise == run: # 45 deg upwards
        rise = run = 2
    elif rise == -run: # 45 deg downwards
        run = 2
        rise = -run

    height = max(1, abs(rise))
    width = max(1, abs(run))
    if (rise, run, spacing) in _cache:
        return _cache[rise, run, spacing]
    points = set()#tuple(line_points(0, 0, run, rise))
    if height > width: #Line closer to vertical, stacking will be horizontal
        width  = lcm(width, spacing+1)
        for x in range(0, width, spacing+1):
            for point in line_points(0, 0, run, rise):
                points.add(((point[0] + x) % width, point[1] % height))
    else: # Line closer to horizontal, stacking will be vertical
        height = lcm(height, spacing+1)
        for y in range(0, height, spacing+1):
            for point in line_points(0, 0, run, rise):
                points.add((point[0] % width, (point[1] + y) % height))
    def f(x, y):
        return (x % width, y % height) in points
    _cache[rise, run, spacing] = f
    return f

if __name__ == "__main__":
##    from test_hatching import test_hatching
##    test_hatching()
    STEPS = 16
    for n in range(STEPS):
        x, y = int(STEPS * cos(tau*n/STEPS)), int(STEPS * sin(tau*n/STEPS))
        line_field(x, y)
