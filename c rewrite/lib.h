
/***** Structs *****/

typedef struct ScreenXY {
    int x, y;
} ScreenCoords;

typedef struct Vec3 {
    double v[3];
} Vec3;

typedef struct SphereCoords {
    double v[2];
} SphereCoords;

typedef struct Mat4x4 {
    double m[4][4];
} Mat4x4;

typedef struct RGB24 {
    unsigned char rgb[3];
} RGB24;

typedef struct RGB48 {
    short rgb[3];
} RGB48;

typedef struct ShadeContext {
    int latSections;
    int lonSections;
    double brightness;
    double contrast;
    Vec3 normal;
    Vec3 lightV;
    Vec3 objUp;
} ShadeContext;

typedef struct Camera {
    float focalDist;
    Vec3 eye;
    Vec3 gazePoint;
    Mat4x4 camToWorld;
    Mat4x4 worldToCam;
} Camera;

typedef struct PpmWrapper {
    FILE *f;
    int width, height, maxVal;
} PpmWrapper;

/***** Constants *****/

// const Vec3 UP = {{0, 1, 0 }};
// const Vec3 DOWN = {{0, -1, 0 }};
// const RGB24 WHITE = {{255, 255, 255 }};
// const RGB24 BLACK = {{0, 0, 0 }};

#define TAU (2 * M_PI)

/***** Library function declarations *****/

/* Compute matrix multiplication a x b and store the result at dest. */
void MatMul4x4(Mat4x4 *a, Mat4x4 *b, Mat4x4 *dest);

/* Multiply Vec3 v by matrix a and store the result at dest. */
void MatMulVec3(Mat4x4 *a, Vec3 *v, Vec3 *dest);

/* Find the magnitude of vector v. */
double magnitude(Vec3 *v);

/* Scale v in-place by scalar s. */
void scaleVector(Vec3 *v, double s);

/* Scale v in-place to make it a unit vector. */
void normalize(Vec3 *v);

double dot(Vec3 *v1, Vec3 *v2);

void cross(Vec3 *v1, Vec3 *v2, Vec3 *result);

void rotateX(double rotation, Vec3 *orig, Vec3 *new);

void rotateY(double rotation, Vec3 *orig, Vec3 *new);

void rotateZ(double rotation, Vec3 *orig, Vec3 *new);

void sphereCoordsToVec3 (SphereCoords *s, Vec3 *v);

void vec3ToSphereCoords (SphereCoords *s, Vec3 *v);

/***** Shader function declarations *****/

void rgbToNormal(RGB24 *color, Vec3 *normal, int maxVal);

void rgb48ToNormal(RGB48 *color, Vec3 *normal, int maxVal);

double getBrightness(Vec3 *normal, Vec3 *lightV, double contrast);

void shadeRandDither(RGB24 *colorOut, ShadeContext *context);

void shadeSphereGrid(RGB24 *colorOut, ShadeContext *context);

void shadeGrayScale(RGB24 *colorOut, ShadeContext *context);

/***** Argument processing function declarations *****/

int initContext(ShadeContext *context, int argc, char **argv);

/***** Image processing function declarations *****/

int loadPpmRead(PpmWrapper *img, char *filename);

int loadPpmWrite(PpmWrapper *img, char *filename);

void processNormalMap(char *inFN, char *outFN, ShadeContext *context, void *shader(SphereCoords *, Vec3 *)) ;

/***** Camera function declarations (camera.c) *****/

void initCamera(Camera *c, float focalDist, Vec3 eye, Vec3 gazePoint);