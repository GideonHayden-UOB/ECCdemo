import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt 
from dataclasses import dataclass
import math


class EllipticCurve:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return "y^2 = x^3 + "+str(self.a)+"x + "+str(self.b)
    
    def y2Value(self, x):
        return (pow(x,3)+ self.a*x + self.b)
    
    def yvalue(self,x):
        return (math.sqrt(self.y2Value(x)))
    
    def isCurveElem(self,x,y):
        return(self.y2Value(x)==y**2)
    

    def pointNegation(self, point):
        match point:
            case (x,y):
                if (self.isCurveElem(x,y)):
                    return (x,-y)
                else:
                    raise Exception ("Not a valid point on the curve")
            case "Infinity" | "infinity" | "inf" | "Inf" | "I" | "i":
                return "Infinity"
            case _:
                raise Exception ("Not a valid point on the curve")
            
    def pointAddition(self, P, Q):
        expr = (P,Q)
        match expr:
            case ((xp,yp),(xq,yq)):
                    if (xp==xq and yp == -yq):
                        return "Infinity"
                    elif(xp==xq and yp==yq):
                        slope = (3*(xp**2) + self.a)/(2*yp)
                        xr = slope**2 - xp - xq
                        yr = slope*(xp-xr) - yp
                        return (xr,yr)

                    else:
                        slope = (yq-yp)/(xq-xp)
                        xr = slope**2 - xp - xq
                        yr = slope*(xp-xr) - yp
                        return (xr,yr)

            case ("Infinity", (x,y)):
                if (self.isCurveElem(x,y)):
                    return Q
                else:
                    raise Exception ("Not a valid point on the curve")
            case ((x,y),"Infinity"):
                if (self.isCurveElem(x,y)):
                    return P
                else:
                    raise Exception ("Not a valid point on the curve")
            case _:
                raise Exception ("Not valid points on the curve")

            
    
    
curve = EllipticCurve(0,4)
print(curve.y2Value(2))
print(curve) 
print(curve.pointNegation((0,-2)))

print(curve.pointAddition((3,curve.yvalue(3)),(1,curve.yvalue(1))))
