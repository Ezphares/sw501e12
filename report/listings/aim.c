/* Horizontal aim */

//How many miliseconds ahead should the aim predict
double prediction = 2000;
//Save prediction based on information received from USB in a 3d vector
Vector3 *t = predict_target(&target, prediction);

double depth = length(t);

//Adjust firing time according to targets position and the cannon delay
prediction -= depth / v;
prediction -= cannon_delay;

//Set alarm relative to the computed time
SetRelAlarm(AlarmFire, (int)prediction, 0)

//Adjust for height difference of tower and kinect in mm
t->y -= 100;

//Take the arctangens of delta_z/delta_x, and calculate degrees for motors.
double radians = asin(t->x / depth);
double raw_degrees = -radtodeg(radians);


/* Vertical aim */

//Gravitational acceleration on Earth.
double g = -98.1f;

//Calculate angles according to math theory
double tan_angle_base = ((v * v) - 2.0f * g * (t->y + .5f * g * (depth * depth) / (v * v)));
double tan_angle_vpos = v + sqrt(tan_angle_base);
double tan_angle_divpos = tan_angle_vpos / (g * depth / v);
double degrees_pos = radtodeg(atan(tan_angle_divpos));

double tan_angle_vneg = v - sqrt(tan_angle_base);
double tan_angle_divneg = tan_angle_vneg / (g * depth / v);
double degrees_neg = radtodeg(atan(tan_angle_divneg));

double vertical = max(degrees_pos, degrees_neg);