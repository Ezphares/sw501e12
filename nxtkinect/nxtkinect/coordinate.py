import math

class Vector3(object):
    def __init__(self, x = 0, y = 0, z = 0, from_kinect = None):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        
        if (from_kinect):
            self._kinect(from_kinect)
        
    def _kinect(self, kinect_data):
        if type(kinect_data) != KinectData:
            raise ValueError()
        
        depth = kinect_data.depth_mm()
        
        self.x = int(math.sin(math.radians(kinect_data.h_deg)) * (depth / math.sin(math.radians(90.0))))
        self.y = int(-(math.sin(math.radians(kinect_data.v_deg)) * (depth / math.sin(math.radians(90.0))) - 100.0))
        
        dist2 = math.sqrt(self.x * self.x + self.y * self.y)
        
        self.z = int(math.sqrt(depth * depth - dist2 * dist2))
    
    def __sub__(self, other):
        if type(other) == Vector3:
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        
    def __add__(self, other):
        if type(other) == Vector3:
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

class KinectData(object):  
    hres = 640.0
    hfield = 57.0
    vres = 480.0
    vfield = 34.0
    
    def __init__(self, depth = 0, h = 0, v = 0):
        self.depth = float(depth)
        self.h = float(h)
        self.v = float(v)
        
    def depth_mm(self):
        return 0.1236 * math.tan(self.depth / 2843.5 + 1.1863) * 1000.0
    
    def h_deg(self):
        return self.h / (KinectData.hres / 2) * (KinectData.hfield / 2)
        
    def v_deg(self):
        return self.v / (KinectData.vres / 2) * (KinectData.vfield / 2)

        
