import os
import numpy as np


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


    def simula(self, j):
        name = f"airfoil_geracao_{j}.txt"
        with open(name, 'w') as file:
            file.write(
                
                "LOAD %s \n" %(self.file_coordenadas) +
                "\n"+
                "OPER\n"+
                "VPAR\n"+
                "N %f\n" %(self.ncrit)+
                "\n" +
                "ITER %i\n" %(int(self.iter)) +
                "VISC %f\n" %(self.re) +

                
                "MACH %f\n" %(self.mach) +
                
                "PACC \n"+
                "%s\n"%(f"saida_geracao_{str(j)}.txt")+
                "\n"+
                "ASEQ %f %f %f" %(self.aoa[0],self.aoa[1], self.aoa[2])+
                "\n"+
                
                "\n"+
                "\n"+
                "\n"+
                "QUIT\n"
            )

        execulta = r'C:\Users\marcy\Desktop\TCC\AeroMan\xfoil\xfoil.exe<' + name
        os.system(execulta) # gera os arquivos de saida.

        saida = self.getDados(f"saida_geracao_{str(j)}.txt")
        print("maxima eficiencia aerodinamica: ", saida)

        os.remove(f"saida_geracao_{str(j)}.txt")
        os.remove(name)


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
        



if __name__ == '__main__':
    name = 'teste_otimizacao.txt'

    Aoa = [0,25,0.5] #[-15,15,0.5]
    c = [2.0, 1.5, 1.25, 1.0]
    Re = 2000000
    
    perfil = airfoil(name, Re, Aoa, iter = 10)
    perfil.simula(11)
    

