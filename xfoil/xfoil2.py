import os
import numpy as np
import subprocess as sp
import time


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

        path = r'C:\Users\marcy\Desktop\TCC\AeroMan\xfoil\xfoil.exe < ' + f'{self.file_coordenadas}.txt'
        path2 = 'C:/Users/marcy/Desktop/TCC/AeroMan/xfoil/xfoil.exe'
        

        
        '''
        os.system(path) # gera os arquivos de saida.
        saida = self.getDados(f"saida_{self.file_coordenadas}.txt")

        '''
        try:
            sp.call([path2,'<', f'{self.file_coordenadas}.txt' ], timeout = 5, shell=True)
            saida = self.getDados(f"saida_{self.file_coordenadas}.txt")
           

        except sp.TimeoutExpired:
            saida = -1
        
        finally:
            print("maxima eficiencia aerodinamica: ", saida)

            os.remove(f'C:/Users/marcy/Desktop/TCC/AeroMan/coord_{self.file_coordenadas}.txt') # arquivo de coordenadas
            os.remove(f'C:/Users/marcy/Desktop/TCC/AeroMan/{self.file_coordenadas}.txt') # arquivo de execução 
            os.remove(f'C:/Users/marcy/Desktop/TCC/AeroMan/saida_{self.file_coordenadas}.txt') # arquivo de saida


        return saida


    def getDados(self, filename):
        #import matplotlib.pyplot as plt 
        #plt.figure()

    
        alpha = []
        cl = []
        cd = []
        l_d = []
        #cm = []
        f = open(filename,'r')
        lines = f.readlines()
        try:
            for row in range(12,len(lines)-1): 
                data = lines[row].split()
                alpha.append(float(data[0]))
                cl.append(float(data[1]))
                cd.append(float(data[2]))
                #cm.append(float(data[3]))

                l_d.append(float(data[1])/float(data[2]))
            f.close()
            
            dado = max(l_d)
        except:
            dado = -1
        
        return dado
        



if __name__ == '__main__':
    name = 'teste_otimizacao'

    Aoa = [0,25,0.5] #[-15,15,0.5]
    c = [2.0, 1.5, 1.25, 1.0]
    Re = 2000000
    
    perfil = airfoil(name, Re, Aoa, iter = 10)
    dado = perfil.simula()
    print('\n\n\n Eficiencia aerodinamcia: ', dado)
    

