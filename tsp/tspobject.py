from os import path, listdir
import tspparser
import metrics

class TSPObject:
    def __init__(self,tsp_file,metricfunc):
        self.metricfunc = metricfunc
        self.data = tspparser.parse(tsp_file)
        self.V = [x[0] for x in self.data['nodes']]
        self.V_idx = {v:idx for idx,v in enumerate(self.V) }
        self.points = [(x[1],x[2]) for x in self.data['nodes']]        

    def neighbors(self,v):
        v_idx = self.V_idx[v]
        for u in self.V:
            if u == v:
                continue
            u_idx = self.V_idx[u]
            yield (u, self.metricfunc(self.points[v_idx],self.points[u_idx]))

    def evaluate_tour(self,tour):
        n = len(tour)
        distance = 0
        for i in range(n):
            v_idx = self.V_idx[tour[i]]
            u_idx = self.V_idx[tour[(i+1)%n]]
            distance += self.metricfunc(self.points[v_idx],self.points[u_idx])
        return distance

    def tour_coordinates(self,tour):
        n = len(tour)
        coords = []
        for v in tour+[tour[0]]:
            coords.append(self.points[self.V_idx[v]])
        x = [c[0] for c in coords]
        y = [c[1] for c in coords]
        return x,y
        
    def distance(self,u,v):
        u_idx = self.V_idx[u]
        v_idx = self.V_idx[v]
        return self.metricfunc(self.points[v_idx],self.points[u_idx])

if __name__ == '__main__':
    test_file = path.join('..','benchmarks','dj38.tsp')
    O = TSPObject(test_file,metrics.euc_dist)
    #print(list(O.neighbors('1')))
    print(O.distance('1','2'))
    print(O.distance('2','3'))
    print(O.distance('3','1'))
    print(O.evaluate_tour(['1','2','3']))