/* Horizontal aim */
double prediction = 2000;
Vector3 *t = predict_target(&target, prediction);

double depth = length(t);

prediction -= depth / v;
prediction -= cannon_delay;

if (SetRelAlarm(AlarmFire, (int)prediction, 0) != E_OK)
{
	display_string("ERR");
	display_update();
}

//Adjust for height difference of tower and kinect
t->y -= 100;

//extended Pythagoras for 3D, gets depth in mm

//Take the arctangens of delta_z/delta_x, and calculate degrees.
double radians = asin(t->x / depth);
double raw_degrees = -radtodeg(radians);


/* Vertical aim */
double g = -98.1f;

double tan_angle_base = ((v * v) - 2.0f * g * (t->y + .5f * g * (depth * depth) / (v * v)));
double tan_angle_vpos = v + sqrt(tan_angle_base);
double tan_angle_divpos = tan_angle_vpos / (g * depth / v);
double degrees_pos = radtodeg(atan(tan_angle_divpos));

double tan_angle_vneg = v - sqrt(tan_angle_base);
double tan_angle_divneg = tan_angle_vneg / (g * depth / v);
double degrees_neg = radtodeg(atan(tan_angle_divneg));

double vertical = max(degrees_pos, degrees_neg);