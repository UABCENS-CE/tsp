def tsp_2opt(O,tour):
    mejor_tour = tour[:]
    mejor_distancia = O.evaluate_tour(mejor_tour)
    mejora = True
    while mejora:
        mejora = False
        for i in range(len(mejor_tour)-1):
            for j in range(i+1,len(mejor_tour)):
                nuevo_tour = swap2opt(mejor_tour,i,j)
                nueva_distancia = O.evaluate_tour(nuevo_tour)
                if nueva_distancia < mejor_distancia:
                    mejor_distancia = nueva_distancia
                    mejor_tour = nuevo_tour
                    mejora = True
                    break
            if mejora:
                break
    return mejor_tour

def swap2opt(tour,i,j):
    nuevo_tour = tour[0:i]
    nuevo_tour.extend(reversed(tour[i:j+1]))
    nuevo_tour.extend(tour[j+1:])
    return nuevo_tour