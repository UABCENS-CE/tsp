
# coding: utf-8

# In[13]:


#Librerias
import numpy as np

#Funciones
def distance(node1,node2,axes='X'):
    if axes == 'X':
        r = node1[0] - node2[0]
        return abs(r)
    elif axes == 'Y':
        r = node1[1] - node2[1]
        return abs(r)
    
def euc_dist(node1,node2):
    x1,y1 = node1[1],node1[2]
    x2,y2 = node2[1],node2[2]
    return ((y2-y1)**2+(x2-x1)**2)**.5

#Clase Region
class region:
    def __init__(self,x1,y1,x2,y2,linewidth=1,edgecolor='g',facecolor='none',alpha=.4):
        """
        x1,y1 corresponden al punto inferior derecho
        x2,y2 corresponden al punto superior izquierdo
        """
        #Coordenadas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        #Atributos
        self.cities = [] #Sera una lista con coordenadas correspondientes a las ciudades
        self.tour = [] #Sera una lista con el tour correspondiente
        #Detalles esteticos
        self.linewidth = linewidth
        self.edgecolor = edgecolor
        self.facecolor = facecolor
        self.alpha = alpha
        
    def add_city(self,point):
        self.cities.append(point)
        
    def fill_region(self,nodos):
        for nodo in nodos:
            if nodo[1] >= self.x2 and nodo[1] <= self.x1:
                if nodo[2] >= self.y2 and nodo[2] <= self.y1:
                    self.cities.append(nodo)
        
    def get_patch(self):
        return matplotlib.patches.Rectangle((self.x1,self.y1),self.x2-self.x1,self.y2-self.y1,
                    linewidth=self.linewidth,edgecolor=self.edgecolor,facecolor=self.facecolor,alpha=self.alpha)
    
    def get_center(self):
        return ((self.x1+self.x2)/2,(self.y1+self.y2)/2)
    
    def split_X(self,point=None):
        """
        Split por el eje X. Si no recibe una coordenada, lo hace a la mitad.
        """
        if point is None:
            point = self.get_center()
        return region(self.x1,self.y1,point[0],self.y2),region(point[0],self.y1,self.x2,self.y2)
    
    def split_Y(self,point=None):
        """
        Split por el eje Y. Si no recibe una coordenada, lo hace a la mitad.
        """
        if point is None:
            point = self.get_center()
        return Region(self.x1,self.y1,self.x2,point[1]),Region(self.x1,point[1],self.x2,self.y2)
    
    def __repr__(self):
        return '(%.2f,%.2f)-(%.2f,%.2f)'%(self.x1, self.y1, self.x2, self.y2)
    
#Parte 1
def tsp_dac(O):
    #Calculamos maximos y minimos
    x = [node[1] for node in  O.data['nodes']]
    y = [node[2] for node in  O.data['nodes']]    
    x_min,x_max = min(x),max(x)
    y_min,y_max = min(y),max(y)

    #Definimos todo el mapa como una sola region
    mapa = region(x_max,y_max,x_min,y_min)
    mapa.fill_region(O.data['nodes']) #Llenamos la region con las ciudades correspondientes

    #Mostramos la linea que divide el mapa por la mitad
    center = mapa.get_center()

    #Buscamos que punto es el mas cercano al eje horizontal marcado por el punto medio
    dist = float('inf')
    for nodo in mapa.cities:
        new_distance = distance(center,(nodo[1],nodo[2]))
        if new_distance == 0:
            point = nodo
            break
        elif new_distance < dist:
            dist = new_distance
            point = nodo

    reg1,reg2 = mapa.split_X((point[1],point[2]))

    #Llenamos las nuevas regiones con sus respectivas ciudades
    reg1.fill_region(O.data['nodes'])
    reg2.fill_region(O.data['nodes'])
    
    #Escribimos el archibo .tsp
    #Region 1
    f = open("reg1.tsp","w+")
    f.write("NAME: region1 \n")
    f.write("COMMENT: Mitad_derecha \n")
    f.write("TYPE: TSP \n")
    f.write("DIMENSION: " + str(len(reg1.cities)) + "\n") #Tamaño del tour de esta region
    f.write("EDGE_WEIGHT_TYPE: EUC_2D \n") #Puede cambiar
    f.write("NODE_COORD_SECTION \n")
    for city in reg1.cities:
        f.write("" + city[0] + " " + str(int(city[2])) + " " + str(int(city[1])) + "\n")
    f.write("EOF \n")
    f.close()
    #Region2
    f = open("reg2.tsp","w+")
    f.write("NAME: region2 \n")
    f.write("COMMENT: Mitad_izquierda \n")
    f.write("TYPE: TSP \n")
    f.write("DIMENSION: " + str(len(reg2.cities)) + "\n") #Tamaño del tour de esta region
    f.write("EDGE_WEIGHT_TYPE: EUC_2D \n") #Puede cambiar
    f.write("NODE_COORD_SECTION \n")
    for city in reg2.cities:
        f.write("" + city[0] + " " + str(int(city[2])) + " " + str(int(city[1])) + "\n")
    f.write("EOF \n")
    f.close()
    
    print("DONE!")
    variables = [reg1,reg2,point]
    return variables

