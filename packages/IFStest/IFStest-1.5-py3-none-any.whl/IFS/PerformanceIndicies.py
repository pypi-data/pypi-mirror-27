import numpy as np

def error_calc(A,B,reversed = False,mask = np.array([]) , List = True):
    A = np.array(A)
    B = np.array(B)

    x = len(A)
    y = len(A[0])

    Accuracy = 0
    Precision = 0
    Recall = 0
    tn = 0
    tp = 0
    fn = 0
    fp = 0

    if mask.size == 0:
        mask = np.ones((x,y))

    A_msk = A == 0
    A = ~A_msk
    A = A.astype(int)

    B_msk = B == 0

    B = B_msk
    if reversed == 1:
        B = ~B
        B = B.astype(int)

    A = np.array(A)
    B = np.array(B)

    ff = A[A == 1]
    aa = B[A == 1]

    tp = np.sum([ff == aa])

    ff = A[A == 0]
    aa = B[A == 0]

    tn = np.sum([ff == aa])

    ff = A[A == 0]
    aa = B[A == 0]

    fp = np.sum([ff != aa])

    ff = A[A == 1]
    aa = B[A == 1]

    fn = np.sum([ff != aa])

    Accuracy = (tp + tn) / float(tp + tn + fp + fn)
    Precision = tp / float(tp + fp)
    Recall = tp / float(tp + fn)
    SimilarityMeasure = np.sum(1 - np.absolute(A - B)) / float(x * y)
    Fmeasure = 2 * (Precision * Recall) / float(Precision + Recall)
    BitErrorRate = (fp + fn) / float(tp + tn + fp + fn)


    if List:
        return np.array([Accuracy , Precision , Recall , SimilarityMeasure , Fmeasure , BitErrorRate])
    else:
        dictionary = {'Accuracy' : Accuracy , 'Precision' : Precision , 'Recall' : Recall , 'SimilarityMeasure' : SimilarityMeasure,
                      'Fmeasure' : Fmeasure , 'BitErrorRate' : BitErrorRate}
        return dictionary

