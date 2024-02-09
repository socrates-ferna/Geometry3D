from ..geometry import Point
from .vector import Vector
class AnchoredVector(Vector):
    def __init__(self, *args, anchor: Point = None):
        super().__init__(*args)
        self.anchor = anchor if anchor is not None else Point.origin()
        self.end_point = Point(self.anchor.pv() + self)
    
    def __eq__(self, other):
        sup = super().__eq__(other)
        selfeq = self.anchor == other.anchor
        self_end = self.end_point == other.end_point
        return sup and selfeq and self_end
    
    def move(self,v):
        """
        Moves the anchor by the given vector v
        """
        self.anchor.move(v)
        self.end_point = Point(self.anchor.pv() + self)
    
    def rotate(self,angle,axis: Vector, point: Point = None):
        """
        Rotates the vector around the given axis by the given angle (in radians)
        If point is None, rotates around the anchor, else rotates around the given point
        """
        super().rotate(angle,axis)
        if point is not None:
            self.anchor.rotate(angle,axis, point)
        self.end_point = Point(self.anchor.pv() + self)
        return