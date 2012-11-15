'''
    analyzer.py
    
    This file contains the analyzer class which will do most of the math of the detector.
'''
import cv2
import cv2.cv as cv
import freenect
import math
from nxtkinect.objects import CompositeData, DetectedObject
from nxtkinect.usbcom import Usbcom
from datetime import datetime
from multiprocessing import Lock

class Analyzer(object):
    frame_threshold = 10000000 / 3
    blur_strength = (15,15)
    tracking_max_distance = 45
    object_max_age = 0
    
    def __init__(self):
        self.window = str(self)
        self.running  = True
        self.last_frame = ('none', ())
        self.frames = []
        self.frames_captured = 0
        self.objects = []
        self.start = None
        self.usb = Usbcom()
        self.nxtwaiting = True
        self.lock = Lock()
        
        cv2.namedWindow(self.window)
        
    
    def new_image(self, dev, data, timestamp):
        pass
        if cv.WaitKey(10) == 27:
            self.running = False
        self.process_frame('image', data, timestamp)
    
    def new_depth(self, dev, data, timestamp):
        if cv.WaitKey(10) == 27:
            self.running = False
        self.process_frame('depth', data, timestamp)

    def process_frame(self, t, data, timestamp):
        self.lock.acquire()
        if type == self.last_frame[0] or self.last_frame[0] == 'none':
            self.last_frame = (t, (data, timestamp))
            self.lock.release()
            return
        
        if timestamp - self.last_frame[1][1] > Analyzer.frame_threshold:
            self.last_frame = (t, (data, timestamp))
            self.lock.release()
            return
        
        c = None
        if t == 'image':
            c = CompositeData(data, self.last_frame[1][0], timestamp)
        else:
            c = CompositeData(self.last_frame[1][0], data, self.last_frame[1][1])
        
        self.frames.append(c)
        self.frames_captured += 1
        self.last_frame = ('none', ())
        self.lock.release()

    def body(self, *args):
        #self.timer()
        self.detect_objects()
        self.report_object()
              
        if not self.running:
            raise freenect.Kill
    
    def report_object(self):
        for o in self.objects:
            if o.is_suitable():
                if self.nxtwaiting:
		    self.nxtwaiting = False
                    data = o.encode()
                    print data
                    self.usb.send_data(data[0], data[1], data[2], data[3], data[4], data[5])
                
                self.objects.remove(o)
    
    def detect_objects(self):
        for frame in self.frames:
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
                #print x, y, z
                cv2.circle(frame.image, (int(x), int(y)), int(circle[2]), cv.CV_RGB(255, 0, 0), 2, 8, 0 )
                
                assigned = (None, Analyzer.tracking_max_distance)
                for o in self.objects:
                    pos = o.get_position()
                    dist = math.sqrt(math.pow(pos[0] - x, 2) + math.pow(pos[1] - y, 2))
                    if dist < assigned[1]:
                        assigned = (o,dist)
        
                o = None
                if assigned[0] == None:
                    #print "New object"
                    o = DetectedObject(datetime.now())
                    self.objects.append(o)
                else:
                    o = assigned[0]    
                
                o.coordinates.append((x, y))
                o.distances.append(z)
                o.end = datetime.now()
                o.age = 0
        
            cv2.imshow(self.window, frame.image)
            #print len(self.objects)
            
        self.frames = []
    
    def timer(self):
        if len(self.frames) > 0:
            if self.start == None:
                self.start = datetime.now()
                print "Starting timer..."
                
        if self.start != None:
            td = datetime.now() - self.start
            if td.microseconds > 1000:
                print 'FPS:',self.frames_captured / td.total_seconds()
