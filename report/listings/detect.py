class Analyzer(object):
	#...
    def detect_objects(self):
		# ...
        for frame in temp_frames:
			gray = cv2.cvtColor(frame.image, cv.CV_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, Analyzer.blur_strength, 0)
			depth = frame.depth.flatten()
            #...
            circles = cv2.HoughCircles(gray, cv.CV_HOUGH_GRADIENT, 2, 100)
            #...
			for circle in circles[0]:
                x, y = circle[0], circle[1]
                z = depth[y * 640 + x]
                p = Vector3(from_kinect = KinectData(depth = z, h = x + DetectedObject.offset_x, v = y + DetectedObject.offset_y))
                assigned = (None, Analyzer.tracking_max_distance)
                for o in self.objects:
					#...
                    pos = o.get_position()
                    dist = len(pos - p)
                    if dist < assigned[1]:
                        assigned = (o,dist)
			#...