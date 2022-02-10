# hatching
Generate hatched shading from normal maps. With curved surfaces there can be some moire effects with fractal properties.

* ./sphere.py 300 1 1 
* ./hatching.py --help
usage: hatching.py [-h] [-x] [--h_spacing line_width line_gap]
                   [--v_spacing line_width line_gap]
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
* ./sphere.py --help
usage: sphere.py [-h] [--h_spacing line_width line_gap]
                 [--v_spacing line_width line_gap] [-x] [-n]
                 size

Generate an image representing a 3d sphere.

positional arguments:
  size                  Side length of the generated image.

optional arguments:
  -h, --help            show this help message and exit
  --h_spacing line_width line_gap
                        Spacing of horizontal lines and gaps.
  --v_spacing line_width line_gap
                        Spacing of vertical lines and gaps.
  -x, --xor             Combine vertical and horizontal line fields with XOR.
                        Default is OR.
  -n                    Output a normal map image. Default is to generate a
                        crosshatched image.
