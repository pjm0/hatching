#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "lib.h"
#include "shader.h"

const Vec3 UP = {{0, 1, 0}};
const Vec3 DOWN = {{0, -1, 0}};

int main(int argc, char **argv)
{
    const int size = atoi(argv[1]);
    const int sections = atoi(argv[2]);
    float contrast;
    if (argc >= 3) {
        contrast = atof(argv[3]);
    } else {
        contrast = 0.5;
    }
    char filename[100];
    sprintf(filename, "sphere-%d-%d-%.2f.ppm", size, sections, contrast);
    FILE *fp = fopen(filename, "wb"); /* b - binary mode */
    ShadeContext context;
    context.latSections = sections;
    context.lonSections = sections;
    context.contrast = contrast;
    context.lightDirection = DOWN;
    context.objUp = UP;
    (void) fprintf(fp, "P6\n%d %d\n255\n", size, size);
    for (int j = 0; j < size; ++j) {
        printf("Row %d / %d\n", j, size);
        double y = -(2*j/(double)size-1);
        double y_sq = y * y;
        for (int i = 0; i < size; ++i)
        {
            double x = 2*i/(double)size - 1;
            double x_sq = x * x;
            //static unsigned char color[3];
            RGB24 color;

            if (x_sq + y_sq < 1) {

                context.normal.v[0] = x;
                context.normal.v[1] = y;
                context.normal.v[2] = sqrt(1-x_sq - y_sq );

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
