/***** Structs *****/

typedef struct ShadeContext {
    int latSections;
    int lonSections;
    double contrast;
    Vec3 normal;
    Vec3 lightDirection;
    Vec3 objUp;
} ShadeContext;

/***** Shader function declarations *****/

void shadeSphereGrid(RGB24 *colorOut, ShadeContext *context);