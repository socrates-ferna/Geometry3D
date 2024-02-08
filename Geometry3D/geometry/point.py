# -*- coding: utf-8 -*-
"""Point Module"""
from typing import Self
import numpy as np
import trimesh.transformations as transformations
from ..utils.util import unify_types
import math
from ..utils.logger import get_main_logger
from ..utils.constant import get_sig_figures,get_eps
from ..utils.vector import Vector

class Point(object):
    """
    - Point(a, b, c)
    
    - Point([a, b, c]):
    
    The point with coordinates (a | b | c)

    - Point(Vector):
    
    The point that you get when you move the origin by the given
    vector. If the vector has coordinates (a | b | c), the point
    will have the coordinates (a | b | c) (as easy as pi).
    """
    class_level = 0 # the class level of Point
    @classmethod
    def origin(cls):
        """Returns the Point (0 | 0 | 0)"""
        return cls(0, 0, 0)
    
    def __init__(self, *args):
        """
        Initializes a Point object.

        Args:
            *args: Variable number of arguments. 
                - If a single argument is provided, it is treated as a sequence of coordinates.
                - If three arguments are provided, they are treated as individual x, y, and z coordinates.

        Raises:
            TypeError: If the number of arguments is not 1 or 3.

        Returns:
            None
        """
        if len(args) == 1:
            # Initialisation by Vector is also handled by this
            coords = args[0]
        elif len(args) == 3:
            coords = args
        else:
            raise TypeError("Point() takes one or three arguments, not {}"
                    .format(len(args)))
        self.coords = [None, None, None]
        self.x, self.y, self.z = unify_types(coords)
        #self.coords = [self.x, self.y, self.z]
        get_main_logger().debug('Create %s' %(self.__repr__(),))

    def __repr__(self):
        return "Point({}, {}, {})".format(
                self.x,
                self.y,
                self.z,
                )

    def __hash__(self):
        """return the hash of a point"""
        return hash(("Point",
        round(self.x,get_sig_figures()),
        round(self.y,get_sig_figures()),
        round(self.z,get_sig_figures()),
        round(self.x,get_sig_figures()) * round(self.y,get_sig_figures()),
        round(self.x,get_sig_figures()) * round(self.z,get_sig_figures()),
        round(self.y,get_sig_figures()) * round(self.z,get_sig_figures()),
        ))

    def __eq__(self, other):
        """Checks if two Points are equal. Always use == and not 'is'!"""
        if isinstance(other,Point):
            return (abs(self.x - other.x) < get_eps() and
                    abs(self.y - other.y) < get_eps() and
                    abs(self.z - other.z) < get_eps())
        else:
            return False

    def __sub__(self, other):
        return [x-y for x, y in zip(self, other)]
    
    def __getitem__(self, item):
        """return the i element of a Point"""
        return self.coords[item]

    def __setitem__(self, item, value):
        """set the i element of a Point"""
        setattr(self, "xyz"[item], value)
        self.coords[item] = value
    
    def __array__(self,dtype=None):
        """return the array of a Point"""
        return np.array([self.x, self.y, self.z],dtype=dtype)

    def __ndarray__(self,dtype=None,n=2):
        """return the n-dimensional array of a Point"""
        return self.__array__(dtype=dtype)[:,*[np.newaxis]*(n-1)].T

    @property
    def x(self):
        return self.coords[0]
    
    @x.setter
    def x(self, value):
        self.coords[0] = value
    
    @property
    def y(self):
        return self.coords[1]
    
    @y.setter
    def y(self, value):
        self.coords[1] = value
    
    @property
    def z(self):
        return self.coords[2]
    
    @z.setter
    def z(self, value):
        self.coords[2] = value

    def T(self):
        """Column vector form of the point"""
        return np.array([[self.x, self.y, self.z]]).T
    def pv(self):
        """Return the position vector of the point."""
        return Vector(self.x, self.y, self.z)

    def move(self, v):
        """Return the point that you get when you move self by vector v, self is also moved"""
        v = Vector(v) # the original author enforced moving with a vector, this respects the intention
        self[0] += v[0]
        self[1] += v[1]
        self[2] += v[2]
        return Point(self.coords)

    def rotate(self, angle: float, axis: Vector, point: Self = None):
        """
        Rotate around axis by angle (in radians) using
        trimesh transformations module
        """
        if not isinstance(axis,(Vector,list,tuple,np.ndarray)):
            raise NotImplementedError("The first parameter for rotate function must be Vector")

        R = transformations.rotation_matrix(angle,axis.normalized(),point)
        v = np.dot(R,np.array([self.coords]).T).T[:,:3] # could use np.dot here but not sure if I need to use all 4 cols of R
        self.x, self.y, self.z = v[0],v[1],v[2]
        self.coords = [self.x, self.y, self.z] # coords requires update
        return Point(v[0],v[1],v[2]) # this return respects the spirit of the rest of methods, but I think it should return None

    def distance(self,other):
        """Return the distance between self and other"""
        return math.sqrt((self.x -other.x) ** 2 + (self.y -other.y) ** 2 + (self.z -other.z) ** 2)
    def vdistance(self,other):
        """Return the distance between self and other"""
        return AnchoredVector(self,other,anchor=self)


class AnchoredVector(Vector):
    def __init__(self, *args, anchor: Point = None):
        super().__init__(*args)
        self.anchor = anchor if anchor is not None else Point.origin()

origin = Point.origin

__all__ = ("Point","AnchoredVector","origin")
