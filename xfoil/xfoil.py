import os 
import sys
import subprocess as sp
import time


path = os.path.dirname(os.path.realpath(__file__))
if sys.platform == 'win32':
    path = os.path.join(path,'xfoil.exe')
elif sys.platform == 'linux2':
    path = ['xfoil'] # valido para variavel de ambiente


class Xfoil:

    def __init__(self, path, plotter = False):
        ''' star conection from xfoil '''
        self.xfsim = sp.Popen(path, stdin = sp.PIPE, stderr = sp.PIPE, stdout = sp.PIPE, shell= False)
        self._stdin = self.xfsim.stdin
        self._stdout = self.xfsim.stdout
        self._stderr = self.xfsim.stderr # saida de erro

        if plotter == False: # dasativando o modo ploter do xfoil
            self.write('PLOP\nG\n')

    def write(self, comando = '', autoline = True):
        ''' insert comand xfoil '''

        n = '\n' if autoline else ''
        entrada = comando + n
        self._stdin.write(entrada.encode('ascii'))
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
 

    

if __name__ == '__main__':
    import numpy as np
    name = 'naca 2024'
    
    Re = 1.e6
    Aoa = [-10,20,1]
    analises(name, Re, Aoa, iter= 100)
    '''
    start2 = time.time()
    for i in Re:
        start = time.time()
        alpha,cl,cd,cm = analises(name, i, Aoa, iter = 10) # so retorna os dados que convergem 
        
        finish = time.time()
        print('Cl: ',cl)
        print('AoA: ', alpha)
        print('Time: ', finish-start)
        
    print('time final: ',time.time()-start2)
    '''