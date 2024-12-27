import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt 
from dataclasses import dataclass
import math
import numbers


class EllipticCurve:
    """
    A class to represent an elliptic curve over the reals.

    ...

    Attributes
    ----------
    a : numbers.Real
        coefficient of the x term of the curve in Weierstrass form
    b : numbers.Real
        coefficient of the constant term of the curve in Weierstrass form

    Methods
    -------
    y2Value(self, x):
        Return the value of y^2 under the curve given the x coordinate

    yvalue(self, x):
        Return the positive y value under the curve given the x coordinate

    isElem(self, x, y):
        Determine if (x,y) is an element of the curve.
    
    pointNegation(self, x, y):
        Return the negation of the point: (x,y) -> (x,-y).    

    pointAddition(self, xp, yp, xq, yq):
        Return the addition of two points: (xp,yp) and (xq,yq).

    pointMultiplication(self, x, y, s):
        Return the multiplication of point (x,y) by a scalar s.
    """    
    def __init__(self, a:numbers.Real, b:numbers.Real):
        """
        Inits an elliptic curve, y^2 = x^3 + ax + b with corresponding a and parameters.
        """
        self.a = a
        self.b = b

    def __str__(self):
        return "y^2 = x^3 + "+str(self.a)+"x + "+str(self.b)
    
    def y2Value(self, x:numbers.Real) -> numbers.Real:
        """
        Return the value of y^2 given the x coordinate

            Parameters:
                    x : The x coordinate
        """
        return (pow(x,3)+ self.a*x + self.b)
    
    def yvalue(self,x:numbers.Real) -> numbers.Real:
        """
        Return the positive value of y given the x coordinate

            Parameters:
                    x : The x coordinate
        """
        return (math.sqrt(self.y2Value(x)))
    
    def isElem(self, x:numbers.Real | None, y:numbers.Real | None) -> bool:
        """
        Return whether a point (x,y) is an element of the curve.\n
        This includes the point at infinity, represented by the pair (None,None)

            Parameters:
                    x : The x coordinate
                    y : The y coordinate
        """
        if x==None and y==None:
            return True
        elif isinstance(x, numbers.Number) and isinstance(y, numbers.Number):
            return(abs(self.y2Value(x)-y**2) <= 0.0000001)
        else:
            return False
    
    def _errorCorrect(self, x:numbers.Real | None, y:numbers.Real | None) -> tuple[numbers.Real,numbers.Real] | tuple[None,None]:
        if x==None and y==None:
            return None,None
        assert isinstance(x, numbers.Real) and isinstance(y, numbers.Real),"Not a valid point"
        if (y<0):
            return x,-self.yvalue(x)
        else:
            return x,self.yvalue(x)

    def pointNegation(self, x:numbers.Real | None, y:numbers.Real | None) -> tuple[numbers.Real,numbers.Real] | tuple[None,None]:
        """
        Return the negation of a points on the curve.\n
        (x,y) -> (x,-y)

            Parameters:
                    x : The x coordinate
                    y : The y coordinate

        """
        assert self.isElem(x,y),"Not a point on the curve"

        if x==None and y==None:
            return None,None
        else:
            return x,-y

    def pointAddition(self, xp:numbers.Real | None, yp:numbers.Real | None, xq:numbers.Real | None, yq:numbers.Real | None) -> tuple[numbers.Real,numbers.Real] | tuple[None,None]:
        """
        Return the addition of 2 points on the curve

            Parameters:
                    xp : The x coordinate of p
                    yp : The y coordinate of p
                    xq : The x coordinate of q
                    yq : The y coordinate of q

            Detail:
                    The point at infinity is the additive identity element of the curve.\n
                    (x,y) + (None,None) = (x,y).\n
                    Adding a point to its negation returns the point at infinity.\n
                    On an elliptic curve over reals this will be the point with equal x coordinate but y' = -y.\n
                    (x,y) + (x,-y) = (x,y) + -(x,y) = (None,None).\n
                    Adding a point to itself follows the point doubling formula.\n
                    Adding 2 different points follows the point addition formula.\n
                    https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
        """
        assert self.isElem(xp,yp), "p not on the curve"
        assert self.isElem(xq,yq), "q not on the curve"

        if (xp == yp == None):
            return xq,yq
        if (xq == yq == None):
            return xp,yp
        if (xq==xp and yq==-yp):
            return None,None
        elif (xq==xp and yq==yp):
            slope = (3*(xp**2) + self.a)/(2*yp)
            xr = slope**2 - xp - xq
            yr = slope*(xp-xr) - yp
            return self._errorCorrect(xr,yr)
        else:
            slope = (yq-yp)/(xq-xp)
            xr = slope**2 - xp - xq
            yr = slope*(xp-xr) - yp
            return self._errorCorrect(xr,yr)

    def pointMultiplication(self, x:int | None, y:int | None, s:int) -> tuple[int,int] | tuple[None,None]:
        """
        Return the multiplication of a point on the curve by a non-negative integer scalar.

            Parameters:
                    x : The x coordinate
                    y : The y coordinate
                    s : The scalar
            
            Detail:
                    Multiplying any point 0 returns the point at infinity.\n
                    Multiplying the point at infinity by any scalar returns the point at infinity.\n
                    This implementation uses the double-and-add algorithm.\n
                    https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
        """
        assert isinstance(s,int) and s>=0,"can only multiply by non negative integers"
        assert self.isElem(x,y),"must be a point on the curve"
        if (s==0 or (x==None and y==None)):
            return None,None
        else:
            s = bin(s)
            s = str(s)
            s = s[2:]
            resx,resy = None,None
            tempx,tempy = x,y
            for bit in s[::-1]:
                if (bit == '1'):
                    resx,resy = self.pointAddition(resx,resy,tempx,tempy)
                tempx,tempy = self.pointAddition(tempx,tempy,tempx,tempy)
                            
            return self._errorCorrect(resx,resy)

    
    
curve = EllipticCurve(0,4)
#print(curve.y2Value(2))
#print(curve) 
#print(curve.pointNegation((0,-2)))
print(curve.isElem(3,curve.yvalue(3)))

#print(curve.pointAddition((3,curve.yvalue(3)),(3,curve.yvalue(3))))
print(curve.pointMultiplication(3,curve.yvalue(3),7))