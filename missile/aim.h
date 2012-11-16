#ifndef AIM_H_
#define AIM_H_

double convert(int sign, int number1, int number2) 
{
	double value = ((double)number1 * 256) + (double)number2;
	if(sign==1)
	{
		return -value;
	}
	else
	{
		return value;
	}
}

#endif
