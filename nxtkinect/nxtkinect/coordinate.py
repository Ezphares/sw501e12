import math

class Vector3(object):
    def __init__(self, x = 0, y = 0, z = 0, from_kinect = None):
        if not from_kinect:
            self.x = int(x)
            self.y = int(y)
            self.z = int(z)
        
        else:
            self._kinect(from_kinect)
        
    def _kinect(self, kinect_data):
        if type(kinect_data) != KinectData:
            raise TypeError('Expected a KinectData instance')
        
        depth = kinect_data.depth_mm()
        
        self.x = int(math.sin(math.radians(kinect_data.h_deg())) * (depth / math.sin(math.radians(90.0))))
        self.y = int(-(math.sin(math.radians(kinect_data.v_deg())) * (depth / math.sin(math.radians(90.0)))))
        
        dist2 = math.sqrt(self.x * self.x + self.y * self.y)
        
        self.z = int(math.sqrt(depth * depth - dist2 * dist2))
    
    def __sub__(self, other):
        if type(other) == Vector3:
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        raise TypeError('Expected a Vector3 instance')
        
    def __add__(self, other):
        if type(other) == Vector3:
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        raise TypeError('Expected a Vector3 instance')
    
    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            return Vector3(self.x * other, self.y * other, self.z * other)
        raise TypeError('Expected int or float')
    
    def __div__(self, other):
        if type(other) == int or type(other) == float:
            return Vector3(self.x / other, self.y / other, self.z / other)
        raise TypeError('Expected int or float')
    
    def __len__(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def __str__(self):
        return str((self.x, self.y, self.z))

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

    def __str__(self):
        return 'Kinect(%f, %f, %f)' % (self.depth, self.h, self.v)
        
