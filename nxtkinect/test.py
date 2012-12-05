import unittest
import math
from datetime import datetime
from datetime import timedelta
from nxtkinect import coordinate
from nxtkinect import objects

class TestCoordinate(unittest.TestCase):

    def test_vector_length(self):
        v = coordinate.Vector3(10, 5, 0)
        self.assertEqual(len(v), int(math.sqrt(125)))
        
    def test_vector_arith(self):
        v1 = coordinate.Vector3(10, 5, 0)
        v2 = coordinate.Vector3(0, 10, 5)
        
        sub = v1 - v2
        
        self.assertEqual(sub.x, 10)
        self.assertEqual(sub.y, -5)
        self.assertEqual(sub.z, -5)
        
        add = v1 + v2

        self.assertEqual(add.x, 10)
        self.assertEqual(add.y, 15)
        self.assertEqual(add.z, 5)
        
        div = v1 / 2
        
        self.assertEqual(div.x, 5)
        self.assertEqual(div.y, 2)
        self.assertEqual(div.z, 0)

    def test_kinect(self):
        k = coordinate.KinectData(100, 100, 100)
        self.assertAlmostEqual(k.depth_mm(), 339, 0)
        self.assertAlmostEqual(k.h_deg(), 9, 0)
        self.assertAlmostEqual(k.v_deg(), 7, 0)


class TestObject(unittest.TestCase):
    def test_sutable(self):
        o = objects.DetectedObject(datetime.now())
        o.end = o.start + timedelta(0, 1)
        
        self.assertFalse(o.is_suitable())
        
        o.coordinates = [coordinate.Vector3(i, 0, 0) for i in range(0,10)]
        
        self.assertTrue(o.is_suitable())
        
    def test_motion(self):
        o = objects.DetectedObject(datetime.now())
        o.end = o.start + timedelta(0, 1)
        
        o.coordinates = [coordinate.Vector3(10, 10, 10) for i in range(0, 2)]
        v = o.get_motion()
        self.assertEqual(len(v), 0)       
        
        o.coordinates = [coordinate.Vector3(10 * i, 10, 10) for i in range(0, 11)]
        v = o.get_motion()
        self.assertEqual(len(v), 10)       
        
        
        
        

if __name__ == '__main__':
    unittest.main()
