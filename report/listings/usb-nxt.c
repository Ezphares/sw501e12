GetResource(Target_Rx);
target.pos.x = convert((int)data[0], (int)data[1], (int)data[2]);
target.pos.y = convert((int)data[3], (int)data[4], (int)data[5]);
target.pos.z = convert((int)data[6], (int)data[7], (int)data[8]);

target.speed.x = convert((int)data[9], (int)data[10], (int)data[11]);
target.speed.y = convert((int)data[12], (int)data[13], (int)data[14]);
target.speed.z = convert((int)data[15], (int)data[16], (int)data[17]);
ReleaseResource(Target_Rx);

SetEvent(TaskAim, EvTargetAcquired);