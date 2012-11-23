#ifndef AIM_H_
#define AIM_H_

int convert(int sign, int number1, int number2) 
{
	int value = (number1 * 256) + number2;
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
