# -*- coding: utf-8 -*-
"""Vector Module""" 
import math
import numpy as np
from typing import Self
from trimesh import transformations
from .util import unify_types
from .constant import get_eps,get_sig_figures

class Vector(object):
    """Vector Class"""
    @classmethod
    def zero(cls):
        """Returns the zero vector (0 | 0 | 0)"""
        return cls(0, 0, 0)
    
    @classmethod
    def x_unit_vector(cls):
        """Returns the unit vector (1 | 0 | 0)"""
        return cls(1, 0, 0)
    
    @classmethod
    def y_unit_vector(cls):
        """Returns the unit vector (0 | 1 | 0)"""
        return cls(0, 1, 0)

    @classmethod
    def z_unit_vector(cls):
        """Returns the unit vector (0 | 0 | 1)"""
        return cls(0, 0, 1)

    def __init__(self, *args):
        """Vector(x, y, z)
        Vector([x, y, z]):
        A vector with coordinates (x | y | z)

        Vector(P1, P2):
        A vector going from point P1 to P2.
        """
        if len(args) == 3:
            # Initialising with 3 coordinates
            self._v = list(args)
        elif len(args) == 2:
            # Initialising from point A to point B
            A, B = args
            self._v = [
                B.x - A.x,
                B.y - A.y,
                B.z - A.z,
            ]
        elif len(args) == 1:
            # Initialising with an array of coordinates
            self._v = list(args[0])
        else:
            raise TypeError("Vector() takes one, two or three parameters, "
                            "not {}".format(len(args)))
        self._v = unify_types(self._v)
        #self.anchor = Point(anchor) if anchor is not None else Point.origin()

    def __hash__(self):
        """return the hash of a vector"""
        return hash(("Vector",
        round(self._v[0],get_sig_figures()),
        round(self._v[1],get_sig_figures()),
        round(self._v[2],get_sig_figures()),
        round(self._v[0],get_sig_figures()) * round(self._v[1],get_sig_figures()),
        round(self._v[1],get_sig_figures()) * round(self._v[2],get_sig_figures()),
        round(self._v[2],get_sig_figures()) * round(self._v[0],get_sig_figures()),
        ))

    def __repr__(self):
        return "Vector({}, {}, {})".format(*self._v)
    
    def __eq__(self, other):
        return np.allclose(self._v, other._v)

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Can only add a Vector to another Vector")
        return Vector(x+y for x, y in zip(self, other))
    
    def __sub__(self, other):
        if not isinstance(other, Vector): # TODO: should support other iterables of length 3
            raise TypeError("Can only subtract a Vector from another Vector")
        return Vector([x-y for x, y in zip(self, other)])

    def __mul__(self, other):
        if isinstance(other, Vector):
            return sum(x*y for x, y in zip(self, other))
        return Vector([x*other for x in self._v])

    def __rmul__(self, other):
        return self * other
    
    def __truediv__(self, other):
        return Vector([x/other for x in self._v])
    
    def __neg__(self):
        return self * -1

    def __getitem__(self, item):
        return self._v[item]

    def __setitem__(self, item, value):
        self._v[item] = value
    
    def __array__(self,dtype=None):
        return np.array(self._v,dtype=dtype)
    
    def __ndarray__(self,dtype=None,n=2):
        return self.__array__(dtype=dtype)[:,*[np.newaxis]*(n-1)].T

    def T(self):
        return self.__ndarray__().T
    
    def cross(self, other):
        r"""Calculates the cross product of two vectors, defined as
        _   _   / x2y3 - x3y2 \
        x × y = | x3y1 - x1y3 |
                \ x1y2 - x2y1 /

        The cross product is orthogonal to both vectors and its length
        is the area of the parallelogram given by x and y.
        """
        a, b = self._v, other._v
        return Vector(
                a[1] * b[2] - a[2] * b[1],
                a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0]
                )

    def length(self):
        """Returns |v|, the length of the vector."""
        return (self * self) ** 0.5
    __abs__ = length

    def parallel(self, other):
        """Returns true if both vectors are parallel."""
        from .solver import solve
        if self == Vector.zero() or other == Vector.zero():
            return True
        if self == other:
            return True

        return abs(abs(self * other) - self.length() * other.length()) < get_eps() * self.length()

    def orthogonal(self, other):
        """Returns true if the two vectors are orthogonal"""
        return abs(self * other) < get_eps()

    def angle(self, other):
        """Returns the angle (in radians) enclosed by both vectors."""
        return math.acos((self * other) / (self.length() * other.length()))

    def normalized(self):
        """Return the normalized version of the vector, that is a vector
        pointing in the same direction but with length 1.
        """
        # Division is not defined, so we have to multiply by 1/|v|
        return self / self.length()
    unit = normalized

    def rotate(self, angle, axis: Self):
        """Rotate the vector around the given axis by the given angle (in radians)
        The rotation is done around the origin, as there is no anchor to keep track of,
        so the vector remains the same even if the point was not the origin. See AnchoredVector class
        """
        if not isinstance(axis,(Vector,list,tuple,np.ndarray)):
            raise NotImplementedError("The first parameter for rotate function must be Vector-like")

        R = transformations.rotation_matrix(angle,axis.normalized())
        self._v = np.dot(R,np.array([self._v+[1]]).T).T[:,:3].squeeze().tolist() # could use np.dot here but not sure if I need to use all 4 cols of R
        return

x_unit_vector = Vector.x_unit_vector
y_unit_vector = Vector.y_unit_vector
z_unit_vector = Vector.z_unit_vector
__all__ = ("Vector","x_unit_vector","y_unit_vector","z_unit_vector")
