import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt 
from dataclasses import dataclass

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

curve2 = FiniteFieldEllipticCurve(0,7,17)
print(curve2.isElem(9,15))
print(curve2.isElem(5,8))