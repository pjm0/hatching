#include <math.h>
#include "lib.h"

// const static RGB24 BLACK = {{0, 0, 0}};
// const static RGB24 WHITE = {{1, 1, 1}};

/* Compute matrix multiplication a x b and store the result at dest. */
void MatMul4x4(Mat4x4 *a, Mat4x4 *b, Mat4x4 *dest) {

}

/* Multiply Vec3 v by matrix a and store the result at dest. */
void MatMulVec3(Mat4x4 *a, Vec3 *v, Vec3 *dest) {

}

/* Find the magnitude of vector v. */
double magnitude(Vec3 *v) {
    double sum = 0;
    for (int i = 0; i < 3; i++) {
        sum += v->v[i] * v->v[i];
    }
    return sqrt(sum);
}

/* Scale v in-place by scalar s. */
void scaleVector(Vec3 *v, double s) {
    for (int i = 0; i < 3; i++) {
        v->v[i] *= s;
    }
}

/* Compute the dot product of vectors v1 and v2. */
double dot(Vec3 *v1, Vec3 *v2) {
    double sum = 0;
    for (int i = 0; i < 3; i++) {
        sum += v1->v[i] * v2->v[i];
    }
    return sum;
}

void cross(Vec3 *v1, Vec3 *v2, Vec3 *result) {
    result->v[0] = v1->v[1] * v2->v[2] - v1->v[2] * v2->v[1];
    result->v[1] = v1->v[2] * v2->v[0] - v1->v[0] * v2->v[2];
    result->v[2] = v1->v[0] * v2->v[1] - v1->v[1] * v2->v[0];
}

void sphereCoordsToVec3 (SphereCoords *s, Vec3 *v) {
    float theta, phi;
    theta = TAU * s->v[0] / 360;
    phi = TAU * s->v[1] / 360;

    v->v[0] = cos(phi) * sin(theta);
    v->v[3] = sin(phi) * sin(theta);
    v->v[2] = cos(theta);
}

void vec3ToSphereCoords (SphereCoords *s, Vec3 *v) {

}
