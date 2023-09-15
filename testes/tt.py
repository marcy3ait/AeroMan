
import subprocess as sp
import threading
from multiprocessing import Process 
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from pathlib import Path

if str(Path(Path().absolute())).split('\\')[-1] == 'AeroMan':
    path_xfoil = str(Path(Path().absolute())) + r'\xfoil'
else:
    path_xfoil = str(Path(Path().absolute().parents[0])) + r'\xfoil'

sys.path.insert(1, path_xfoil)
print(path_xfoil)
import xfoil2 as xfoil

def naca00xx(t,n):
    # naca 0012
    # t = 12  # dois últimos digitos do naca (série 4 digitos)
    # n = 30  # número de pontos

    # coeficientes da equação
    a0 = +0.2969
    a1 = -0.1260
    a2 = -0.3516
    a3 = +0.2843
    a4 = -0.1015 # bordo de fuga espesso
    a4 = -0.1036 # bordo de fuga colapsado

    coord = np.zeros((n,2))

    # concentra pontos nas extremidades usando uma função cosseno
    theta  = np.linspace(0.0,2*np.pi,n)
    coord[:,0] = np.cos(theta)*0.5+0.5

    # função sinal: indentifica se estamos no intradorso ou extradorso
    side = np.where(theta>np.pi,-1,1)

    t = t/100.0
    coord[:,1] = -t/0.2*(a0*np.sqrt(coord[:,0]) + a1*coord[:,0] + a2*coord[:,0]**2 + a3*coord[:,0]**3 + a4*coord[:,0]**4)
    coord[:,1] = side*coord[:,1]

    return coord


def save(name, data):

    with open(path_xfoil+'\\'+name+'.dat', 'a') as file:
        for i in data:
            print(i)
            file.write(str(i[0])+'   '+str(i[1])+'\n')

def alpha(dataX, dataY):

    dx = dataX[-1] - dataX[0]
    dy = dataY[-1] - dataY[0]

    return float(dy/dx)

def parabola(dataX, dataY):
    # retona CL1 CD1  CL2 CD2  CL3 CD3
    Cd = np.array(dataX)
    Cl = np.array(dataY)

    Cd2 = float(min(Cd))
    Cl2 = float(Cl[np.where(Cd == min(Cd))])

    Cd1 = float(Cd[np.where(min(Cl))])
    Cl1 = float(min(Cl))

    Cd3 = float(Cd[np.where(-1.*min(Cl))])
    Cl3 = float(-1.*min(Cl))

    return np.array([Cl1, Cd1, Cl2, Cd2, Cl3, Cd3])


if __name__ == '__main__':
    
    name1 = 'naca0012'
    name2 = 'naca0008'
    if os.path.exists(path_xfoil +'\\'+f'{name1}.dat'):
        os.remove(path_xfoil +'\\'+f'{name1}.dat') # arquivo de saida
    if os.path.exists(path_xfoil +'\\'+f'{name2}.dat'):
        os.remove(path_xfoil +'\\'+f'{name2}.dat') # arquivo de saida

    naca0012 = naca00xx(12,50)
    naca0008 = naca00xx(8,50)
    save('naca0012',naca0012)
    save('naca0008',naca0008)
    Aoa = [-20,20,2]
    c = [2.0, 1.5, 1.25, 1.0]
    Re = 6e6
    perfil1 = xfoil.airfoil(name1, Re, Aoa, iter = 30)
    perfil2 = xfoil.airfoil(name2, Re, Aoa, iter = 30)
    aoa1,cl1,cd1 = perfil1.getDados()
    aoa2,cl2,cd2 = perfil2.getDados()

    print('\n aoa: ', aoa1)
    print('\n aoa: ', aoa2)
    print('\n cl: ', cl1)
    print('\n cl: ', cl2)
    print('\n cd: ', cd1)
    print('\n cd: ', cd2)
    a = parabola(cd1,cl1)
    print('\n teste: ', a)
    

    
    plt.figure(1)
    plt.plot(aoa1,cl1,'r')
    plt.plot(aoa2,cl2,'b')

    plt.figure(2)

    plt.plot(cd1,cl1,'r')
    plt.plot(cd2,cl2,'b')
    plt.plot(a[1],a[0],'xk')
    plt.plot(a[3],a[2],'xk')
    plt.plot(a[5],a[4],'xk')
    #deg = 10
    #z = np.polyfit(cl1, cd1, deg)
    #y2 = np.poly1d(z)
    #x = np.linspace(min(cl1),max(cl1),100)
    #plt.plot(y2(x),x,  "-")

    plt.show()




    
