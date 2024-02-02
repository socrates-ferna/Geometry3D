import unittest
import numpy as np
from itertools import combinations
from Geometry3D import Point
class PointTest(unittest.TestCase):
    def test_origin(self):
        self.assertEqual(
            Point.origin(),
            Point(0, 0, 0),
        )
    def test_equality(self):
        self.assertEqual(
            Point(1, 2, 3),
            Point(1, 2, 3),
        )
        self.assertNotEqual(
            Point(1, 2, 3),
            Point(1, 2, 4),
        )
    def test_init(self):
        refp = Point(1, 2, 3)
        lst = [1, 2, 3]
        tup = (1, 2, 3)
        arr = np.array([1, 2, 3])
        otherp = Point(1, 2, 3)
        all_combs = combinations([refp, lst, tup, arr, otherp], 2)
        for a, b in all_combs:
            self.assertEqual(
                a,
                b,
            )
        # missing check on coords attribute
    def test_repr(self):
        self.assertEqual(
            repr(Point(1, 2, 3)),
            "Point(1, 2, 3)",
        )
    def test_hash(self):
        self.assertEqual(
            hash(Point(1, 2, 3)),
            hash(Point(1, 2, 3)),
        )
        self.assertNotEqual(
            hash(Point(1, 2, 3)),
            hash(Point(1, 2, 4)),
        )

