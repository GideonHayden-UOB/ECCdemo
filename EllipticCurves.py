import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt 
from dataclasses import dataclass


class EllipticCurve:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return "y^2 = x^3 + "+str(self.a)+"x + "+str(self.b)
    
    def y2Value(self, x):
        return (pow(x,3)+ self.a*x + self.b)
    
    def yvalue(self,x):
        return (np.sqrt(self.y2Value(x)),-np.sqrt(self.y2Value(x)))
    
    def isCurveElem(self,x,y):
        return(self.y2Value(x)==y**2)
    
    def pointNegation(self, point):
        match point:
            case (x,y):
                if (type(x) is int and type(y) is int and self.isCurveElem(x,y)):
                    return (x,-y)
                else:
                    raise Exception ("Not a valid point on the curve")
            case "Infinity" | "infinity" | "inf" | "Inf" | "I" | "i":
                return "Infinity"
            case _:
                raise Exception ("Not a valid point on the curve")
            
    
    
curve = EllipticCurve(0,4)
print(curve.y2Value(2))
print(curve) 
print(curve.pointNegation((0,-2)))

print(curve.pointNegation("Inf"))

