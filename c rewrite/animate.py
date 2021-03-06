#! /usr/bin/python3
import os
from math import log10, cos, pi
FRAMES = 10
THREADS = 4
FRAME_RATE = 5
SIZE = 10000

def linear_interpolator(initial, final):
    return lambda t: initial + (final - initial) * t

def log10_interpolator(initial, final):
    return lambda t: initial * 10 ** (t * (log10(final) - log10(initial)))

def cosine_interpolator(initial, final):
    return lambda t: initial + 0.5 * (final - initial) * (1-cos(pi * t))
initial_values = [2**9, 0.5, -90, 15, 0, 15]
final_values = [2**15, 0.5, 90, -15, 720, -15]
interpolators = [log10_interpolator,
                 cosine_interpolator,
                 linear_interpolator,
                 linear_interpolator,
                 linear_interpolator,
                 linear_interpolator]
os.popen("rm frame.*.ppm")
for i in range(FRAMES):
    t = i / FRAMES
    a = i / 10
    params = [f(initial, final)(t) for f, initial, final in zip(interpolators, initial_values, final_values)]

    stream = os.popen('./hatching frame.{:04d}.ppm {} {} {} {} {} {} {}'.format(i, SIZE, *params))
    output = stream.read()
    print(output)
animate = "ffmpeg -y -r {0} -i frame.%04d.ppm -c:v libx264 -vf fps={0} -pix_fmt yuv420p sphere.mkv; rm frame.*.ppm".format(FRAME_RATE)
stream = os.popen(animate).read()
