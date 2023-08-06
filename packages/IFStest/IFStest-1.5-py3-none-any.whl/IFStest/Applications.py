import numpy as np
from IFS.Measures.Distances import distance
from IFS.Measures.Similarities import similarity
from IFS.Measures.Miscellaneous import miscs

########################################################################################################################

def distanceThreshold(I , dist , w = np.array([]) , lamdbda = 0.2 , mask = np.array([]) , ty = 'H'):
    I = np.array(I)
    x = len(I)
    y = len(I[0])
    if mask.size == 0:
        mask = np.ones((x,y))
    if w.size == 0:
        w = np.full(x*y , 1.0/x*y)

    L = 256

    I = I.reshape(-1)

    w = np.full((x * y), 1.0 / (x * y))

    mask = mask.reshape(-1)
    mask = np.array(mask)
    maskSkip = (mask == 0)
    nmsk = maskSkip.reshape(-1)

    fmaxa = np.max(I[~nmsk])
    fmina = np.min(I[~nmsk])
    c = 1.0 / float(fmaxa - fmina)

    hs = np.zeros(256)
    for i in range(256):
        hs[i] = np.sum([I == i])
    hs = hs.astype("int")

    np.reshape(I, (x * y, 1))

    A = np.zeros([x * y, 3])
    B = np.zeros([x * y, 3])
    B[:, 0] = 1

    mx = np.zeros(x * y)

    distances = np.zeros(256)

    for t in range(-1, L - 1):  # L - 1):
        sum1 = np.sum(hs[range(t + 1)] * np.array(range(t + 1)))
        sum2 = np.sum(hs[range(t + 1)])
        if sum2 == 0:
            m0 = 0
        else:
            m0 = sum1 / float(sum2)

        sum1 = np.sum(hs[range(t + 2, L - 1)] * np.array(range(t + 2, L - 1)))
        sum2 = np.sum(hs[range(t + 2, L - 1)])
        if (sum2 == 0):
            m1 = 0
        else:
            m1 = sum1 / float(sum2)

        up = np.array(I > t)
        low = np.array(I <= t)

        mx[up] = np.exp(-c * np.absolute(I[up & ~maskSkip] - m1))
        mx[low] = np.exp(-c * np.absolute(I[low & ~maskSkip] - m0))
        mx[maskSkip] = 1

        A[:, 0] = np.array(mx)
        A[:, 2] = (1 - mx) - np.divide((1 - mx), (1.0 + lamdbda * mx.astype(np.float)))
        A[:, 1] = 1 - A[:, 2] - A[:, 0]

        distances[t+1] = distance(dist, A, B, w=w , type=ty)

    level = np.argmin(distances)
    value = np.min(distances)
    return level, value

########################################################################################################################

def similarityThreshold(I , sim , w = np.array([]) , lamdbda = 0.2 , mask = np.array([]) , ty = 'H'):
    I = np.array(I)
    x = len(I)
    y = len(I[0])
    if mask.size == 0:
        mask = np.ones((x,y))
    if w.size == 0:
        w = np.full(x*y , 1.0/x*y)

    L = 256

    I = I.reshape(-1)

    w = np.full((x * y), 1.0 / (x * y))

    mask = mask.reshape(-1)
    mask = np.array(mask)
    maskSkip = (mask == 0)
    nmsk = maskSkip.reshape(-1)

    fmaxa = np.max(I[~nmsk])
    fmina = np.min(I[~nmsk])
    c = 1.0 / float(fmaxa - fmina)

    hs = np.zeros(256)
    for i in range(256):
        hs[i] = np.sum([I == i])
    hs = hs.astype("int")

    np.reshape(I, (x * y, 1))

    A = np.zeros([x * y, 3])
    B = np.zeros([x * y, 3])
    B[:, 0] = 1

    mx = np.zeros(x * y)

    similarities = np.zeros(256)

    for t in range(-1, L - 1):  # L - 1):
        sum1 = np.sum(hs[range(t + 1)] * np.array(range(t + 1)))
        sum2 = np.sum(hs[range(t + 1)])
        if sum2 == 0:
            m0 = 0
        else:
            m0 = sum1 / float(sum2)

        sum1 = np.sum(hs[range(t + 2, L - 1)] * np.array(range(t + 2, L - 1)))
        sum2 = np.sum(hs[range(t + 2, L - 1)])
        if (sum2 == 0):
            m1 = 0
        else:
            m1 = sum1 / float(sum2)

        up = np.array(I > t)
        low = np.array(I <= t)

        mx[up] = np.exp(-c * np.absolute(I[up & ~maskSkip] - m1))
        mx[low] = np.exp(-c * np.absolute(I[low & ~maskSkip] - m0))
        mx[maskSkip] = 1

        A[:, 0] = np.array(mx)
        A[:, 2] = (1 - mx) - np.divide((1 - mx), (1.0 + lamdbda * mx.astype(np.float)))
        A[:, 1] = 1 - A[:, 2] - A[:, 0]

        similarities[t+1] = similarity(sim, A, B, w=w, type=ty)

    level = np.argmin(similarities)
    value = np.min(similarities)
    return level, value

#########################################################################################################################

def miscThreshold(I, mis, k=0.5, lamdbda=0.2, mask=np.array([])):
    I = np.array(I)
    x = len(I)
    y = len(I[0])
    if mask.size == 0:
        mask = np.ones((x,y))

    L = 256

    I = I.reshape(-1)

    w = np.full((x * y), 1.0 / (x * y))

    mask = mask.reshape(-1)
    mask = np.array(mask)
    maskSkip = (mask == 0)
    nmsk = maskSkip.reshape(-1)

    fmaxa = np.max(I[~nmsk])
    fmina = np.min(I[~nmsk])
    c = 1.0 / float(fmaxa - fmina)

    hs = np.zeros(256)
    for i in range(256):
        hs[i] = np.sum([I == i])
    hs = hs.astype("int")

    np.reshape(I, (x * y, 1))

    A = np.zeros([x * y, 3])
    B = np.zeros([x * y, 3])
    B[:, 0] = 1

    mx = np.zeros(x * y)

    misc = np.zeros(256)

    for t in range(-1, L - 1):  # L - 1):
        sum1 = np.sum(hs[range(t + 1)] * np.array(range(t + 1)))
        sum2 = np.sum(hs[range(t + 1)])
        if sum2 == 0:
            m0 = 0
        else:
            m0 = sum1 / float(sum2)

        sum1 = np.sum(hs[range(t + 2, L - 1)] * np.array(range(t + 2, L - 1)))
        sum2 = np.sum(hs[range(t + 2, L - 1)])
        if (sum2 == 0):
            m1 = 0
        else:
            m1 = sum1 / float(sum2)

        up = np.array(I > t)
        low = np.array(I <= t)

        mx[up] = np.exp(-c * np.absolute(I[up & ~maskSkip] - m1))
        mx[low] = np.exp(-c * np.absolute(I[low & ~maskSkip] - m0))
        mx[maskSkip] = 1

        A[:, 0] = np.array(mx)
        A[:, 2] = (1 - mx) - np.divide((1 - mx), (1.0 + lamdbda * mx.astype(np.float)))
        A[:, 1] = 1 - A[:, 2] - A[:, 0]

        misc[t + 1] = miscs(mis,A,B,k,x,y)

    level = np.argmin(misc)
    value = np.min(misc)
    return level, value
