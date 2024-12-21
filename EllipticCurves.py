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
        return(abs(self.y2Value(x)-y**2) <= 0.01)
    

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

    def pointMultiplication(self, P, s):
        if (not isinstance(s,int)):
            raise Exception("Can only multiply by integers")
        match P:
            case (x,y):
                if (curve.isCurveElem(x,y)):
                    s = bin(s)
                    s = str(s)
                    s = s[2:]
                    res = "Infinity"
                    temp = (x,y)
                    for bit in s[::-1]:
                        if (bit == '1'):
                            res = curve.pointAddition(res,temp)
                        temp = curve.pointAddition(temp,temp)
                        
                    return res
                else:
                    raise Exception("Invalid point to multiply (Not on the curve)")
            case "Infinity":
                return "Infinity"

            case _:
                raise Exception("Invalid point to multiply")

    
    
curve = EllipticCurve(0,4)
#print(curve.y2Value(2))
#print(curve) 
#print(curve.pointNegation((0,-2)))
print(curve.isCurveElem(3,curve.yvalue(3)))

#print(curve.pointAddition((3,curve.yvalue(3)),(3,curve.yvalue(3))))
print(curve.pointMultiplication((3,curve.yvalue(3)),4))