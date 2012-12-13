//Alarm that starts the task responsible for polling
DeclareAlarm(AlarmKinect);
//Alarm that starts the Fire task
DeclareAlarm(AlarmFire);
//System counter to keep track of time
DeclareCounter(CntSystem);
//Shared resource facilitating USB communication
DeclareResource(USB_Rx);
//Shared resource containing info about the Target
DeclareResource(Target_Rx);

//Task to reset turret position during initialization
DeclareTask(TaskReset);
//Task responsible for polling for coordinates from USB
DeclareTask(TaskKinect);
//Task responsible for predicting target position and aiming
DeclareTask(TaskAim);
//Task responsible for firing projectile
DeclareTask(TaskFire);

//Event signaling that it's time to poll for coordinates
DeclareEvent(EvResetDone);
//Event signaling that it's time to aim
DeclareEvent(EvTargetAcquired);
//Even fired to start TaskFire
DeclareEvent(EvAimDone);

//Target struct. Contains 3d vector with info about target position and speed
static Target target;
//USB connection messages
const static unsigned char DISCONNECT_REQ = 0xFF;
const static unsigned char COMM_STRING = 0x01;
const static unsigned char ACK_STRING = 0x02;
//Relation between servor motor and gear system to move horizontally
const static double horizontal_relation = 0.053571428571486;
//Speed of projectile
const static double v = 450.0f;
//Delay used to compute when the cannon should fire
const static double cannon_delay = 350.0f;