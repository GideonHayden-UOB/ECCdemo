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
        return (np.sqrt(self.y2Value(x)))
    
    def isElem(self,x,y):
        return ((x**3 + self.a*x + self.b - y**2)%self.p ==0)

def tonelli_Shanks(p,n):
    Q = p-1
    S = 0
    while (Q%2==0):
        Q = Q/2
        S = S+1
    Q = int(Q)
    z= np.random.randint(2,p-2)
    while (isQuadraticResidue(p,z)):
        z= np.random.randint(2,p-2)

    M = S
    c = (z**Q ) %p
    t = (n**Q)  %p
    R = (n**int((Q+1)/2))  %p

    while(True):
        if (t==0):
            return 0
        elif (t==1):
            return R
        else:
            i=1
            while (t**(2**i)%p != 1):
                i = i+1
                print(i,t)
                if (i==M):
                    raise Exception("n is not a quadratic residue") 
            b = (c**(2**(M-i-1))) %p
            M=i %p
            c = (b**2) %p
            t = (t*(b**2)) %p
            R = (R*b) %p



def isQuadraticResidue(p,a):
    ls = a**(int((p-1)/2))
    if (ls%p==1):
        return True
    else:
        return False


curve2 = FiniteFieldEllipticCurve(0,7,17)
#print(curve2.isElem(9,15))
#print(curve2.isElem(5,8))

print(tonelli_Shanks(101,4))
