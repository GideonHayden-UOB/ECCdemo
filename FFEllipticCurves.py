import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt 
from dataclasses import dataclass
import math

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
        return (math.sqrt(self.y2Value(x)))
    
    def isElem(self,x,y):
        return ((x**3  - y**2 + self.a*x + self.b)%self.p ==0)

def tonelliShanks(p,n):
    Q = p-1
    S = 0
    while (Q%2==0):
        Q = Q>>1
        S = S+1
    Q = int(Q)
    z= np.random.randint(2,p-2)
    while (isQuadraticResidue(p,z)):
        z= np.random.randint(2,p-2)

    M = S
    c = pow(z,Q,p)
    t = pow(n,Q,p)
    R = pow(n,(Q+1)>>1,p)

    while(True):
        if (t==0):
            return 0
        elif (t==1):
            return R
        else:
            i=1
            while (pow(t,2**i,p) != 1):
                i = i+1
                if (i==M):
                    raise Exception("n="+str(n)+" is not a quadratic residue mod "+str(p)) 
            b = pow(c,2**(M-i-1),p)
            M = i %p
            c = pow(b,2,p)
            t = (t*(b**2)) %p
            R = (R*b) %p

def sqrtModPrime(p,n):
    n=n%p
    if (p==2):
        return n
    else:
        if (p%4==3):
            r = pow(n,(p+1)>>2,p)
        else:
            r = tonelliShanks(p,n)
        return r,p-r


def isQuadraticResidue(p,a):
    if (a==0 or a==1):
        return True
    else:
        ls = pow(a,(p-1)>>1,p)
        if (ls==1):
            return True
        else:
            return False


curve2 = FiniteFieldEllipticCurve(0,7,17)
#print(curve2.isElem(9,15))
#print(curve2.isElem(5,8))


print(isQuadraticResidue(101,4))
print(tonelliShanks(101,4))
print(list(sqrtModPrime(11,5)))