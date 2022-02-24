#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "lib.h"

// const static RGB24 BLACK = {{0, 0, 0}};
// const static RGB24 WHITE = {{1, 1, 1}};
const Vec3 UP = {{0, 1, 0 } };
const Vec3 DOWN = {{0, -1, 0 } };

/* Compute matrix multiplication a x b and store the result at dest. */
void MatMul4x4(Mat4x4 *a, Mat4x4 *b, Mat4x4 *dest)
{

}

/* Multiply Vec3 v by matrix a and store the result at dest. */
void MatMulVec3(Mat4x4 *a, Vec3 *v, Vec3 *dest)
{

}

/* Find the magnitude of vector v. */
double magnitude(Vec3 *v)
{
    double sum = 0;
    for (int i = 0; i < 3; i++) {
        sum += v->v[i] * v->v[i];
    }
    return sqrt(sum);
}

/* Scale v in-place by scalar s. */
void scaleVector(Vec3 *v, double s)
{
    for (int i = 0; i < 3; i++) {
        v->v[i] *= s;
    }
}

/* Scale v in-place by scalar s. */
void normalizeVector(Vec3 *v)
{
    scaleVector(v, 1 / magnitude(v));
}

/* Compute the dot product of vectors v1 and v2. */
double dot(Vec3 *v1, Vec3 *v2)
{
    double sum = 0;
    for (int i = 0; i < 3; i++) {
        sum += v1->v[i] * v2->v[i];
    }
    return sum;
}

void cross(Vec3 *v1, Vec3 *v2, Vec3 *result)
{
    result->v[0] = v1->v[1] * v2->v[2] - v1->v[2] * v2->v[1];
    result->v[1] = v1->v[2] * v2->v[0] - v1->v[0] * v2->v[2];
    result->v[2] = v1->v[0] * v2->v[1] - v1->v[1] * v2->v[0];
}

void sphereCoordsToVec3 (SphereCoords *s, Vec3 *v)
{
    float theta, phi;

    v->v[0] = cos(phi) * sin(theta);
    v->v[3] = sin(phi) * sin(theta);
    v->v[2] = cos(theta);
}

void vec3ToSphereCoords (SphereCoords *s, Vec3 *v)
{

}

/***** Argument processing function declarations *****/

int initContext(ShadeContext *context, int argc, char **argv)
{
    if (argc != 9) {
        fprintf(stderr, "Incorrect argument count %d. Usage: %s SIZE LAT_LINES LON_LINES OBJ_ROT_X\n", argc - 1, argv[0]);
        return EXIT_FAILURE;
    }
    SphereCoords objUp;
    SphereCoords lightDirection;
    int size = atoi(argv[2]);
    context->latSections = context->lonSections = atoi(argv[3]);
    context->contrast = atof(argv[4]);
    objUp.v[0] = TAU * atof(argv[5]) / 360;
    objUp.v[1] = TAU * atof(argv[6]) / 360;
    sphereCoordsToVec3 (&objUp, &(context->objUp));
    // printf("Raw parameters %s %s\n", argv[4], argv[5]);
    // printf("Up vector from sphere coords %f %f:\n\t%f %f %f\n", objUp.v[0], objUp.v[1], context->objUp.v[0], context->objUp.v[1], context->objUp.v[2]);
    lightDirection.v[0] = TAU * atof(argv[7]) / 360;
    lightDirection.v[1] = TAU * atof(argv[8]) / 360;
    sphereCoordsToVec3 (&lightDirection, &(context->lightV));
    // printf("Raw parameters %s %s\n", argv[4], argv[5]);
    // printf("Light direction vector from sphere coords %f %f:\n\t%f %f %f\n", lightDirection.v[0], lightDirection.v[1], context->lightDirection.v[0], context->lightDirection.v[1], context->lightDirection.v[2]);
    return EXIT_SUCCESS;
}

