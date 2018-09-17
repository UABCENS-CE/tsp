from math import radians, cos, sin, asin, acos, atan, atan2, sqrt,pi

def euc_dist(node1,node2): 
#the cost of travel between cities is specified by the Eulidean distance 
#rounded to the nearest whole number (the TSPLIB EUC_2D-norm).
    x1,y1 = node1[1],node1[2]
    x2,y2 = node2[1],node2[2]
    #return int(((y2-y1)**2+(x2-x1)**2)**.5)
    return ((y2-y1)**2+(x2-x1)**2)**.5


def geo_norm_waterloo(node1,node2): 
#http://www.math.uwaterloo.ca/tsp/world/geom.html
    lat1,lon1 = node1[1],node1[2]
    lat2,lon2 = node2[1],node2[2]
    lat1,lat2 = pi*lat1/180, pi*lat2/180
    lon1,lon2 = pi*lon1/180,pi*lon2/180
    q1 = cos(lat2)*sin(lon1-lon2)
    q3 = sin((lon1-lon2)/2)
    q4 = cos((lon1-lon2)/2)
    q2 = sin(lat1+lat2)*q3*q3-sin(lat1-lat2)*q4*q4
    q5 = cos(lat1-lat2)*q4*q4-cos(lat1+lat2)*q3*q3
    return int(6378.388*atan2(sqrt(q1*q1+q2*q2),q5)+1)
    #return 6378.388*atan2(sqrt(q1*q1+q2*q2),q5)+1

    
def _radian_feo(x):
    PI= 3.141592
    _deg = int(x)
    _min = x-_deg
    return PI*(_deg+5.0*_min/3.0)/180.0


def geo_norm_heidelberg(node1,node2):
#https://wwwproxy.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/TSPFAQ.html
    lat1,lon1 = node1[1],node1[2]
    lat2,lon2 = node2[1],node2[2]
    lon1, lat1, lon2, lat2 = map(_radian_feo, [lon1, lat1, lon2, lat2])
    RRR = 6378.388
    q1 = cos(lon1-lon2)
    q2 = cos(lat1-lat2)
    q3 = cos(lat1+lat2)
    return int(RRR*acos(.5*((1.0+q1)*q2-(1.0-q1)*q3))+1.0)

def haversine(node1,node2):
#https://en.wikipedia.org/wiki/Haversine_formula
#https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    lat1,lon1 = node1[1],node1[2]
    lat2,lon2 = node2[1],node2[2]
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6378.388 # Radius of earth in kilometers: 6371. Use 3956 for miles
    #return round(c*r)
    return c*r


if __name__=='__main__':
    a = ['A',3,3]
    b = ['B',7,6]
    print(euc_dist(a,b))
    print(haversine(a,b))