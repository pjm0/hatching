#include <stdio.h>
#include <math.h>
#include "lib.h"

void shadeGrayScale(RGB24 *colorOut, ShadeContext *context)
{   double angle = TAU / 12;
    Vec3 n_prime;
    // # Rotate normal around x
    n_prime.v[0] = context->normal.v[0];
    n_prime.v[1] = context->normal.v[1] * sin(angle) - context->normal.v[2] * cos(angle);
    n_prime.v[2] = (context->normal.v[1] * cos(angle) + context->normal.v[2] * sin(angle));
    scaleVector(&n_prime, 1 / magnitude(&n_prime));
    double brightness = fmax(0, dot(&(context->normal), &(context->lightDirection)));
    // brightness = (brightness - 0.5) * context->contrast + 0.5;

    colorOut->rgb[0] = (char)(255*brightness);
    colorOut->rgb[1] = (char)(255*brightness);
    colorOut->rgb[2] = (char)(255*brightness);
    // printf("\tColor out%d %d %d\n", colorOut->rgb[0], colorOut->rgb[1], colorOut->rgb[2]);
}

void shadeSphereGrid(RGB24 *colorOut, ShadeContext *context)
{   double angle = TAU / 12;
    Vec3 n_prime;
    // # Rotate normal around x
    n_prime.v[0] = context->normal.v[0];
    n_prime.v[1] = context->normal.v[1] * sin(angle) - context->normal.v[2] * cos(angle);
    n_prime.v[2] = (context->normal.v[1] * cos(angle) + context->normal.v[2] * sin(angle));
    //light_source = 1, 0, 1
    // # Rotate light source around z
    // l_x = light_source[0] * sin(angle) - light_source[1] * cos(angle)#context->normal.v[0]
    // l_y = (light_source[0] * cos(angle) + light_source[1] * sin(angle))
    // l_z = light_source[2]#

    double brightness = fmax(0, dot(&(context->normal), &(context->lightDirection)));
    brightness = (brightness - 0.5) * context->contrast + 0.5;

    double lon = atan2(n_prime.v[1], n_prime.v[0]) * context->lonSections / TAU;
    double lat = acos(n_prime.v[2]) * context->latSections / TAU;
    int on_lat_line = fabs(lat - round(lat)) < brightness;
    // printf("\tlatitude\t%f\n", lat);
    // printf("\tlatitude rounding error\t%f\n", fabs(lat - round(lat)));
    // printf("\tthreshold %f brightness %f On lat line?%s\n", 2*fabs(lat - round(lat)), brightness, on_lat_line ? "yes" : "no");

    if (on_lat_line)
    {   colorOut->rgb[0] = 0;
        colorOut->rgb[1] = 0;
        colorOut->rgb[2] = 0;
    }
    else
    {   colorOut->rgb[0] = 255;
        colorOut->rgb[1] = 255;
        colorOut->rgb[2] = 255;
    }
    // printf("\tColor out%d %d %d\n", colorOut->rgb[0], colorOut->rgb[1], colorOut->rgb[2]);
}