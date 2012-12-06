DeclareAlarm(AlarmKinect);
DeclareAlarm(AlarmFire);
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
const static double v = 450.0f;
const static double cannon_delay = 350.0f;