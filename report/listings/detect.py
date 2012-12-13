''' Python Code '''

# Class for analyzing images
class Analyzer(object):
	
	# Detect circular objects in images
    def detect_objects(self):
		
		# 'temp_frames' contain composite data stored
		#   from freenect callbacks
        for frame in temp_frames:
			# Desaturate the image ...
			gray = cv2.cvtColor(frame.image, cv.CV_BGR2GRAY)
			# ... and blur it
			gray = cv2.GaussianBlur(gray, Analyzer.blur_strength, 0)
			
			# The depth array is flattened, making it a one-dimensional
			#   array.
			depth = frame.depth.flatten()
            
			# Find circles in the image data
            circles = cv2.HoughCircles(gray, cv.CV_HOUGH_GRADIENT, 2, 100)
            
			# 'circles[0]' and not 'circles' is the list of circles found,
			#   as OpenCV stores various data about errors in circles[1]
			for circle in circles[0]:
				# Get the x, y and z values from their respective variables
				#   These are actually the h, v, and depths variables for a
				#   KinectData position, and not the vectorized coordinates
                x, y = circle[0], circle[1]
                z = depth[y * KinectData.hres + x]
				
				# Convert the position to a vector
                p = Vector3(from_kinect = KinectData(depth = z, h = x + DetectedObject.offset_x, v = y + DetectedObject.offset_y))
				
				# See if the object can be assigned to an existing object
                assigned = (None, Analyzer.tracking_max_distance)
				# 'objects' contain objects saved for previous frames
                for o in self.objects:
                    pos = o.get_position()
					# Find the distance using vector arithmetic
                    dist = len(pos - p)
					# If it is the closest object, assume they are the same
                    if dist < assigned[1]:
                        assigned = (o,dist)
			#...