# hatching
Generate hatched shading from normal maps. With curved surfaces there can be some moire effects with fractal properties.
```
./hatching.py --help
usage: hatching.py [-h] [-x] [--h_spacing line_width line_gap]
                   [--v_spacing line_width line_gap] [-s]
                   filename [filename ...]

Convert a normal map image to crosshatched pixel art.

positional arguments:
  filename              An image file representing a normal map

optional arguments:
  -h, --help            show this help message and exit
  -x, --xor             Combine vertical and horizontal line fields with XOR.
                        Default is OR.
  --h_spacing line_width line_gap
                        Spacing of horizontal lines and gaps.
  --v_spacing line_width line_gap
                        Spacing of vertical lines and gaps.
  -s                    Use spherical coordinates to generate a grid.
```
```
./sphere.py --help
usage: sphere.py [-h] [-r ROTATION] [--h_spacing line_width line_gap]
                 [--v_spacing line_width line_gap] [-x] [-n] [-s]
                 size

Generate an image representing a 3d sphere.

positional arguments:
  size                  Side length of the generated image.

optional arguments:
  -h, --help            show this help message and exit
  -r ROTATION           Rotation of hatch lines in degrees.
  --h_spacing line_width line_gap
                        Spacing of horizontal lines and gaps.
  --v_spacing line_width line_gap
                        Spacing of vertical lines and gaps.
  -x, --xor             Combine vertical and horizontal line fields with XOR.
                        Default is OR.
  -n                    Output a normal map image. Default is to generate a
                        crosshatched image.
  -s                    Output a spherical grid.
```
<iframe width="1288" height="496" src="https://www.youtube.com/embed/4Kz_gQi5OWE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
