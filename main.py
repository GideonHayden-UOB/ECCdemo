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
    
class FiniteFieldEllipticCurve:
    def __init__(self, a, b, p:int):
        self.a = a
        self.b = b
        self.p = p

    def __str__(self):
        return "y^2 = x^3 + "+str(self.a)+"x + "+str(self.b)
    
    def y2Value(self, x):
        return (pow(x,3)+ self.a*x + self.b)
    
    def yvalue(self,x):
        return (np.sqrt(self.y2Value(x)),-np.sqrt(self.y2Value(x)))
    
    def isElem(self,x,y):
        return ((x**3 + self.a*x + self.b - y**2)%self.p ==0)

@dataclass
class Coordinate:
    x: int
    y: int  

Point = str | Coordinate

def pointNegation(curve:EllipticCurve, point:Point):
    match point:
        case str(string):
            return "infinity"
        case Coordinate(x,y):
            return Coordinate(x,-y)

curve = EllipticCurve(-2,4)
print(curve.y2Value(2))
print(curve) 
print(pow(0.5,2))

curve2 = FiniteFieldEllipticCurve(0,7,17)
print(curve2.isElem(9,15))
print(curve2.isElem(5,8))

coord = Coordinate(3,4)
print(pointNegation(curve, Coordinate(3,4)))