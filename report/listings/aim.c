/* Prediction */
double prediction = 2000;
Vector3 *t = predict_target(&target, prediction);

/* Adjustments */
t->y -= 100;

double depth = length(t);

prediction -= depth / v;
prediction -= cannon_delay;
SetRelAlarm(AlarmFire, (int)prediction, 0)

/* Horizontal aim */
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