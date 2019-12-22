import copy
import numpy as np
import cv2
import sys

def star_op(data,kernel):
    s = 0
    for i in range(len(data)):
        s += np.dot(data[i,:],kernel[:,i])
    return s

def tf(data,kernel):
    G = np.zeros(data.shape)
    g = np.zeros(tuple(np.subtract(data.shape, (2, 2))))
    S = np.zeros((1,np.size(data,1)))
    for i in range(np.size(data,0)-(np.size(kernel,0)-1)):
        for j in range(np.size(data,1)-(np.size(kernel,0)-1)):
            g[i,j] = star_op(data[i:i+len(kernel),j:j+len(kernel)],kernel)

    G[1:np.size(data,0)-1,1:np.size(data,1)-1]=g
    return G

def nms(M):
    A=copy.deepcopy(M)
    N = np.zeros(A.shape)
    for i in range(2,np.size(A,0)-2):
        for j in range(2,np.size(A,1)-2):
            #0
            if (((t[i,j] >= -22.5) and (t[i,j] <= 22.5)) or (t[i,j] >= 157.5) or (t[i,j] <= -157.5)):
                if ((A[i,j] >= A[i,j+1]) and (A[i,j] >= A[i,j-1])):
                    N[i,j] = A[i,j]
                else:
                    N[i,j] = 0.
            #45    
            elif (((t[i,j] > 22.5) and (t[i,j] < 67.5)) or ((t[i,j] < -112.5) and (t[i,j] > -157.5))):
                if ((A[i,j] >= A[i+1,j+1]) and (A[i,j] >= A[i-1,j-1])):
                    N[i,j] = A[i,j]
                else:
                    N[i,j] = 0.
            #90   
            elif (((t[i,j] >= 67.5) and (t[i,j] <= 112.5)) or ((t[i,j] >= -112.5) and (t[i,j] <= -67.5))):
                if ((A[i,j] >= A[i,j+1]) and (A[i,j] >= A[i,j-1])):
                    N[i,j] = A[i,j]
                else:
                    N[i,j] = 0.
            #135    
            elif (((t[i,j] > 112.5) and (t[i,j] < 157.5)) or ((t[i,j] < -22.5) and (t[i,j] > -67.5))):
            
                if ((A[i,j] >= A[i+1,j-1]) and (A[i,j] >= A[i-1,j+1])):
                    N[i,j] = A[i,j]
                else:
                    N[i,j] = 0.
    return N

img = cv2.imread(sys.argv[1],0)

Gx = (1./3)*np.matrix('-1 0 1;-1 0 1;-1 0 1')
Gy_1 = (1./3)*np.matrix('-1 -1 -1;0 0 0;1 1 1')
#Gy_2 = (1./3)*np.matrix('1 1 1;0 0 0;-1 -1 -1')



fx=tf(img,Gx)
fy_1=tf(img,Gy_1)
#fy_2=tf(img,Gy_2)

M = np.sqrt(fx**2+fy_1**2)
cv2.imwrite('magni.png',M)
t = np.arctan2(fx, fy_1)*180/np.pi;
cv2.imwrite('theta.png',t)              
cv2.imwrite(sys.argv[2],nms(M))

















