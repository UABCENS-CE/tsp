from scipy.stats import levy
import random
from random import randint

#BURBUJA#
def Burbuja(lista,i,j):
    temp = lista[i]
    lista[i]=lista[j]
    lista[j]=temp
    
#2opt#
def DosOpt(Nido,a,b):
    Nido = Nido[0].copy()
    Burbuja(Nido,a,b)
    _ , y = evaluate_tour(tsp_data,Nido)
    return (Nido, y)
  
#doblebridge#
def DobleBridge(Nido,a,b,c,d):
    Nido = Nido[0].copy()
    Burbuja(Nido,a,b)
    Burbuja(Nido,c,d)
    _ , y = evaluate_tour(tsp_data,Nido)
    return (Nido, y)

#Busqueda cuckoo#
from scipy.stats import levy
import random
from random import randint


#BURBUJA#
def Burbuja(lista,i,j):
    temp = lista[i]
    lista[i]=lista[j]
    lista[j]=temp
    
#2opt#
def DosOpt(Nido,a,b):
    Nido = Nido[0].copy()
    Burbuja(Nido,a,b)
    _ , y = evaluate_tour(tsp_data,Nido)
    return (Nido, y)
  
#doblebridge#
def DobleBridge(Nido,a,b,c,d):
    Nido = Nido[0].copy()
    Burbuja(Nido,a,b)
    Burbuja(Nido,c,d)
    _ , y = evaluate_tour(tsp_data,Nido)
    return (Nido, y)


def CuckooSearch(NumNidos, MaxGen, MatrizDist):

    pa = int(0.6*NumNidos)
    n = len(MatrizDist)
    Nidos = []


    #CREAR NIDOS ALEATORIAMENTE#
    for i in range(NumNidos):
        x=random_tour(tsp_data)
        _ , y = evaluate_tour(tsp_data,x)
        Nidos.append((x.copy(), y))



    #ORDENAR NIDOS DENTRO DE LA LISTA POR FITNESS#
    Nidos.sort(key=lambda s: s[1])


    #INICIO DE CICLO#
    for t in range(MaxGen):
        band=0
        #USANDO LA DISTRIBUCION LEVY GENERAR UN NUMERO PARA EL NUMERO DE MOVIMIENTOS#
        r = levy.rvs()
        if int(r)>100:
            r=r/10
            band=1

        #SELECCIONAR UN NIDO EN EL CUAL BASARSE PARA CREAR EL HUEVO QUE EL CUCKOO QUIERE DEJAR#
        Cuckoo = Nidos[randint(0,NumNidos-1)]

        #VER QUE MOVIMIENTO SE VA A HACER Y CUANTAS VECES#
        if band==1:
            for i in range(int(r)):
                Cuckoo = DobleBridge(Cuckoo,randint(0,n-1),randint(0,n-1),randint(0,n-1),randint(0,n-1))
        else:
            for i in range(int(r)):
                Cuckoo = DosOpt(Cuckoo,randint(0,n-1),randint(0,n-1))

        #SELECCIONAR UN NIDO ALEATORIO#
        NidoAleatorio = randint(0,NumNidos-1)

        #COMPARAR NIDO SLECCIONADO Y HUEVO DE CUCKOO#
        if(Nidos[NidoAleatorio][1]>Cuckoo[1]):
            Nidos[NidoAleatorio] = Cuckoo

        Nidos.sort(key=lambda s: s[1])

        #ELIMINAR PEORES NIDOS#
        for i in range(pa):
            Nidos.pop()

        #CREAR NUEVOS NIDOS#
        for i in range(pa):
            x=random_tour(tsp_data)
            _ , y = evaluate_tour(tsp_data,x)
            Nidos.append((x.copy(), y))

        #ORDENAR NIDOS#
        Nidos.sort(key=lambda s: s[1])

    
    return Nidos[0][0]