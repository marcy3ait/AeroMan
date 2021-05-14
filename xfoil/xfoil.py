#%%
import os 
import sys
import subprocess as sp
import time
import numpy as np


path = os.path.dirname(os.path.realpath(__file__))
if sys.platform == 'win32':
    path = os.path.join(path,'xfoil.exe')
elif sys.platform == 'linux2':
    path = ['xfoil'] # valido para variavel de ambiente


class Xfoil:

    def __init__(self, path, plotter = False):
        ''' star conection from xfoil '''
        self.xfsim = sp.Popen(path, stdin = sp.PIPE, stderr = sp.PIPE, stdout = sp.PIPE, shell= False)


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

    
    
class Airfoil:
    def __init__(self, airfoil, re, aoa,  iter=10, mach = None,  ncrit = 9.0):
        self.airfoil = airfoil
        self.re = re
        self.aoa = aoa
        self. iter = iter
        self.mach = mach
        self.ncrit = ncrit

        self.fitness = self.analises()
        
    def analises(self ):
        
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
        # loading self.airfoil 
        if self.airfoil.split()[0].upper() != 'NACA':
            name = '_'.join(self.airfoil.split('.')[:-1])+'.log'
            xfoil.write('LOAD '+ self.airfoil)
            xfoil.write(self.airfoil)  
                
        else:
            name = '_'.join(self.airfoil.split())+'.log'
            xfoil.write(self.airfoil)  

        xfoil.write('OPER')

        xfoil.write('VPAR')
        xfoil.write('N ' + str(self.ncrit))
        xfoil.write()
        
        xfoil.write('ITER {:0.0f}'.format(self.iter))

        xfoil.write('VISC ' + str(self.re))

        if self.mach:
            xfoil.write('MACH {:.3f}'.format(self.mach))
        
    
        try:
            os.remove(name)
        except:
            pass
        
        xfoil.write('PACC')
        xfoil.write(name)

        xfoil.write()
        xfoil.write('ASEQ {:0.2f} {:0.2f} {:0.2f}'.format(self.aoa[0], self.aoa[1], self.aoa[2]))
        xfoil.write()
        xfoil.terminate()

        return self.getPolar(name)


    def getPolar(self, filename):
                #import matplotlib.pyplot as plt 
            #plt.figure()

        
            alpha = []
            cl = []
            cd = []
            l_d = []
            #cm = []
            f = open(filename,'r')
            lines = f.readlines()
            for row in range(12,len(lines)-1): 
                data = lines[row].split()
                alpha.append(float(data[0]))
                cl.append(float(data[1]))
                cd.append(float(data[2]))
                #cm.append(float(data[3]))

                l_d.append(float(data[1])/float(data[2]))
            f.close()
            #print(np.array(alpha))
            #print(np.array(l_d))
            #plt.plot(np.array(alpha),np.array(l_d))
            #plt.show()

            
            dado = max(l_d)
            
            return dado


    
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

    name = 'teste_otimizacao.txt'
    re =  3.e6
    Aoa = [0,15,0.5] #[-15,15,0.5]
    re = 3.e6

    naca_teste = Airfoil(name, re, Aoa, iter = 30)
    print(naca_teste.fitness)

# %%
