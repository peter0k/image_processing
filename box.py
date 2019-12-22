import numpy as np
import cv2
import time
import sys


def star_op(data,kernel):
    s = 0
    for i in range(len(data)):
        s += np.dot(data[i,:],kernel[:,i])
    return s

#read image
img = cv2.imread(sys.argv[1],0)


nlist = [3,7,11]
for n in nlist:
    #boxfilter
    F=np.ones((n,n))


    data = img
    kernel = F*1./n**2


    G = np.zeros(data.shape)
    g = np.zeros(tuple(np.subtract(data.shape, (2, 2))))
    S = np.zeros((1,np.size(data,1)))

    #by definition
    start = time.time()
    for i in range(np.size(data,0)-(np.size(kernel,0)-1)):
        for j in range(np.size(data,1)-(np.size(kernel,0)-1)):
            g[i,j] = star_op(data[i:i+len(kernel),j:j+len(kernel)],kernel)

    end = time.time()
    print n,"bydef_filter",(end - start)



    G[1:np.size(data,0)-1,1:np.size(data,1)-1]=g
    G[:,-(int(np.floor(n/2))+1):-1] = (np.ones((np.size(G,0),int(np.floor(n/2))))*g.mean())
    cv2.imwrite(sys.argv[1]+str(n)+'_bydef.png',G)


    #running filter
    h,w = img.shape
    IM = np.zeros((h,w))

    start = time.time()
    S = np.sum(img[0:n,:],axis=0)
    for j in range(1,h-(n-1)):
        ws = np.sum(S[0:n])
        IM[j,0] = ws/(n*n)
        for i in range(1,len(S)-(n-1)):

            ws = ws+S[i+(n-1)]-S[i-1]
            IM[j,i] = ws/(n*n)
            
        S = S + img[j+(n-1),:]-img[j-1,:]
    end = time.time()
    print n,"run_filter:",(end - start)

    cv2.imwrite(sys.argv[1]+str(n)+'_run.png',IM)



