#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "lib.h"
#include "shader.h"

const Vec3 UP = {{0, 1, 0}};
const Vec3 DOWN = {{0, -1, 0}};

int main(int argc, char **argv)
{
    ShadeContext context;
    SphereCoords objUp;
    SphereCoords lightDirection;
    int size = atoi(argv[2]);
    context.latSections = context.lonSections = atoi(argv[3]);
    if (argc >= 3) {
        context.contrast = atof(argv[4]);
    } else {
        context.contrast = 0.5;
    }
    if (argc >= 7) {
        objUp.v[0] = atof(argv[5]);
        objUp.v[1] = atof(argv[6]);
        sphereCoordsToVec3 (&objUp, &(context.objUp));
        // printf("Raw parameters %s %s\n", argv[4], argv[5]);
        // printf("Up vector from sphere coords %f %f:\n\t%f %f %f\n", objUp.v[0], objUp.v[1], context.objUp.v[0], context.objUp.v[1], context.objUp.v[2]);
    } else {
        context.objUp = UP;
    }
    if (argc >= 9) {
        lightDirection.v[0] = atof(argv[7]);
        lightDirection.v[1] = atof(argv[8]);
        sphereCoordsToVec3 (&lightDirection, &(context.lightDirection));
        // printf("Raw parameters %s %s\n", argv[4], argv[5]);
        // printf("Light direction vector from sphere coords %f %f:\n\t%f %f %f\n", lightDirection.v[0], lightDirection.v[1], context.lightDirection.v[0], context.lightDirection.v[1], context.lightDirection.v[2]);
    } else {
        context.lightDirection = DOWN;
    }
    
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
