'''

'''

class DetectedObject(object):
    offset_x = -320
    offset_y = -240
    offset_z = 0
    
    def __init__(self, start):
        self.coordinates = []
        self.distances = []
        self.age = 0
        self.start = start
        self.end = 0
        
    def get_motion(self):
        if len(self.coordinates) != len(self.distances):
            raise 'Error: coordinate and distance mismatch.'
        
        motion_set = [(self.coordinates[i][0] - self.coordinates[i-1][0],
                       self.coordinates[i][1] - self.coordinates[i-1][1],
                       self.distances[i] - self.distances[i-1])
                      for i in range(1, len(self.coordinates))]
        
        x, y, z = 0, 0, 0
        for i in range(0, len(motion_set)):
            x += motion_set[i][0]
            y += motion_set[i][1]
            z += motion_set[i][2]
        
        x /= len(motion_set)
        y /= len(motion_set)
        z /= len(motion_set)
        
        dt = self.end - self.start
        s = dt.total_seconds()
        
        x /= s
        y /= s
        z /= s        
        
        return (x,y,z)
    
    def get_position(self):
        return (self.coordinates[-1][0], self.coordinates[-1][1], self.distances[-1])
    
    def encode(self):
        pos = self.get_position()
        mov = self.get_motion()
        return [int(pos[0] + DetectedObject.offset_x),
                int(pos[1] + DetectedObject.offset_y),
                int(pos[2] + DetectedObject.offset_z),
                int(mov[0]), int(mov[1]), int(mov[2])]
    
    def is_suitable(self):
        if len(self.coordinates) != len(self.distances):
            raise 'Error: coordinate and distance mismatch.'
        
        return len(self.coordinates) >= 3
    
    
class CompositeData(object):
    def __init__(self, image, depth, timestamp):
        self.image = image
        self.depth = depth
        self.timestamp = timestamp
