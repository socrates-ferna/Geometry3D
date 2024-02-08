# -*- coding: utf-8 -*-
import math
import numpy as np
import unittest
from Geometry3D import Vector


class VectorTest(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(
            Vector.zero(),
            Vector(0, 0, 0),
        )

    def test_getitem(self):
        v = Vector(1, 2, 3)
        self.assertEqual(v[0], 1)
        self.assertEqual(v[1], 2)
        self.assertEqual(v[2], 3)

    def test_addition(self):
        self.assertEqual(
            Vector(2, 3, 5) + Vector(7, 11, 13),
            Vector(9, 14, 18),
        )
    
    def test_equality(self):
        self.assertEqual(Vector(1, 2, 3), Vector(1, 2, 3))
        self.assertNotEqual(Vector(1, 2, 3), Vector(1, 2, 4))

    def test_subtraction(self):
        self.assertEqual(
            Vector(9, 14, 18) - Vector(7, 11, 13),
            Vector(2, 3, 5),
        )

    def test_multiply_real_with_vector(self):
        self.assertEqual(
            2 * Vector(2, 3, 5),
            Vector(4, 6, 10),
        )

    def test_multiply_vector_with_vector(self):
        self.assertEqual(
            Vector(2, 3, 5) * Vector(7, 11, 13),
            2 * 7 + 3 * 11 + 5 * 13,
        )
    
    def test_divide(self):
        self.assertEqual(
            Vector(2, 3, 5) / 2,
            Vector(1, 1.5, 2.5),
        )

    def test_neg(self):
        self.assertEqual(
            -Vector(2, 3, 5),
            Vector(-2, -3, -5),
        )

    def test_setitem(self):
        v = Vector(2, 3, 5)
        v[0] = 7
        v[1] = 11
        v[2] = 13
        self.assertEqual(v, Vector(7, 11, 13))

    def test_array(self):
        v = Vector(2., 3., 5.)
        self.assertTrue(np.allclose(v.__array__(dtype=np.float64), np.array([2., 3., 5.])))

    def test_ndarray(self):
        v = Vector(2., 3., 5.)
        self.assertTrue(np.allclose(v.__ndarray__(dtype=np.float64), np.array([2,3,5])))
    
    def test_transpose(self):
        v = Vector(2., 3., 5.)
        self.assertTrue(np.allclose(v.T(), np.array([[2.], [3.], [5.]])))
        self.assertTrue(v.T().shape == (3, 1))
    
    def test_cross_product(self):
        a = Vector(2, 3, 5)
        b = Vector(7, 11, 13)
        self.assertEqual(
            a.cross(b),
            Vector(
                3 * 13 - 5 * 11,
                5 * 7 - 2 * 13,
                2 * 11 - 3 * 7,
            ),
        )

    def test_length(self):
        self.assertEqual(
            abs(Vector(3, 4, 0)),
            5,
        )

    def test_parallel(self):
        self.assertTrue(Vector(2, 3, 5).parallel(Vector(4, 6, 10)))
        self.assertTrue(Vector(1, 0, 0).parallel(Vector(10, 0, 0)))
        self.assertFalse(Vector(2, 3, 5).parallel(Vector(4, 6, 11)))
        self.assertFalse(Vector(1, 0, 0).parallel(Vector(0, 1, 0)))

    def test_orthogonal(self):
        self.assertTrue(Vector(1, 0, 0).orthogonal(Vector(0, 1, 1)))
        self.assertFalse(Vector(1, 0, 0).orthogonal(Vector(1, 0, 0)))

    def test_angle(self):
        self.assertAlmostEqual(
            Vector(1, 0, 0).angle(Vector(1, 0, 1)),
            math.pi / 4,  # 45 deg
        )

    def test_normalization(self):
        self.assertAlmostEqual(abs(Vector(1, 1, 1).normalized()), 1)

    def test_rotate(self):
        self.assertEqual(
            Vector(1, 0, 0).rotate(math.pi / 2, Vector(0, 0, 1)),
            Vector(0, 1, 0),
        )

if __name__ == '__main__':
    unittest.main()