#Parte 2
def dac_tour(O, variables, nombre1='reg1_solved.cyc', nombre2='reg2_solved.cyc'):
    
    reg1 = variables[0]
    reg2 = variables[1]
    point = variables[2]
    
    #Region 1
    f = open(nombre1,"r")
    if f.mode == 'r':
        contenido = f.readlines()
    f.close()
    indices = []
    for elemento in contenido:
        indices.append(int(elemento))
    reg1.tour = [reg1.cities[i][0] for i in indices]
    
    #Region 2
    f = open(nombre2,"r")
    if f.mode == 'r':
        contenido = f.readlines()
    f.close()
    indices = []
    for elemento in contenido:
        indices.append(int(elemento))
    reg2.tour = [reg2.cities[i][0] for i in indices]
    
    #Juntamos ambos tours a partir de la ciudad que tienen en comun, esta estrategia puede cambiar:
    #Obtenemos el vecino mas lejano que este conectado a la ciudad en comun en ambos tours
    common_city = point

    #Region 1
    idx = reg1.tour.index(common_city[0]) #Esta es la ciudad comun del tour en la region 1
    vecinoA = reg1.tour[idx-1] #Este es el vecino izquierdo en la lista
    vecinoB = reg1.tour[(idx+1)%len(reg1.tour)] #Este es el vecino derecho en la lista
    #Region 2
    idx = reg2.tour.index(common_city[0]) #Esta es la ciudad comun del tour en la region 2
    vecinoC = reg2.tour[idx-1] #Este es el vecino izquierdo en la lista
    vecinoD = reg2.tour[(idx+1)%len(reg1.tour)] #Este es el vecino derecho en la lista

    #Verificamos cuales son las distancias entre los vecinos para juntar los tours
    A = O.data['nodes'][int(vecinoA)-1]
    B = O.data['nodes'][int(vecinoB)-1]
    C = O.data['nodes'][int(vecinoC)-1]
    D = O.data['nodes'][int(vecinoD)-1]

    values = []
    AC = euc_dist(A,C)
    AD = euc_dist(A,D)
    BC = euc_dist(B,C)
    BD = euc_dist(B,D)
    values.append(AC)
    values.append(AD)
    values.append(BC)
    values.append(BD)

    prueba = []
    prueba2 = []

    for idx,element in enumerate(values):
        if element == min(values):
            if idx == 0:
                ##El par es AC
                #print("El par es AC")
                indice = reg1.tour.index(vecinoA)
                for i in range(len(reg1.tour)):
                    prueba.append(reg1.tour[(indice+i)%len(reg1.tour)])
                indice = reg2.tour.index(vecinoD)
                for i in range(len(reg2.tour)):
                    prueba2.append(reg2.tour[(indice+i)%len(reg2.tour)])

            elif idx == 1:
                #El par es AD
                #print("El par es AD")
                indice = reg1.tour.index(vecinoA)
                for i in range(len(reg1.tour)):
                    prueba.append(reg1.tour[(indice+i)%len(reg1.tour)])
                indice = reg2.tour.index(vecinoD)
                for i in range(len(reg2.tour)):
                    prueba2.append(reg2.tour[(indice+i)%len(reg2.tour)])

            elif idx == 2:
                ##El par es BC
                #print("El par es BC")
                indice = reg1.tour.index(vecinoB)
                for i in range(len(reg1.tour)):
                    prueba.append(reg1.tour[(indice+i)%len(reg1.tour)])
                indice = reg2.tour.index(vecinoD)
                for i in range(len(reg2.tour)):
                    prueba2.append(reg2.tour[(indice+i)%len(reg2.tour)])

            elif idx == 3:
                #el par es BD
                #print("El par es BD")
                indice = reg1.tour.index(vecinoA)
                for i in range(len(reg1.tour)):
                    prueba.append(reg1.tour[(indice+i)%len(reg1.tour)])
                indice = reg2.tour.index(vecinoC)
                for i in range(len(reg2.tour)):
                    prueba2.append(reg2.tour[(indice+i)%len(reg2.tour)])

            break


    #Juntamos
    prueba2 = prueba2[::-1]
    prueba2.pop(0)
    new_tour = prueba + prueba2
    
    return new_tour

