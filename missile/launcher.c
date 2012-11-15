#include "kernel.h"
#include "kernel_id.h"
#include "ecrobot_interface.h"
#include "target.h"
#include "aim.h"
#include "math2.h"
#include <math.h>

DeclareAlarm(AlarmKinect);
DeclareCounter(CntSystem);
DeclareResource(USB_Rx);
DeclareResource(Target_Rx);

DeclareTask(TaskReset);
DeclareTask(TaskKinect);
DeclareTask(TaskAim);
DeclareTask(TaskFire);

DeclareEvent(EvResetDone);
DeclareEvent(EvTargetAcquired);
DeclareEvent(EvAimDone);

static Target target;
const static unsigned char DISCONNECT_REQ = 0xFF;
const static unsigned char COMM_STRING = 0x01;
const static unsigned char ACK_STRING = 0x02;
const static double horizontal_relation = 0.053571428571486;

// nxtOSEK hook to be invoked from an ISR in category 2
void user_1ms_isr_type2(void)
{ 
	StatusType ercd;
	
	ercd = SignalCounter(CntSystem);
	if (ercd != E_OK)
	{
		ShutdownOS(ercd);
	}
}

void ecrobot_device_initialize()
{
	ecrobot_init_usb();
}
void ecrobot_device_terminate()
{
	ecrobot_term_usb();
}
TASK(TaskReset)
{

	nxt_motor_set_speed(NXT_PORT_A, 100, 0);
	while (ecrobot_get_touch_sensor(NXT_PORT_S1) == 0);
	nxt_motor_set_speed(NXT_PORT_A, 0, 1);
	
	nxt_motor_set_speed(NXT_PORT_B, -15, 1);
	while (ecrobot_get_touch_sensor(NXT_PORT_S2) == 0);
	nxt_motor_set_count(NXT_PORT_B, 0);
	nxt_motor_set_speed(NXT_PORT_B, 15, 1);
	while (nxt_motor_get_count(NXT_PORT_B) <= 8);
	nxt_motor_set_speed(NXT_PORT_B, 0, 1);
	
	SetEvent(TaskKinect, EvResetDone);
	
	TerminateTask();
	
}

TASK(TaskKinect)
{
	unsigned short len;
	U8 data[MAX_USB_DATA_LEN];
	
	ecrobot_process1ms_usb();
	len = ecrobot_read_usb(data, 0, MAX_USB_DATA_LEN);
	ReleaseResource(USB_Rx);
	
	if (len > 0)
	{
		if (data[0] == DISCONNECT_REQ)
		{
			ecrobot_disconnect_usb();
		}
		else
		{
			int x = convert((int)data[0], (int)data[1], (int)data[2]);
			int y = convert((int)data[3], (int)data[4], (int)data[5]);
			
			GetResource(Target_Rx);
			target.pos_x = sin(x / 320 * 28.5) * (target.pos_z / sin(90));
			target.pos_y = sin(y / 320 * 21.5) * (target.pos_z / sin(90));
			target.pos_z = convert((int)data[6], (int)data[7], (int)data[8]);
			target.speed_x = convert((int)data[9], (int)data[10], (int)data[11]);
			target.speed_y = convert((int)data[12], (int)data[13], (int)data[14]);
			target.speed_z = convert((int)data[15], (int)data[16], (int)data[17]);
			ReleaseResource(Target_Rx);
						
			SetEvent(TaskAim, EvTargetAcquired);
			///send back the acknowledgment ok string
			data[0] = ACK_STRING;
			data[1] = 'o';
			data[2] = 'k';
			data[3] = 0;

			GetResource(USB_Rx);
			len = ecrobot_send_usb(data, 0, 4);
			ReleaseResource(USB_Rx);		
		}
	}
	
	ReleaseResource(USB_Rx);
	TerminateTask();

	}

TASK(TaskAim)
{
	WaitEvent(EvTargetAcquired);
	
	/* Horizontal aim */

	//Hardcoded position of tower
	int center_x = 0;
	
	int delta_x = target.pos_x - center_x;

	//Take the arctangens of delta_z/delta_x, and calculate degrees.
	double radians = atan2(target.pos_z, delta_x);
	double raw_degrees = radians * 180 / 3.1415926;
	int rounded_degrees = ceil (raw_degrees);
	
	//set position
	if (rounded_degrees >= 0)
	{		
		nxt_motor_set_speed(NXT_PORT_A, 100, 1);
		nxt_motor_set_count(NXT_PORT_A, 0);
		while (nxt_motor_get_count(NXT_PORT_A) <= (rounded_degrees * horizontal_relation));
		nxt_motor_set_speed(NXT_PORT_A, 0, 1);
	}
	else
	{
		nxt_motor_set_speed(NXT_PORT_A, -100, 1);
		nxt_motor_set_count(NXT_PORT_A, 0);
		while (nxt_motor_get_count(NXT_PORT_A) >= -(rounded_degrees * horizontal_relation));
		nxt_motor_set_speed(NXT_PORT_A, 0, 1);
	}
		

	/* Vertical aim */
	double g = -9.81;
	double v = 41;
	
	double tan_angle_base = ( pow(v,2) - 2*g*(target.pos_y + .5*g*( pow(target.pos_z,2) / pow(v,2))));
	double tan_angle_vpos = v + pow(tan_angle_base, .5);
	double tan_angle_divpos = tan_angle_vpos / (g*target.pos_z/v);
	double degrees_pos = atan(tan_angle_divpos) * 180 / 3.1415926;

	double tan_angle_vneg = v - pow(tan_angle_base, .5);
	double tan_angle_divneg = tan_angle_vneg / (g*target.pos_z/v);
	double degrees_neg = atan(tan_angle_divneg) * 180 / 3.1415926;
	
	double vertical = min(degrees_pos, degrees_neg);
	
	nxt_motor_set_count(NXT_PORT_B, 0);
	nxt_motor_set_speed(NXT_PORT_B, 15, 1);
	while (nxt_motor_get_count(NXT_PORT_B) <= vertical);
	nxt_motor_set_speed(NXT_PORT_B, 0, 1);
	
	
	TerminateTask();
}

TASK(TaskFire)
{
	WaitEvent(EvAimDone);
	
	nxt_motor_set_speed(NXT_PORT_C, 100, 1);
	nxt_motor_set_count(NXT_PORT_C, 0);
	while(nxt_motor_get_count(NXT_PORT_C) < 100);
	nxt_motor_set_speed(NXT_PORT_C, 0, 1);
	
	TerminateTask();
}
