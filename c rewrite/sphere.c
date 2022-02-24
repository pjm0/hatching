#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "lib.h"

int main(int argc, char **argv)
{
    ShadeContext context;
    if (initContext(&context, argc, argv) == EXIT_FAILURE) {
        return EXIT_FAILURE;
    }
    int size = atoi(argv[2]);
    char *filename = argv[1];/*[100];
    sprintf(filename, "sphere %d %d %.2f %.2f %.2f %.2f %.2f.ppm",
            size, context.latSections, context.contrast, objUp.v[0], objUp.v[1], lightDirection.v[0], lightDirection.v[1]);*/
    printf("%s\n", filename);
    FILE *fp = fopen(filename, "wb"); /* b - binary mode */

    (void) fprintf(fp, "P6\n%d %d\n255\n", size, size);
    for (int j = 0; j < size; ++j) {
        // printf("Row %d / %d\n", j, size);
        double y = -(2*j/(double)size-1);
        double y_sq = y * y;
        for (int i = 0; i < size; ++i) {
            double x = 2*i/(double)size - 1;
            double x_sq = x * x;
            //static unsigned char color[3];
            RGB24 color;
            if (x_sq + y_sq < 1) {
                context.normal.v[0] = x;
                context.normal.v[1] = y;
                context.normal.v[2] = sqrt(1-x_sq - y_sq );
                //shadeGrayScale(&color, &context);
                shadeSphereGrid(&color, &context);
            } else {
                color.rgb[0] = 0;
                color.rgb[1] = 0;
                color.rgb[2] = 0;
            }
            (void) fwrite(&(color.rgb), 1, 3, fp);
        }
    }
    (void) fclose(fp);
    return EXIT_SUCCESS;
}
