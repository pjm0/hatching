#include <stdio.h>
#include "lib.h"

#define PPM_HEADER "P6\n%d %d\n%d\n"
#define CONTRAST .8

void *processNormals(char *normalFN, char *lightFN, char *outFN)
{
    int nWidth, nHeight, nMaxVal, lWidth, lHeight, lMaxVal;
    FILE *normalMap, *lightMap, *output;
    output = fopen(outFN, "wb"); /* b - binary mode */
    normalMap = fopen(normalFN, "rb");
    fscanf(normalMap, PPM_HEADER, &nWidth, &nHeight, &nMaxVal);
    if (lightFN) {
        lightMap = lightFN ? fopen(lightFN, "rb") : NULL;
        fscanf(lightMap, PPM_HEADER, &lWidth, &lHeight, &lMaxVal);
    } else {
        lightMap = NULL;
    }
    printf("%d %d %d %d %d %d\n", nWidth, nHeight, nMaxVal, lWidth, lHeight, lMaxVal);
    (void) fprintf(output, "P6\n%d %d\n%d\n", nWidth, nHeight, nMaxVal);
    for (int j = 0; j < nHeight; ++j) {
        // printf("Row %d / %d\n", j, size);
        //double y = -(2*j/(double)sizeH-1);
        for (int i = 0; i < nWidth; ++i) {
            //double x = 2*i/(double)sizeW - 1;
            int n;
            ShadeContext context;
            context.latSections = 12;
            context.lightV.v[0] = 1;
            context.lightV.v[1] = 0;
            context.lightV.v[2] = 0;
            normalize(&(context.lightV));
            context.contrast = CONTRAST;
            RGB24 normColor, lightColor, outColor;
            RGB48 normColor48, lightColor48;
            double brightness;
            if (nMaxVal > 255) {
                fread(&(normColor48.rgb), 2, 3, normalMap);
                rgb48ToNormal(&normColor48, &(context.normal), nMaxVal);
            } else {
                fread(&(normColor.rgb), 1, 3, normalMap);
                rgbToNormal(&normColor, &(context.normal), nMaxVal);
            }
            if (lightMap) {
                if (lMaxVal > 255) {
                    fread(&(lightColor48.rgb), 2, 3, lightMap);
                    context.brightness = (lightColor48.rgb[0], lightColor48.rgb[1], lightColor48.rgb[2]) / 3 / lMaxVal;
                } else {
                    fread(&(lightColor.rgb), 2, 3, lightMap);
                    context.brightness = (lightColor.rgb[0], lightColor.rgb[1], lightColor.rgb[2]) / 3 / lMaxVal;
                }
            } else {
                context.brightness = getBrightness(&(context.normal), &(context.lightV), context.contrast);
            }
            shadeSphereGrid(&outColor, &context);
            (void) fwrite(&(outColor.rgb), 1, 3, output);
            // (void) fwrite(&(outColor.rgb), 1, 3, stdout;
        }
    }
    fflush(output);
    (void) fclose(output);
}

int main(int argc, char **argv)
{
    if (argc == 3) {
        processNormals(argv[1], (char *)NULL, argv[2]);
    } else if (argc == 4) {
        processNormals(argv[1], argv[2], argv[3]);
    }
}