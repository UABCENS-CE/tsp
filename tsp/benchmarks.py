import os
from os import path, listdir
from bs4 import BeautifulSoup
import requests
import gzip,tarfile
from math import sin, cos, radians
import time
import tspparser


def download_tsp_heidelberg(all_tsp_url=r'https://wwwproxy.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/tsp/ALL_tsp.tar.gz',
    output_folder=r'benchmark_symmetric'):
    if not path.exists(output_folder):
        os.mkdir(output_folder)
    #Conectarse a la web y descargar el comprimido en RAM
    r = requests.get(url=all_tsp_url)
    #Copiar el archivo de RAM a un archivo local
    with open(path.join(output_folder,'all.gz'),'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)
    #Descomprimir archivo local
    with tarfile.open(name=path.join(output_folder,'all.gz'), mode='r|gz') as tarf:
        for m in tarf:
            f_gz = tarf.extractfile(m)        
            with open(path.join(output_folder,m.name),'wb') as f:
                f.write(f_gz.read())    
    os.remove(path.join(output_folder,'all.gz'))    
    time.sleep(.5)
    #Descomprimir cada archivo comprimido que se descomprimio
    for gz in sorted([x for x in listdir(output_folder) if x.endswith('.gz')]):
        print(path.join(output_folder,gz))
        with gzip.open(path.join(output_folder,gz),'r') as input_file:
            with open(path.join(output_folder,gz.replace('.gz','')),'wb') as output_file:
                output_file.write(input_file.read())
        os.remove(path.join(output_folder,gz))

def download_tsp_waterloo(all_tsp_url=r'http://www.math.uwaterloo.ca/tsp/world/countries.html',
    output_folder=r'benchmark_countries'):
    if not path.exists(output_folder):
        os.mkdir(output_folder)
    #Conectarse a la web y descargar el comprimido en RAM
    page_response = requests.get(url=all_tsp_url)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    tsp_links = [a for a in page_content.find_all('a') if a.text.startswith('Data')]
    for a in tsp_links:
        _tsp ='/'.join(all_tsp_url.split('/')[:-1])+'/'+a.attrs['href']     
        new_file = path.join(output_folder,a.attrs['href'])
        if path.exists(new_file):
            continue
        print(_tsp)
        r = requests.get(_tsp)    
        with open(new_file,'wb') as f:
            f.write(r.content)    
        #Sleep para que no crean que es un ataque 
        time.sleep(1)
        
###Generar benchmarks basados en polígonos regulares
def _filename(file):
    return path.splitext(path.basename(file))[0]


#Concorde resuelve de 11 para arriba
def polygon_to_TSPLIB(point_list,output_file):
    coords = '\n'.join([' '.join(map(str,[idx+1, p[0],p[1]])) for idx,p in enumerate(point_list)])
    file_str = '''NAME : %s
COMMENT : Polygon
TYPE : TSP
DIMENSION : %d
EDGE_WEIGHT_TYPE : EUC_2D
NODE_COORD_SECTION
%s
EOF
'''%(_filename(output_file),len(point_list),coords)    
    with open(output_file,'w') as f:
        f.write(file_str)    

        
def regular_polygon(edges,radius,center=(0,0)):
    theta = radians(360/edges)
    return [(radius*cos(i*theta)+center[0], radius*sin(i*theta)+center[1]) for i in range(edges)]    

def benchmark_folder_info(benchmark_path):
    import pandas as pd

    if not path.exists(benchmark_path):
        raise FileNotFoundError('Folder not found.')
    files = sorted([f for f in listdir(benchmark_path) if f.endswith('.tsp')])
    P = []
    for f in files:
        P.append(tspparser.info(path.join(benchmark_path,f)))
    df = pd.DataFrame(P)
    df.set_index('NAME',inplace=True)
    return df
    

if __name__=='__main__':
    test_path = path.join('..','benchmarks') 
    print(benchmark_folder_info(test_path))