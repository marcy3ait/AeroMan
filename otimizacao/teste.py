#%%
import sys
from pathlib import Path
import numpy as np
import random
import matplotlib.pyplot as plt


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
import xfoil as xf



def fitness(cromossos):
    name = f"airfoil_geracao"
    
    pontosControle = geraPcontrole(cromossos)

    coordenadas_airfoil = bz.BezierCoord(pontosControle, name)
    coordenadas_airfoil.saveCoord()
    coordenadas = coordenadas_airfoil._getCoord()


    ##rodarXfoil()
    Re = 3e6
    Aoa = [0, 10, 0.5]

    naca_teste = xf.Airfoil(name, Re, Aoa, iter = 30)
    fit = naca_teste.fitness

    plotAirfoil(coordenadas,fit)
#
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
                [ 3.53474364e-07, -1.41520231e-02 ],#<-Borda de ataque
                [ 2.31863952e-01, Cromossomo[3]   ],
                [ 6.35846184e-01, Cromossomo[4]   ],
                [ 9.43100719e-01, -5.82645955e-03]]#<-Borda de fuga

    return naca_0012 



def plotAirfoil(coord_airfooil, fitness):
    plt.ion()
    plt.title(f'Fitness = {fitness}')
    plt.plot(coord_airfooil[:,0], coord_airfooil[:,1])
    plt.pause(0.01)
    plt.show()
    plt.cla()

#Teste

validacao = genetic.Genetic_simple(ngen = 20, npop = 300, pmut = 0.2, best = 50, pcross = 0.5, function = fitness, lim_up= cromossomo_max, lim_down = cromossomo_min )
pop = validacao.run()
    # cl max 
    # menor arrasto para aoa fixo
    # l/d