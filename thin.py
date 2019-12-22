import numpy as np
import cv2
import sys

def bin2bool(img):
    """object 1.0, background 0.0"""
    img = np.where(img == 255, img, 1.0) 
    img = np.where(img == 1.0, img, 0.0) 
    return img

def bool2bin(img):
    """object 0.0, background 255."""
    img = np.where(img == 1.0, img, 255) 
    img = np.where(img == 255., img, 0.0) 
    return img

def NZ(list):
    nz = 0 
    for e in range(len(list)-1):
        if list[e] == 1.0:
            nz += 1
    return nz

def NTR(m,i,j):
    ntr = 0
    p2 = m[i-1][j]
    p3 = m[i-1][j-1]
    p4 = m[i][j-1]
    p5 = m[i+1][j-1]
    p6 = m[i+1][j]
    p7 = m[i+1][j+1]
    p8 = m[i][j+1]
    p9 = m[i-1][j+1]
    p = [p2,p3,p4,p5,p6,p7,p8,p9,p2]
    for e in range(len(p)-1):
        if (p[e] == 0.0) and (p[e+1] == 1.0):
            ntr += 1
    return ntr
def p234567892(m,i,j):
    p2 = m[i-1][j]
    p3 = m[i-1][j-1]
    p4 = m[i][j-1]
    p5 = m[i+1][j-1]
    p6 = m[i+1][j]
    p7 = m[i+1][j+1]
    p8 = m[i][j+1]
    p9 = m[i-1][j+1]
    return [p2,p3,p4,p5,p6,p7,p8,p9,p2]


img = cv2.imread(sys.argv[1],0)
u2 = bin2bool(img);
u1 = bin2bool(img);

ndel = 0
for l in range(100):
    u2 = np.zeros((np.size(img,0),np.size(img,1)))
    for i in range(2,np.size(u1,0)-2):
        for j in range(2,np.size(u1,1)-2):
        
            p = p234567892(u1,i,j)
        
            if u1[i][j] == 1.0:
            
                p248 = p[0]*p[2]*p[6] #248 NTR(p2)
                p246 = p[0]*p[2]*p[4] #246 NTR(p4)
                if ((NZ(p) >= 2) and (NZ(p) <= 6)) and (NTR(u1,i,j)==1) and ((p248 == 0.0) or (NTR(u1,i-1,j)!= 1)) and ((p246==0) or (NTR(u1,i,j-1)!=1)):
                    u2[i][j] = 0.0
                    ndel += 1 
                else:
                    u2[i][j] = u1[i][j]
            else:
                u2[i][j] = u1[i][j]
            
            p = []
    if ndel == 0:
        break
    else:
        u1 = u2
        ndel = 0


img = bool2bin(u2)
cv2.imwrite(sys.argv[2],img)



