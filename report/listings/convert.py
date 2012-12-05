class KinectData(object): 
	#...

	def depth_mm(self):
		return 0.1236 * math.tan(self.depth / 2843.5 + 1.1863) * 1000.0

	def h_deg(self):
		return self.h / KinectData.hres * KinectData.hfield

	def v_deg(self):
		return self.v / KinectData.vres * KinectData.vfield

class Vector3(object):
	#...

	def _kinect(self, kinect_data):
		if type(kinect_data) != KinectData:
			raise TypeError('Expected a KinectData instance')

		depth = kinect_data.depth_mm()

		self.x = int(math.sin(math.radians(kinect_data.h_deg())) * (depth / math.sin(math.radians(90.0))))
		self.y = int(-(math.sin(math.radians(kinect_data.v_deg())) * (depth / math.sin(math.radians(90.0)))))

		dist2 = math.sqrt(self.x * self.x + self.y * self.y)

		self.z = int(math.sqrt(depth * depth - dist2 * dist2))

