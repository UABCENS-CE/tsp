import matplotlib
import matplotlib.pyplot as plt

class Region:
    def __init__(self,x1,y1,x2,y2,
                linewidth=1,edgecolor='g',facecolor='none',alpha=.4):        
        self.x1, self.y1, self.x2, self.y2 = x1,y1,x2,y2        
        #Detalles estéticos
        self.linewidth=linewidth
        self.edgecolor=edgecolor
        self.facecolor=facecolor
        self.alpha=alpha
            

    def get_patch(self):
        return matplotlib.patches.Rectangle((self.x1,self.y1),self.x2-self.x1,self.y2-self.y1,
                    linewidth=self.linewidth,edgecolor=self.edgecolor,facecolor=self.facecolor,alpha=self.alpha)
    

    def __repr__(self):
        return '(%.2f,%.2f)-(%.2f,%.2f)'%(self.x1, self.y1, self.x2, self.y2)
    

    def get_center(self):
        return ((self.x1+self.x2)/2,(self.y1+self.y2)/2)
    

    def whole_region(tspobject):
        x = [point[0] for point in  tspobject.points]
        y = [point[1] for point in  tspobject.points]    
        x_min,x_max = min(x),max(x)
        y_min,y_max = min(y),max(y)
        return Region(x_min,y_min,x_max,y_max)


    def split_X(self,point=None):
        """
        Split por el eje X. Si no recibe una coordenada, lo hace a la mitad.
        """
        if point is None:
            point = self.get_center()
        return Region(self.x1,self.y1,point[0],self.y2),Region(point[0],self.y1,self.x2,self.y2)
    
    
    def split_Y(self,point=None):
        """
        Split por el eje Y. Si no recibe una coordenada, lo hace a la mitad.
        """
        if point is None:
            point = self.get_center()
        return Region(self.x1,self.y1,self.x2,point[1]),Region(self.x1,point[1],self.x2,self.y2)

if __name__ == '__main__':
    from os import path
    from tspobject import TSPObject
    import metrics

    test_file = path.join('..','benchmarks','dj38.tsp')
    O = TSPObject(test_file,metrics.euc_dist)
    R = Region.whole_region(O)
    print(R)