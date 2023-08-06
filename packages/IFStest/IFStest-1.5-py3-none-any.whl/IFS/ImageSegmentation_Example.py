import numpy as np
import cv2
from Applications import distanceThreshold

I = np.array(cv2.imread('rice.png' , cv2.IMREAD_GRAYSCALE))


x = len(I)
y=len(I[0])

n=x*y

thr_level = distanceThreshold(I , 'defIFSDistance')


A = np.zeros((x,y))

msk1 = I < thr_level[0]
msk2 = I >= thr_level[0]

A[msk1] = 255
A[msk2] = 0 

cv2.imshow("thr :" + str(thr_level) , A.astype("uint8"))
cv2.waitKey(10000)