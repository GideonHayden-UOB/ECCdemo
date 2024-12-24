import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt 
from dataclasses import dataclass
import math
import cProfile

class FiniteFieldEllipticCurve:
    #elliptic curves over finite fields have the form y^2 = x^3 + ax + b (mod p) represented by these attributes
    def __init__(self, a, b, p:int):
        self.a = a
        self.b = b
        self.p = p

    def __str__(self):
        return "y^2 = x^3 + "+str(self.a)+"x + "+str(self.b)+" (mod "+str(self.p)+")"
    
    def y2Value(self, x):
        return ((pow(x,3)+ self.a*x + self.b) %self.p)
    
    def isElem(self,x,y):
        return ((x**3  - y**2 + self.a*x + self.b)%self.p ==0)
    
    def generatePoints(self):
        xs = []
        ys = []

        for x in range(self.p):
            if isQuadraticResidue(self.p, self.y2Value(x)):
                squareRoots = sqrtModPrime(self.p, self.y2Value(x))

                for y in squareRoots:
                    ys.append(y)
                    xs.append(x)
        return xs,ys

    def pointAddition(self, xp, yp, xq, yq):
        if (xp == yp == None):
            return xq,yq
        if (xq == yq == None):
            return xp,yp
        
        assert self.isElem(xp,yp), "p not on the curve"
        assert self.isElem(xq,yq), "q not on the curve"
        
        if (xq==xp and (yq+yp)%self.p==0):
            return None,None
        elif (xq==xp and yq==yp):
            return self.pointDouble(xp,yp)

        else:
            lambdaP = (((yq-yp)%self.p) * pow((xq-xp),-1,self.p)) %self.p
            xr = (pow(lambdaP,2,self.p) - xp - xq)%self.p
            yr = (lambdaP*(xp-xr) - yp) %self.p
            return xr,yr

    def pointDouble(self, x, y):
        lambdaP = (((3*pow(x,2,self.p) + self.a)%self.p) * pow(2*y,-1,self.p)) %self.p 
        xr = (pow(lambdaP,2,self.p) - 2*x)%self.p
        yr = (lambdaP*(x-xr) - y) %self.p
        return xr,yr
    
    def naivePointMultiplication(self,x,y,s):
        nextx, nexty = x,y
        for i in range(s-1):
            nextx, nexty = self.pointAddition(x,y,nextx,nexty)
        return nextx,nexty
    
    def pointMultiplication(self,x,y,s):

        assert(isinstance(s,int) and s>=0),"can only multiply by non negative integers"
        assert(self.isElem(x,y)),"must be a point on the curve"
        if s==0:
            return None,None
        else:
            s = bin(s)
            s = str(s)
            s = s[2:]
            resx,resy = None,None
            tempx,tempy = x,y
            for bit in s[::-1]:
                if (bit == '1'):
                    resx,resy = curve.pointAddition(resx,resy,tempx,tempy)
                tempx,tempy = curve.pointAddition(tempx,tempy,tempx,tempy)
                            
            return resx,resy

    def generatePointsFromGenerator(self,x,y):
        assert(self.isElem(x,y)),"not a point on the curve"
        nextx,nexty = self.pointDouble(x,y)
        xs = [x,nextx]
        ys = [y,nexty]
        while (nextx != x and nexty != y):
            nextx,nexty= self.pointAddition(x,y,nextx,nexty)
            xs.append(nextx)
            ys.append(nexty)
        return xs,ys

    def PointCompression(self,x,y):
        return x,(y%2)

    def PointDecompression(self,x,ybit):
        y = sqrtModPrime(self.p,pow(x, 3, self.p) + self.a * x + self.b)[0]
        if bool(ybit) == bool(y & 1):
            return (x, y)
        return x, self.p - y

    





def isQuadraticResidue(p,a):
    if (a==0 or a==1):
        return True
    else:
        ls = pow(a,(p-1)>>1,p)
        if (ls==1):
            return True
        else:
            return False

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
        return [n]
    else:
        if (p%4==3):
            r = pow(n,(p+1)>>2,p)
        else:
            r = tonelliShanks(p,n)
        if (r==0):
            return [r]
        else:
            return r,p-r



#implements diffie-hellman key exchange
#parameters are curve, generator point for the curve (consisting of gx,gy) and private keys for alice(a) and bob(b): da,db respectively
def diffieHellmanKeyExchangeExample(curve:FiniteFieldEllipticCurve,gx,gy,da,db):
    Qa, Qb = curve.pointMultiplication(gx,gy,da), curve.pointMultiplication(gx,gy,db) #generates the public keys of alice and bob
    
    print("Curve: "+str(curve)+"\n"+
          "Generator: "+str((gx,gy))+"\n"+
          "Alice's private key: "+str(da)+", Alice's public key: "+str(Qa)+"\n"+
          "Bob's private key: "+str(db)+", Bob's public key: "+str(Qb))
    
    xk,yk = curve.pointMultiplication(Qa[0],Qa[1],db)
    xk2,yk2 = curve.pointMultiplication(Qb[0],Qb[1],da)
    print("Each person calculates the product of their private key with the other's private key \nThis gives the same value for each person but is not known to other people")
    print("Shared secret is the x value of the calculated point: ",xk)
    print("Alice and Bob now have a shared secret that can be used in a symmetric key algorithm to encrypt and decrypt messages ")


curve = FiniteFieldEllipticCurve(0,3,11)
#print(curve.generatePoints())
xs,ys = curve.generatePoints()
fig, (ax1) = plt.subplots(1, 1)
fig.suptitle('y^2 = x^3 + '+str(curve.b)+ '(mod '+str(curve.p)+')')
fig.set_size_inches(6, 6)
ax1.set_xticks(range(0,curve.p))
ax1.set_yticks(range(0,curve.p))
plt.grid()
plt.scatter(xs, ys)
plt.plot()
#plt.show()



diffieHellmanKeyExchangeExample(curve,4,10,3,5)

#print(curve.generatePointsFromGenerator(4,10))

