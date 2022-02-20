#! /usr/bin/python3

import os
FRAMES = 360
THREADS = 4
for i in range(FRAMES):
    t = i / FRAMES
    stream = os.popen('./hatching frame.{:04d}.ppm 720 {} {} 30 {} {} 45 {}'.format(i, i, t, i, i, "&" if i % THREADS == 0 else ""))
    output = stream.read()
    print(output)
stream = os.popen("ffmpeg -y -stream_loop 20 -r 60 -i frame.%04d.ppm -c:v libx264 -vf fps=60 -pix_fmt yuv420p sphere.mp4".format())
output = stream.read()
print(output)
print(os.popen("vlc sphere.mp4").read())
