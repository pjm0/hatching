/***** Structs *****/

typedef struct ScreenXY {
    int x, y;
} ScreenCoords;

typedef struct Vec3 {
    double v[3];
} Vec3;

typedef struct Mat4x4 {
    double m[4][4];
} Mat4x4;

typedef struct RGB24 {
    unsigned char rgb[3];
} RGB24;

/***** Constants *****/


#define TAU (2 * M_PI)

/***** Library function declarations *****/

/* Compute matrix multiplication a x b and store the result at dest. */
void MatMul4x4(Mat4x4 *a, Mat4x4 *b, Mat4x4 *dest);

/* Multiply Vec3 v by matrix a and store the result at dest. */
void MatMulVec3(Mat4x4 *a, Vec3 *v, Vec3 *dest);

/* Find the magnitude of vector v. */
double magnitude(Vec3 *v);

/* Scale v in-place to make it a unit vector. */
void normalize(Vec3 *v);

double dot(Vec3 *v1, Vec3 *v2);

void cross(Vec3 *v1, Vec3 *v2, Vec3 *result);
