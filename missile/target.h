#ifndef TARGET_H_
#define TARGET_H_

typedef struct Vector3
{
	double x, y, z;
} Vector3;

typedef struct Target
{
	Vector3 pos, speed;
} Target;

Vector3 *predict_target(Target *t, double ms);
double length(Vector3 *v);
#endif

