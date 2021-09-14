import os
import numpy as np
import subprocess as sp
import time
import sys

from pathlib import Path

if str(Path(Path().absolute())).split('\\')[-1] == 'AeroMan':
    path = str(Path(Path().absolute())) + r'\xfoil'
    sys.path.insert(1, path)
else:
    path = str(Path(Path().absolute()))


class airfoil:

    def __init__(self, file_coordenadas, re, aoa, iter = 10, mach = 0, ncrit = 9.0):
        
        '''
        Parametros

        airfoil: Arquivo do aerofolio ou naca 4 ou 5 digitos
        re: Numero de Reynolds
        aoa: Angulo de ataque [start, stop, step]
        iter: Limite de iterações para solução viscosa
        mach: Numero de mach
        ncrit: Parametro de convergencia
        '''

        self.file_coordenadas = file_coordenadas
        self.re = re
        self.aoa = aoa
        self.iter = iter
        self.mach = mach
        self.ncrit = ncrit 



    def simula(self):
        
        
        with open(f'{self.file_coordenadas}.txt', 'w') as file:
            file.write(
                #"PLOP\nG\n\n"+
                "LOAD %s \n" %(f'coord_{self.file_coordenadas}.txt') +
                "\n"+
                "PANE 100\n"+
                "OPER\n"+
                "VPAR\n"+
                "N %f\n" %(self.ncrit)+
                "\n" +
                "ITER %i\n" %(int(self.iter)) +
                "VISC %f\n" %(self.re) +

                
                "MACH %f\n" %(self.mach) +
                
                "PACC \n"+
                "%s\n"%(f"saida_{self.file_coordenadas}.txt")+
                "\n"+
                "ASEQ %f %f %f" %(self.aoa[0],self.aoa[1], self.aoa[2])+
                "\n"+
                
                "\n"+
                "\n"+
                "\n"+
                "QUIT\n"
            )


     


    def getDados(self):
        #import matplotlib.pyplot as plt 
        #plt.figure()
        self.simula()

        wd = os.getcwd()
        os.chdir("/")

       
        p = sp.Popen(f'xfoil.exe < {self.file_coordenadas}.txt',  shell=True, cwd = path)

        try:
            p.wait(20)
        except sp.TimeoutExpired:
            dev_null = open(os.devnull, 'w')
            command = ['TASKKILL', '/F', '/T', '/PID', str(p.pid)]
            proc = sp.Popen(command, stdin=dev_null, stdout=sys.stdout, stderr=sys.stderr)
            proc.wait(5)
        alpha = []
        cl = []
        cd = []
        l_d = []
        try:
            with open(path +'\\'+f'saida_{self.file_coordenadas}.txt','r') as file:
                lines = file.readlines()
                print(lines)
                for row in range(12,len(lines)-1): 
                    data = lines[row].split()
                    
                    alpha.append(float(data[0]))
                    cl.append(float(data[1]))
                    cd.append(float(data[2]))
                    #cm.append(float(data[3]))

                    l_d.append(float(data[1])/float(data[2]))
                
                dado = max(l_d)
        except:
            dado = -1
        

        if os.path.exists(path +'\\' + f'coord_{self.file_coordenadas}.txt'):
            os.remove(path +'\\' + f'coord_{self.file_coordenadas}.txt')
        
        if os.path.exists(path +'\\' + f'{self.file_coordenadas}.txt'):
            os.remove(path +'\\' + f'{self.file_coordenadas}.txt') # arquivo de execução

        if os.path.exists(path +'\\'+f'saida_{self.file_coordenadas}.txt'):
             os.remove(path +'\\'+f'saida_{self.file_coordenadas}.txt') # arquivo de saida
        
        
        return dado
        



if __name__ == '__main__':
    name = 'teste'

    Aoa = [0,25,5] #[-15,15,0.5]
    c = [2.0, 1.5, 1.25, 1.0]
    Re = 6e6
    perfil = airfoil(name, Re, Aoa, iter = 10)
    dado = perfil.getDados()
    print('\n\n\n Eficiencia aerodinamica: ', dado)
    

