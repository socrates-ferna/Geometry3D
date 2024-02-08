import copy
from math import sqrt
import unittest
import numpy as np
from trimesh import transformations
from itertools import combinations
from Geometry3D import Point, Vector, AnchoredVector


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
            if not isinstance(a, Point):
                a = Point(a)
            if not isinstance(b, Point):
                b = Point(b)
            self.assertEqual(
                a,
                b,
            )
        # Not testing coord by coord because it's done in the equality test
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
    def test_move(self):
        p = Point(1, 2, 3)
        v = np.array([1, 2, 3])
        p.move(v)
        self.assertEqual(
            p,
            Point(2, 4, 6),
        )
        p.move(-1*v)
        self.assertEqual(
            p,
            Point(1, 2, 3),
        )
    def test_rotate(self):
        p = Point(1, 1, 1)
        orig = Point.origin()
        axis = Vector(1, 0, 0)
        refp = np.array([[1,1,1]])
        angle = np.pi/2
        rot_mat = transformations.rotation_matrix(angle, axis,point=orig)
        rotated = transformations.transform_points(p.__ndarray__(n=2), rot_mat)
        p.rotate(angle, axis, point=orig)
        ref_rotated = transformations.transform_points(refp, rot_mat)
        self.assertEqual(
            Point(np.squeeze(rotated)),
            Point(np.squeeze(ref_rotated)),
        )
        self.assertEqual(
            p,
            Point(np.squeeze(ref_rotated))
        )
        neworig = Point(1, 2, 3)
        p = Point(1, 1, 1)
        refp = np.array([[1,1,1]])
        rot_mat = transformations.rotation_matrix(angle, axis,point=neworig)
        rotated = transformations.transform_points(p.__ndarray__(n=2), rot_mat)
        p.rotate(angle,axis,point=neworig)
        ref_rotated = transformations.transform_points(refp, rot_mat)
        self.assertEqual(
            Point(np.squeeze(rotated)),
            Point(np.squeeze(ref_rotated)),
        )
        self.assertEqual(
            p,
            Point(np.squeeze(ref_rotated))
        )
    def test_distance(self):
        p1 = Point(1, 1, 1)
        p2 = Point(1, 2, 3)
        self.assertAlmostEqual(
            p1.distance(p2),
            sqrt(1 + 4),
        )
    def test_array(self):
        self.assertTrue(
            np.allclose(
                Point(1, 2, 3).__array__(),
                np.array([1, 2, 3]),
            )
        )
    def test_ndarray(self):
        p = Point(1, 2, 3)
        _p = np.array([[[1,2,3]]])
        self.assertTupleEqual(
            p.__ndarray__(n=3).shape,
            _p.shape,
        )
        self.assertTrue(
            np.allclose(
                p.__ndarray__(n=2),
                np.array([[1, 2, 3]]),
            )
        )
    def test_T(self):
        p = Point(1, 2, 3)
        self.assertTrue(
            np.allclose(
                p.T(),
                np.array([[1, 2, 3]]).T,
            )
        )
        self.assertTupleEqual(
            p.T().shape,
            (3, 1),
        )
    def test_coords(self):

        p = Point(1, 2, 3)
        self.assertTrue(
            np.allclose(
                p.coords,
                np.array([1, 2, 3]),
            )
        )
        self.assertAlmostEqual(p.x, 1)
        self.assertAlmostEqual(p.y, 2)
        self.assertAlmostEqual(p.z, 3)
        p.x = 4
        p.y = 5
        p.z = 6
        self.assertAlmostEqual(p.x, 4)
        self.assertAlmostEqual(p.y, 5)
        self.assertAlmostEqual(p.z, 6)
        self.assertTrue(
            np.allclose(
                p.coords,
                np.array([4, 5, 6]),
            )
        )
    def test_pv(self):
        p = Point(1, 2, 3)
        self.assertEqual(
            p.pv(),
            Vector(1, 2, 3),
        )
        self.assertEqual(
            p.pv(),
            Vector(p.coords)
        )


class AnchoredVectorTest(unittest.TestCase):
    def test_init(self):
        p = Point(1, 2, 3)
        v = AnchoredVector(1,1,1,anchor=p)
        self.assertEqual(
            v.anchor,
            p,
        )

if __name__ == "__main__":
    unittest.main()

