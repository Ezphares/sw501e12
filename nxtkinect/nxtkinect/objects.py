'''

'''
from nxtkinect.coordinate import Vector3

class DetectedObject(object):
    offset_x = -320
    offset_y = -240
    offset_z = 0
    
    def __init__(self, start):
        self.coordinates = []
        self.age = 0
        self.start = start
        self.end = 0
        
    def get_motion(self):
        motion_set = [self.coordinates[i] - self.coordinates[i-1]
                      for i in range(1, len(self.coordinates))]
        
        motion = Vector3()
        for m in motion_set:
            motion += m
             
        dt = self.end - self.start
        s = dt.total_seconds()
        
        motion /= s        

	# DEBUG
	motion.z = 0
	# /DEBUG
        
        return motion
    
    def get_position(self):
        return self.coordinates[-1]
    
    def encode(self):
        pos = self.get_position()
        mov = self.get_motion()
        return [pos.x, pos.y, pos.z,
                mov.x, mov.y, mov.z]
    
    def is_suitable(self):      
        return len(self.coordinates) >= 10
    
    
class CompositeData(object):
    def __init__(self, image, depth, timestamp):
        self.image = image
        self.depth = depth
        self.timestamp = timestamp
