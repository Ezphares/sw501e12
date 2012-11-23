#include "target.h"
#include <stdlib.h>
#include <math.h>

Vector3 *predict_target(Target *t, double ms)
{
	Vector3 *r = (Vector3 *)malloc(sizeof(Vector3));
	r->x = t->pos.x + t->speed.x * (ms / 1000);
	r->y = t->pos.y + t->speed.y * (ms / 1000);
	r->z = t->pos.z + t->speed.z * (ms / 1000);
	return r;
}

double length(Vector3 *v)
{
	return sqrt(v->x * v->x + v->y * v->y + v->z * v->z);
}
