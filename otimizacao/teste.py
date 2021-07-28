#%%
import sys
from pathlib import Path
import numpy as np
import random
import matplotlib.pyplot as plt
import time

if str(Path(Path().absolute())).split('\\')[-1] == 'AeroMan':
    path_xfoil = str(Path(Path().absolute())) + r'\xfoil'
    path_bezie = str(Path(Path().absolute())) + r'\parametrizacao'
else:
    path_xfoil = str(Path(Path().absolute().parents[0])) + r'\xfoil'
    path_bezie = str(Path(Path().absolute().parents[0])) + r'\parametrizacao'


import class_AG as genetic
sys.path.insert(1, path_bezie)
import bezie_1 as bz
sys.path.insert(1, path_xfoil)
import xfoil2 as xf


def area(point1,point2,point3):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    x3 = point3[0]
    y3 = point3[1]
    aux1 = x2 - x1
    aux2 = y3 - y1
    aux3 = x3 - x1
    aux4 = y2 - y1

    return 0.5*(aux1*aux2 - aux3*aux4)

def valida(A):
    # valido somente para n par
    A = np.array(A)
    n = len(A) #numero de pontos
    m = n//2
    A_up = A[0:m,:]
    A_down = A[m:,:]
    controle = 1
    
    for i in range(m):
        
        if i+1 < n//2:
            print(i, i+1,m-1-i)
            valor = area( A_up[i], A_up[i+1],A_down[m-1-i] )
        else:
            print(i-1, i,m-1-i)
            valor = area( A_up[i-1],A_up[i],A_down[m-1-i] )

        # verificando a area
        if valor<0:
            controle = -1
            break
        

    return controle

count = 0

def fitness(cromossos):
    global count
    count += 1
    name = f"airfoil_geracao_{count}"
    print(cromossos)
    pontosControle = geraPcontrole(cromossos)
    if valida(pontosControle) == 1:
        coordenadas_airfoil = bz.BezierCoord(pontosControle, name)
        coordenadas_airfoil.saveCoord()
        #coordenadas = coordenadas_airfoil._getCoord()


        ##rodarXfoil()
        Re = 3e6
        Aoa = [0, 10, 0.5]

        '''
        # usando a classe xfoi
        naca_teste = xf.Airfoil(name, Re, Aoa, iter = 30)
        fit = naca_teste.fitness
        '''

        #usando a classe xfoil2
        
        perfil = xf.airfoil(name, Re, Aoa, iter = 10)
        
        fit = perfil.simula() 
  
    else: 
        fit = -1
    #plotAirfoil(coordenadas,fit)
#   
    print(fit)
    return fit


A = [ 1.91806421e-02, 4.08603881e-02, 2.83040461e-02, -4.16582287e-02, -2.96215949e-02]

cromossomo_min = list(np.dot(A, 0.8))
cromossomo_max = list(np.dot(A, 1.2))

def geraPcontrole(Cromossomo):

    # NACA 0012 - PONTOS DE CONTROLE
    naca_0012 = [[ 9.71550359e-01,  2.91322978e-03], #<-Borda de fuga
                [ 7.75248631e-01,  Cromossomo[0]  ],
                [ 3.64153844e-01,  Cromossomo[1]  ],
                [ 4.97872062e-02,  Cromossomo[2]  ],
                [ 3.53474364e-07, -1.41520231e-02 ], #<-Borda de ataque
                [ 2.31863952e-01, Cromossomo[3]   ],
                [ 6.35846184e-01, Cromossomo[4]   ],
                [ 9.43100719e-01, -5.82645955e-03]] #<-Borda de fuga

    return naca_0012 



def plotAirfoil(coord_airfooil, fitness):
    plt.ion()
    plt.title(f'Fitness = {fitness}')
    plt.plot(coord_airfooil[:,0], coord_airfooil[:,1])
    plt.pause(0.01)
    plt.show()
    plt.cla()

#Teste

validacao = genetic.Genetic_simple(ngen = 10, npop = 10, pmut = 0.2, best = 5, pcross = 0.5, function = fitness, lim_up= cromossomo_max, lim_down = cromossomo_min )
pop = validacao.run()
    # cl max 
    # menor arrasto para aoa fixo
    # l/d