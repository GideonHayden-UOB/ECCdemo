import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt 
from dataclasses import dataclass
import math
import numbers


class EllipticCurve:
    def __init__(self, a:numbers.Real, b:numbers.Real):
        self.a = a
        self.b = b

    def __str__(self):
        return "y^2 = x^3 + "+str(self.a)+"x + "+str(self.b)
    
    def y2Value(self, x:numbers.Real) -> numbers.Real:
        return (pow(x,3)+ self.a*x + self.b)
    
    def yvalue(self,x:numbers.Real) -> numbers.Real:
        return (math.sqrt(self.y2Value(x)))
    
    def isElem(self, x:numbers.Real | None, y:numbers.Real | None) -> bool:
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
        assert self.isElem(x,y),"Not a point on the curve"

        if x==None and y==None:
            return None,None
        else:
            return x,-y

    def pointAddition(self, xp:numbers.Real | None, yp:numbers.Real | None, xq:numbers.Real | None, yq:numbers.Real | None) -> tuple[numbers.Real,numbers.Real] | tuple[None,None]:
 
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