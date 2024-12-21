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
    
    def pointNegation(self, point):
        if isinstance(point, str):
            if point=="inf":
                return "inf"
            else:
                raise Exception("Not a valid point")
        elif isinstance(point, (int,int)):
            return 
    
    
curve = EllipticCurve(-2,4)
print(curve.y2Value(2))
print(curve) 
print(pow(0.5,2))


