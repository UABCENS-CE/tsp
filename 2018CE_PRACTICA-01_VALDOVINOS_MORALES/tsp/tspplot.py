import matplotlib
import matplotlib.pyplot as plt

def plot_tsp(tspobject,tour=[],figsize=(4,4)): 
    x = [point[0] for point in  tspobject.points]
    y = [point[1] for point in  tspobject.points]
    fig,ax = plt.subplots(figsize=figsize)
    plt.scatter(x,y,color='gray')        
    if len(tour)==0:
        plt.show()
        return
    distance = tspobject.evaluate_tour(tour)
    plt.suptitle('Distance=%.3f (%s)'%(distance,tspobject.metricfunc.__name__))
    x,y = tspobject.tour_coordinates(tour)
    plt.plot(x,y,'r-')
    plt.show()

def plot_tsp_region(tspobject,tours=[],regions=[],figsize=(4,4)):
    x = [point[0] for point in  tspobject.points]
    y = [point[1] for point in  tspobject.points]
    fig,ax = plt.subplots(figsize=figsize)
    plt.scatter(x,y,color='gray')
    for tour in tours:
        x,y = tspobject.tour_coordinates(tour)
        plt.plot(x,y,'r-')
    for region in regions:
        for region in regions:
            ax.add_patch(region.get_patch())     
    plt.show()

if __name__ == '__main__':
    from os import path
    from tspobject import TSPObject
    import metrics
    from region import Region

    test_file = path.join('..','benchmarks','dj38.tsp')
    O = TSPObject(test_file,metrics.euc_dist)
    ###Normal plot
    #plot_tsp(O,tour=['1','2','3'])
    ####Regions
    R = Region.whole_region(O)
    regions = [R, *R.split_Y()]
    tours = [['1','2','3'],['36','37','38']]
    plot_tsp_region(O,tours,regions)