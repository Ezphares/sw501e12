#include "math2.h"
#include <math.h>

double min (double a, double b)
{
	if (a <= b)
		return a;
	else 
		return b;
}

double max(double a, double b)
{
	if (a >= b)
		return a;
	else 
		return b;
}

double radtodeg(double a)
{
	return a / PI * 180;
}

double degtorad(double a)
{
	return a * PI / 180;
}

double normalized_depth(double a)
{
	return 0.1236f * tan(a / 2843.5f + 1.1863f) * 1000.0f;
}
