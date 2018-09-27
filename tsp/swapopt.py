import random

def swap_2opt(tour,n=[]):
	if n == []:
		i,j = random.sample(range(len(tour)), 2)
		i,j = sorted([i,j])
	else:
		i,j = n
    nuevo_tour = tour[0:i]
    nuevo_tour.extend(reversed(tour[i:j+1]))
    nuevo_tour.extend(tour[j+1:])
    return nuevo_tour

def swap_3opt(O,t,n=[]):
    tour = t[:]
    if n == []:
        i,j,k = random.sample(range(len(tour)), 3)
        i,j,k = sorted([i,j,k])
    else:
        i,j,k = n
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
    # Elegir Mejor Intercambio
    m = np.argmin(d)
    # Intercambio Aleatorio
    #m = np.random.randint(1,len(d))
    if m == 1:
        tour[i:j] = reversed(tour[i:j])
    elif m == 2:
        tour[j:k] = reversed(tour[j:k])
    elif m == 3:
        tour[i:k] = reversed(tour[i:k])
    elif m == 4:
        tour[j:k] = reversed(tour[j:k])
        tour[i:k] = reversed(tour[i:k])
    elif m == 5:
        tour[i:j] = reversed(tour[i:j])
        tour[i:k] = reversed(tour[i:k])
    elif m == 6:
        tour[i:j] = reversed(tour[i:j])
        tour[j:k] = reversed(tour[j:k])
    elif m == 7:
        tour[i:k] = tour[j:k] + tour[i:j]
    return tour