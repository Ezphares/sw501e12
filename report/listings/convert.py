''' Python Code '''

# Class containing raw Kinect input
class KinectData(object): 
	
	def depth_mm(self):
		return 0.1236 * math.tan(self.depth / 2843.5 + 1.1863) * 1000.0
	def h_deg(self):
		return self.h / KinectData.hres * KinectData.hfield
	def v_deg(self):
		return self.v / KinectData.vres * KinectData.vfield

# Class containing a vector with 3 elements
class Vector3(object):
	# Has properties x, y, z
	
	# Transform a point from KinectData to Vector3
	def _kinect(self, kinect_data):
	
		# Get distance to point, from (0, 0, 0)
		depth = kinect_data.depth_mm()
		
		# Use the law of sines to find x and y
		self.x = int(math.sin(math.radians(kinect_data.h_deg())) * (depth / math.sin(math.radians(90.0))))
		self.y = int(-(math.sin(math.radians(kinect_data.v_deg())) * (depth / math.sin(math.radians(90.0)))))

		# Use Pythagoras' theorem to find z
		dist2 = math.sqrt(self.x * self.x + self.y * self.y)
		self.z = int(math.sqrt(depth * depth - dist2 * dist2))