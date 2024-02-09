import unittest
import math
from Geometry3D import AnchoredVector, Vector, Point

class AnchoredVectorTest(unittest.TestCase):
    def test_eq(self):
        v1 = AnchoredVector(1, 2, 3)
        v2 = AnchoredVector(1, 2, 3)
        self.assertEqual(v1, v2)
        v2 = AnchoredVector(1, 2, 3, anchor=Point(1, 1, 1))
        self.assertNotEqual(v1, v2)
        v1 = AnchoredVector(1, 2, 3, anchor=Point(1, 1, 1))
        self.assertEqual(v1, v2)
    
    def test_move(self):
        v = AnchoredVector(1, 2, 3)
        v.move(Vector(4, 5, 6))
        self.assertEqual(v.anchor, Point(4, 5, 6))
        self.assertEqual(v.end_point, Point(5, 7, 9))
    
    def test_rotate(self):

        v = AnchoredVector(1, 2, 3)
        v.rotate(math.pi / 2, Vector(1, 0, 0))
        self.assertEqual(v, AnchoredVector(1, -3, 2))
        self.assertEqual(v.anchor, Point(0, 0, 0))
        self.assertEqual(v.end_point, Point(1, -3, 2))
        
        v = AnchoredVector(1, 2, 3, anchor=Point(1, 1, 1))
        v.rotate(math.pi / 2, Vector(1, 0, 0))
        self.assertEqual(v, AnchoredVector(1,-3,2, anchor=Point(1, 1, 1)))
        self.assertEqual(v.anchor, Point(1, 1, 1))
        self.assertEqual(v.end_point, Point(2, -2, 3))

        v = AnchoredVector(1, 2, 3, anchor=Point(1, 1, 1))
        v.rotate(math.pi / 2, Vector(1, 0, 0), point=Point(0, 0, 0))
        p = Point(1, 1, 1)
        p.rotate(math.pi / 2, Vector(1, 0, 0))
        self.assertEqual(
            v,
            AnchoredVector(
                1,-3,2,
                anchor=p
                )
            )

if __name__ == '__main__':
    unittest.main()