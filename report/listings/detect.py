''' Python Code '''
def detect_objects(self):
	self.lock_array.acquire()
	temp_frames = [o for o in self.frames]
	self.frames = []
	self.lock_array.release()

	for frame in temp_frames:
		try:
			gray = cv2.cvtColor(frame.image, cv.CV_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, Analyzer.blur_strength, 0)
			depth = frame.depth.flatten()
		except:
			continue
		
		for o in self.objects:
			if o.age > Analyzer.object_max_age:
				self.objects.remove(o)
			o.age += 1
		
		circles = cv2.HoughCircles(gray, cv.CV_HOUGH_GRADIENT, 2, 100)
		if circles == None:
			circles = [[]]
		
		for circle in circles[0]:
			x, y = circle[0], circle[1]
			z = depth[y * 640 + x]
			p = Vector3f the(from_kinect = KinectData(depth = z, h = x + DetectedObject.offset_x, v = y + DetectedObject.offset_y))
			cv2.circle(frame.image, (int(x), int(y)), int(circle[2]), cv.CV_RGB(255, 0, 0), 2, 8, 0 )
			
			assigned = (None, Analyzer.tracking_max_distance)
			for o in self.objects:
				if o.age == 0:
					continue
				pos = o.get_position()
				dist = len(pos - p)
				if dist < assigned[1]:
					assigned = (o,dist)
	
			o = None
			if assigned[0] == None:
				o = DetectedObject(datetime.now())
				self.objects.append(o)
			else:
				o = assigned[0]    
			
			o.coordinates.append(p)
			o.end = datetime.now()
			o.age = 0
	
		cv2.imshow(self.window, frame.image)
