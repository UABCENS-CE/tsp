from os import path, listdir

def info(tsplib_file):
    if not path.exists(tsplib_file):
        raise FileNotFoundError('File not found.')
    properties = {}        
    with open(tsplib_file,'r') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                key = line.split(':')[0].strip()
                if key in properties:
                    properties[key].append(line.split(':')[1].strip())
                else:
                    properties[key]= [line.split(':')[1].strip()]
                continue                        
    properties = {k:' '.join(v) for k,v in properties.items()}
    return properties


def parse(tsplib_file):
    if not path.exists(tsplib_file):
        raise FileNotFoundError('File not found.')
    properties = info(tsplib_file)
    
    if properties['EDGE_WEIGHT_TYPE'] not in ['EUC_2D','GEO']:
        raise NotImplementedError('Parsing not implemented for EDGE_WEIGHT_TYPE other than "EUC_2D" and "GEO"')       
    #Leer NODE_COORD_SECTION
    nodes = []
    with open(tsplib_file,'r') as f:
        for line in f:
            line = line.strip()
            if line in ['','NODE_COORD_SECTION','EOF']:
                continue
            if ':' in line:
                continue
            node_info = line.split()            
            nodes.append([node_info[0], float(node_info[2]),float(node_info[1])]) #NAME, X, Y
    #Checar si hay solucion optima en la carpeta
    tour = []
    opt_file = tsplib_file.replace('.tsp','.opt.tour')
    if path.exists(opt_file):            
        #Leer solucion optima    
        with open(opt_file,'r') as f:
            for line in f:
                line = line.strip()
                if ':' in line:
                    continue
                if line in ['','TOUR_SECTION','EOF','-1']:
                    continue            
                tour+=line.split()                
    return {'nodes':nodes,
            'properties':properties,
            'optimal_tour':tour}

if __name__ == '__main__':
    test_file = path.join('..','benchmarks','berlin52.tsp')    
    data = parse(test_file)
    print(data)