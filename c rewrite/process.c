#include <stdio.h>
#include <stdlib.h>
#include "lib.h"

#define PPM_HEADER "P6\n%d %d\n%d\n"
#define CONTRAST 0.1


int loadPpmRead(PpmWrapper *img, char *filename)
{
    img->f = fopen(filename, "rb");
    if (!img->f) {
        return 0;
    } else if (fscanf(img->f, PPM_HEADER, &(img->width), &(img->height), &(img->maxVal))<0) {
        return 0;
    }
    printf(PPM_HEADER, img->width, img->height, img->maxVal);
    return 1;
}

int loadPpmWrite(PpmWrapper *img, char *filename)
{
    img->f = fopen(filename, "wb");

    printf(PPM_HEADER, img->width, img->height, img->maxVal);
    if (!img->f) {
        return 0;
    } else if (fprintf(img->f, PPM_HEADER, img->width, img->height, img->maxVal)<0) {
        return 0;
    }
    return 1;
}


void batchProcessNormals(char *outFN)
{

}

int processNormals(ShadeContext *context, char *normalFN, char *lightFN, char *outFN)
{
    PpmWrapper normalMap, lightMap, output;

    int normalFileOK = loadPpmRead(&normalMap, normalFN);
    output.height = normalMap.height;
    output.width = normalMap.width;
    output.maxVal = 255;
    int outputFileOK = loadPpmWrite(&output, outFN);
    if (!(normalFileOK && outputFileOK)) {
        return 0;
    }
    int lightMapFileOK = loadPpmRead(&lightMap, lightFN);

    for (int j = 0; j < normalMap.height; ++j) {
        for (int i = 0; i < normalMap.width; ++i) {
            int n;
            context->contrast = CONTRAST;
            RGB24 normColor, lightColor, outColor;
            RGB48 normColor48, lightColor48;
            double brightness;
            if (normalMap.maxVal > 255) {
                fread(&(normColor48.rgb), 2, 3, normalMap.f);
                rgb48ToNormal(&normColor48, &(context->normal), normalMap.maxVal);
            } else {
                fread(&(normColor.rgb), 1, 3, normalMap.f);
                rgbToNormal(&normColor, &(context->normal), normalMap.maxVal);
            }
            if (lightMapFileOK) {
                if (lightMap.maxVal > 255) {
                    fread(&(lightColor48.rgb), 2, 3, lightMap.f);
                    context->brightness = (lightColor48.rgb[0]+lightColor48.rgb[1]+lightColor48.rgb[2]) / 3 / lightMap.maxVal;
                } else {
                    fread(&(lightColor.rgb), 2, 3, lightMap.f);
                    context->brightness = (lightColor.rgb[0]+lightColor.rgb[1]+lightColor.rgb[2]) / 3 / lightMap.maxVal;
                }
            } else {
                context->brightness = getBrightness(&(context->normal), &(context->lightV), context->contrast);
            }
            shadeSphereGrid(&outColor, context);
            fwrite(&(outColor.rgb), 1, 3, output.f);
            // printf("Norm (%d %d %d) Light (%d %d %d) out (%d %d %d)\n", normColor.rgb[0], normColor.rgb[1], normColor.rgb[2],
            //        lightColor.rgb[0], lightColor.rgb[1], lightColor.rgb[2],
            //        outColor.rgb[0], outColor.rgb[1], outColor.rgb[2]);
        }
    }
    fflush(output.f);
    fclose(normalMap.f);
    fclose(output.f);
    if (lightMap.f) fclose(lightMap.f);
    return 0;
}

int main(int argc, char **argv)
{
    ShadeContext context;
    context.latSections = 100;
    context.lonSections = 2;
    context.lightV.v[0] = 1;
    context.lightV.v[1] = 0;
    context.lightV.v[2] = 0;
    normalize(&(context.lightV));
    if (argc == 3) {
        processNormals(&context, argv[1], (char *)NULL, argv[2]);
    } else if (argc == 4) {
        processNormals(&context, argv[1], argv[2], argv[3]);
    }
}