import numpy as np
import cv2
import sys

def fq(P,t0,t):
    """weight of C1"""
    q = 0
    for i in range(t0,t+1):
        q += P[i]
    return q

def fmu(P,t0,t): 
    mu = 0
    for i in range(t0,t+1):
        mu += i*P[i]
        #print i
    return (1/fq(P,t0,t))*mu

def fvar(P,t0,t):
    mu = fmu(P,t0,t)
    vart = 0
    for i in range(t0,t+1):
        vart += ((i-mu)**2) * P[i]
    return (1/fq(P,t0,t))*vart

def img2bool(img,t_opt):
    for i in range(np.size(img,0)):
        for j in range(np.size(img,1)):
            if img[i][j] < t_opt:
                img[i][j] = 0
            else:
                img[i][j] = 255
    return img

img = cv2.imread(sys.argv[1],0)


p = np.zeros(256) #intensity histogram
for i in range(np.size(img,0)):
    for j in range(np.size(img,1)):
        p[img[i][j]] += 1

P=p/np.sum(p) #histogram normalized with number of pixels

mu = 0 #weighted histogram average
for i in range(len(P)):
    mu += i*P[i]

varP = 0 #histogram variance
for i in range(len(P)):
    varP += (i-mu)**2 * P[i]



sB_opt = -5000
for t in range(1,254):
    q1 = fq(P,0,t)+P[t+1]
    # mean of C1
    m1 = (fq(P,0,t)*fmu(P,0,t)+(t+1)*P[t+1])/fq(P,0,t+1)
    # mean of C2
    m2 = (mu-fq(P,0,t+1)*fmu(P,0,t+1))/(1-fq(P,0,t+1))
    # class distance
    sB = q1*(1-q1)*(m1-m2)**2
    if sB > sB_opt: # max of class distance (between-class variance)
        sB_opt = sB
        t_opt = t


print "t_opt",t_opt
cv2.imwrite(sys.argv[2],img2bool(img,t_opt))
