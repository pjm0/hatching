#include "lib.h"

void initCamera(Camera *c, float focalDist, Vec3 *eye, Vec3 *gazePoint)
{
    c->eye = *eye;
    c->gazePoint = *gazePoint;
    c->focalDist = focalDist;

    Mat4x4 *c2w = &(c->camToWorld);
    Mat4x4 *w2c = &(c->worldToCam);

}