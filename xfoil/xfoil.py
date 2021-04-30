import os 
import sys
import subprocess as sp
import time
import numpy as np


path = os.path.dirname(os.path.realpath(__file__))
print(path)
if sys.platform == 'win32':
    path = os.path.join(path,'xfoil.exe')
elif sys.platform == 'linux2':
    path = ['xfoil'] # valido para variavel de ambiente


class Xfoil:

    def __init__(self, path, plotter = False):
        ''' star conection from xfoil '''
        self.xfsim = sp.Popen(path, stdin = sp.PIPE, stderr = sp.PIPE, stdout = sp.PIPE, shell= False)
        #self._stdin = self.xfsim.stdin
        #self._stdout = self.xfsim.stdout
        #self._stderr = self.xfsim.stderr # saida de erro

        if plotter == False: # dasativando o modo ploter do xfoil
            self.write('PLOP\nG\n')

    def write(self, comando = '', autoline = True):
        ''' insert comand xfoil '''

        n = '\n' if autoline else ''
        entrada = comando + n
        self.xfsim.stdin.write(entrada.encode('ascii'))
        #print(self.xfsim.returncode)
        
    def terminate(self):
        ''' kill process '''

        self.write()
        self.write()
        self.write()
        self.write('QUIT')
        self.xfsim.stdout.close()
        self.xfsim.stdin.close()
        self.xfsim.wait()
        self._close() # finalizando o processo 
    
    def _close(self):
        
        return self.xfsim.kill()

    
    

def analises(airfoil, re, aoa,  iter=10, mach = None,  ncrit = 9.0):
    
    '''
    Parametros

    airfoil: Arquivo do aerofolio ou naca 4 ou 5 digitos
    re: Numero de Reynolds
    aoa: Angulo de ataque [start, stop, step]
    iter: Limite de iterações para solução viscosa
    mach: Numero de mach
    ncrit: Parametro de convergencia

    '''

    
    xfoil = Xfoil(path)
    # loading airfoil 
    if airfoil.split()[0].upper() != 'NACA':
        name = '_'.join(airfoil.split('.')[:-1])+'.log'
        xfoil.write('LOAD '+ airfoil)
        xfoil.write(airfoil)  
            
    else:
        name = '_'.join(airfoil.split())+'.log'
        xfoil.write(airfoil)  

    xfoil.write('OPER')

    xfoil.write('VPAR')
    xfoil.write('N ' + str(ncrit))
    xfoil.write()
    
    xfoil.write('ITER {:0.0f}'.format(iter))

    xfoil.write('VISC ' + str(re))

    if mach:
        xfoil.write('MACH {:.3f}'.format(mach))
    
   
    try:
        os.remove(name)
    except:
        pass
    
    xfoil.write('PACC')
    xfoil.write(name)

    xfoil.write()
    xfoil.write('ASEQ {:0.2f} {:0.2f} {:0.2f}'.format(aoa[0],aoa[1],aoa[2]))
    xfoil.write()
    xfoil.terminate()

    return getPolar(name)


def getPolar(filename):
    try:
        alpha = []
        cl = []
        cd = []
        cm = []
        f = open(filename,'r')
        lines = f.readlines()
        for row in range(12,len(lines)): 
            data = lines[row].split()
            alpha.append(float(data[0]))
            cl.append(float(data[1]))
            cd.append(float(data[2]))
            cm.append(float(data[3]))
        f.close()
        return alpha,cl,cd,cm
    except:
        print('Não houve convergencia dos valores')
        return None, None, None, None


 
def getInterpola(filename):
    cl = []
    cd = []
    f = open(filename,'r')
    lines = f.readlines()
    for row in range(12,len(lines)): 
        data = lines[row].split()
        cl.append(float(data[1]))
        cd.append(float(data[2]))
    f.close()

    cl = np.array(cl)
    cd = np.array(cd)

    return cl, cd

    

if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    #name = 'teste_otimizacao.txt'
    name = 'polar0.dat'
    re =  lambda C: C*10/(1.5*10**-5)
    Aoa = [-25,25,2] #[-15,15,0.5]
    c = [2.0, 1.5, 1.25, 1.0]
    fig1,ax1 = plt.subplots()
    fig2,ax2 = plt.subplots()
    for corda in c:
        Re = re(corda)
        alpha,cl,cd,cm = analises(name, Re, Aoa, iter = 10)
        print('Cl', cl)
        print('Cd', cd)
        ax1.plot(cd,cl,label = 'Re =  {:0.3f}'.format(Re))

        ax2.plot(alpha,cl,label =  'Re =  {:0.3f}'.format(Re))

    # interpolacao
    def func(x, a, b, c):
        return a*x**2+b*x+c

    
    popt, pcov = curve_fit(func, cl , cd)
    cll = np.lispace(min(cl),max(cl),50)
    ax1.plot(cll, func(cll,*popt),'--b', label = 'interpola')

    
    ax1.grid()
    ax1.legend()
    ax2.grid()
    ax2.legend()
    plt.show()




    '''
    Re = [1.e5, 1.e6]
    Aoa = [-10,20,1]
   
    start2 = time.time()
    for i in Re:
        start = time.time()
        alpha,cl,cd,cm = analises(name, i, Aoa, iter = 10) # so retorna os dados que convergem 
        
        finish = time.time()
        print('Reynolds: ',i)
        print('Cl: ',cl)
        print('AoA: ', alpha)
        print('Time: ', finish-start)
        
    print('time final: ',time.time()-start2)
    '''
    
  