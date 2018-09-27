import numpy as np

def tsp_3opt(O,t):
    tour = t[:]
    delta = 0
    for (a,b,c) in all_segments(len(tour)):
        delta = reverse_if_better(O,tour,a,b,c)
    if delta < 0:
        return tsp_3opt(tour)
    return tour

def reverse_if_better(O,tour,i,j,k):
    A,B,C,D,E,F = tour[i-1],tour[i],tour[j-1],tour[j],tour[k-1],tour[k%len(tour)]
    d0 = O._M[A][B] + O._M[C][D] + O._M[E][F]
    d1 = O._M[A][C] + O._M[B][D] + O._M[E][F]
    d2 = O._M[A][B] + O._M[C][E] + O._M[D][F]
    d3 = O._M[F][B] + O._M[C][D] + O._M[E][A]
    d4 = O._M[F][B] + O._M[C][E] + O._M[D][A]
    d5 = O._M[F][C] + O._M[B][D] + O._M[E][A]
    d6 = O._M[A][C] + O._M[B][E] + O._M[D][F]
    d7 = O._M[A][D] + O._M[E][B] + O._M[C][F]
    d = [d0,d1,d2,d3,d4,d5,d6,d7]
    m = np.argmin(d)
    if m == 1:
        tour[i:j] = reversed(tour[i:j])
        return -d0 + d1
    elif m == 2:
        tour[j:k] = reversed(tour[j:k])
        return -d0 + d2
    elif m == 3:
        tour[i:k] = reversed(tour[i:k])
        return -d0 + d3
    elif m == 4:
        tour[j:k] = reversed(tour[j:k])
        tour[i:k] = reversed(tour[i:k])
        return -d0 + d4
    elif m == 5:
        tour[i:j] = reversed(tour[i:j])
        tour[i:k] = reversed(tour[i:k])
        return -d0 + d5
    elif m == 6:
        tour[i:j] = reversed(tour[i:j])
        tour[j:k] = reversed(tour[j:k])
        return -d0 + d6
    elif m == 7:
        tour[i:k] = tour[j:k] + tour[i:j]
        return -d0 + d7
    return d0

def all_segments(N):
    return [(i,j,k)
           for i in range(N)
           for j in range(i+2,N)
           for k in range(j+2,N+(i>0))]