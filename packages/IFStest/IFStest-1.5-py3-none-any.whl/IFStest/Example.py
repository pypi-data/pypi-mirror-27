import numpy as np
import IFS as ifs
import random as rand
from IFS.Measures.Distances import distance
from IFS.Measures.Similarities import similarity
from IFS.Measures.Miscellaneous import miscs

A = np.zeros((100,3))
B = np.zeros((100,3))

for i in range(len(A)):
	A[i,0] = rand.random()
	
A[:,2] = (1-A[:,0])  - (1 - A[:,0]) / (1.0+0.2*A[:,0])
A[:,1] = 1 - A[:,2] - A[:,0]

for i in range(len(B)):
	B[i,0] = rand.random()
	
B[:,2] = (1-B[:,0])  - (1 - B[:,0]) / (1.0+0.2*B[:,0])
B[:,1] = 1 - B[:,2] - B[:,0]

Distance = distance('yangChiclanaDistance' , A,B,type='nH')
print('Distance : '+ str(Distance))

w = np.full(len(A), 1.0/len(A))
p=2
a = 0.3
b = 0.3
c = 0.4

Similarity = similarity('liuSimilarity',A,B,p,w,a=a,b=b,c=c)
print('Similarity : '+ str(Similarity))

A = A[:,0:2]
A[: , 1] = 1-A[:,0]

B= B[:,0:2]
B[: , 1] = 1-B[:,0]

Diverence = miscs('tamalikaDivergence' , A,B)#tamalikaDivergence
print('Diverence : ' + str(Diverence))