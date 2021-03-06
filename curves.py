# curves.py
# Contains classes which represent mathematical equations of curves.
import math

from distfuncs import *

# This class defines a "line equation" object, which represents
# the equation: y = mx + b
# Line equations will be used to represent supply and demand curves
class Linear():
    def __init__(self,m,b):
        # Slope
        self.m = m
        # Y intercept
        self.b = b
    
    # Evaluate the function at a point
    def evaluate(self,x):
        return self.m * x + self.b

    # Returns the angle of the line in radians. Range from -pi to pi radians
    # 0 degrees is east
    def angle(self):
        return math.atan2(self.m,1)

    def print(self):
        print('y = %0.12fx' % self.m + ' + %0.12f' % self.b)

# This function returns the intersection point of two lines
def lines_intersect(line1,line2):
    # How it works:
    # y = m1 x + b1
    # y = m2 x + b2
    # m1 x + b1 = m2 x + b2
    # (m1 - m2) x = b2 - b1
    # x = (b2 - b1) / (m1 - m2)
    
    x = (line2.b - line1.b) / (line1.m - line2.m)
    y = line1.m * x + line1.b

    return (x,y)

def line_intersect_vline(line1,vline_x):
    # Just evaluate at a point
    return (vline_x,line1.evaluate(vline_x))

# This class represents a quadratic equaion in the form:
# y = ax^2 + bx + c
class Quadratic():
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c

        # Avoid divide by 0
        if self.a == 0:
            self.a = 0.00000000000001

    # Evaluates the equation at a point
    def evaluate(self,x):
        return (self.a * x **2 + self.b * 2 + self.c)

    # This function returns the coordinates of the vertex of the function
    def vertex(self):
        """
        How it works:
        
        y = ax^2 + bx + c
        dy/dx = 2ax + b
        0 = 2ax + b
        -b / (2a) = x

        """

        x = -self.b / (2 * self.a)
        y = self.a * x**2 + self.b * x + self.c

        return (x,y)

    # This function returns the roots of the quadratic
    def roots(self):
        """
        How it works:

        x = (-b +/- sqrt(b^2 - 4ac)) / (2a)

        Tests:
        >>> b = Quadratic(1,5,6)
        >>> b.roots() == {-3,-2}
        True
        """

        # Test for complex roots. We don't want to deal with these
        if (self.b**2 - 4 * self.a * self.c) < 0:
            return []

        solutions = set()
        solutions.add((-self.b + math.sqrt(self.b**2 - 4 * self.a * self.c)) / (self.a * 2))
        solutions.add((-self.b - math.sqrt(self.b**2 - 4 * self.a * self.c)) / (self.a * 2))

        return solutions

    def print(self):
        tempstr = '%0.3fx^2' % self.a + ' + %0.3fx' % self.b + ' + %0.3f' % self.c
        print(tempstr)

# Returns the point of intersection between a quadratic and a line
def quad_line_intersect(quad,line):
    """
    How it works:

    mx + b1 = ax ^ 2 + bx + c
    0 = ax^2 + (b - m) x + c - B1

    Then define a new quadratic, and find the roots

    TESTS:
    >>> a = Quadratic(1,0,0)
    >>> b = Linear(0,0)
    >>> {(0, 0)} == quad_line_intersect(a,b)
    True
    >>> a = Quadratic(1,0,1)
    >>> None == quad_line_intersect(a,b)
    True
    """

    temp_quad = Quadratic(quad.a,quad.b - line.m,quad.c - line.b)
    roots = temp_quad.roots()

    # If no roots, end early.
    if roots == []:
        return None

    # Just got a list of either 0, 1, or 2  roots
    int_pts = set()
    for root in roots:
        int_pts.add((root,quad.evaluate(root)))

    return int_pts

# Defines a quadratic bezier curve (order 2)
# Parametric curve in form:
# B(t) = (1-t)^2  P0 + 2(1-t)t P1 + t^2 P2, t in [0,1]
# P0...Pn are coordinate points.
# P0 is the origin, P2 is the endpoint. P1 is an intermediate point.

class QuadraticBezier():
    def __init__(self,P0,P1,P2):
        # Points are in tuples (x,y)
        self.P0 = P0
        self.P1 = P1
        self.P2 = P2

    # Evaluate for a point at t
    def evaluate(self,t):
        x = math.pow(1-t,2) * self.P0[0] + 2*(t-1)*t*self.P1[0] + math.pow(t,2) * self.P2[0]
        y = math.pow(1-t,2) * self.P0[1] + 2*(t-1)*t*self.P1[1] + math.pow(t,2) * self.P2[1]

        return (x,y)
    
    # Find t at point. If the point does not lie on teh curve, return an empty set.
    def solve(self,pt):

        (x,y) = pt
        
        quadx = Quadratic(self.P0[0] - 2*self.P1[0] + self.P2[0],
                          -2 * self.P0[0] + 2 * self.P1[0],
                          self.P0[0] - x)

        quady = Quadratic(self.P0[1] - 2*self.P1[1] + self.P2[1],
                          -2 * self.P0[1] + 2 * self.P1[1],
                          self.P0[1] - y)

        rootx = quadx.roots()
        rooty = quady.roots()

        solutions = set()

        for root in rootx:
            if root in rooty and 0 <= root <= 1:
                solutions.add(root)

        return solutions

# Bezier intersecting vertical line
def Bez_intersect_vline(bez,x):
    """
    Tests:

    >>> bez1 = QuadraticBezier((0,1),(2,0),(3,2))
    >>> print(Bez_intersect_vline(bez1,1))
    

    """
    # This is an easy problem. Define a quadratic
    quad = Quadratic(bez.P0[0]-2*bez.P1[0]+bez.P2[0],-2*bez.P0[0]+2*bez.P1[0],bez.P0[0] - x)
    quad.print()
    
    # Find the roots, so basically solve for t
    t = quad.roots()
    print(t)

    # Throw out roots that are out of bounds

    solutions = set()
    for root in t:
        # if root > 0 and root < 1:
        solutions.add(bez.evaluate(root))
    
    # Return solution set of intersection points
    return solutions

# Find the intersection between two bezier curves numerically. TODO: Algebraic method

# THIS FUNCTION DOES NOT WORK YET
def Bez_intersect(bez1,bez2):
    # Iterate through the curve

    ir = 200
    thr = 0.003

    bez1_pts = []
    for t in range(0,ir):
        bez1_pts.append(bez1.evaluate(t/ir))

    bez2_pts = []
    for t in range(0,ir):
        bez2_pts.append(bez2.evaluate(t/ir))

    solutions = []
    val = []
    
    for i in range(0,ir):
        for j in range(0,ir):
            distance =  dist(bez1_pts[i][0],bez1_pts[i][1],bez2_pts[j][0],bez2_pts[j][1])
            # if distance < 0.07: print(distance)
            a = round(distance,3)
            if a < thr and a not in val:
                solutions.append((i/ir,j/ir))
                val.append(a)

    return solutions
            
if __name__ == "__main__":
        import doctest
        doctest.testmod()
