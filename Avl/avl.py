#%%
import os 
import sys
import subprocess as sp
import numpy as np
from pathlib import Path

if str(Path(Path().absolute())).split('\\')[-1] == 'AeroMan':
    path = str(Path(Path().absolute())) + r'\xfoil'
else:
    path = str(Path(Path().absolute().parents[0])) + r'\xfoil'

sys.path.insert(1, path)
import xfoil as xf


class Wing:

    def __init__(self, c, b, offset, angle = 3, twist = None):
        '''
        Parametros:
        c : c [c1, c2, c3, c4];
        b : envergadura [b1, b2, b3];
        offset : distancia de recuo do borda de ataque [offset1, offset2, offset3].
        '''
        #vetores
        self.c = c
        self.b = b
        self.offset = offset

        #escalares
        self.angle = angle
        self.S = 2*((c[0]+c[1])*b[0]/2 + (c[1]+c[2])*(b[1]-b[0])/2 + (c[2]+c[3])*(b[2]-b[1])/2) # area projetada a asa
        self.B = 2*max(b) # envergadura total
        self.Ar = self.B**2/self.S # razão de aspecto da asa
        self.Lamb = c[-1]/c[0] # afilamento
        self.Mac = (2/3)*c[0]*(1 + self.Lamb + (self.Lamb)**2)/(1 + self.Lamb) # c media aerodinamca

        

        
    def simulacao(self, velocity = 10, viscosity = 1.5*10**-5 , g = 9.81, rho = 1.225 ):
        '''criando arquivo txt de input do avl'''

        Re = (velocity/viscosity)*np.array(self.c)

        
        # arquivo avl
        with open('asa.avl', 'w') as file:

            file.write(
                "Simple Wing\n" +
                "#Mach\n" +
                "0.0                                 \n" +
                "#iYsym  iZsym  Zsym\n" +
                "0     0     0.0                     \n" +
                "#Sref   Cref   Bref\n" +
                "%f     %f     %f   \n" %(self.S, self.Mac, self.B) +
                "#Xref   Yref   Zref\n" +
                "0.00000     0.00000     0.00000 \n" +
                "#\n" +
                "#CDdp\n" +
                "#arrasto parasita\n" +
                "0.0\n" +
                "#\n" +
                "#====================================================================\n"+
                "SURFACE                      \n" +
                "Main Wing\n" +
                "#Nchord  Cspace   [ Nspan Sspace ]\n" +
                "11        1.0\n" +
                "YDUPLICATE\n" +
                "0.0\n" +
                "SCALE\n" +
                "#Xscale  Yscale  Zscale\n" +
                "1.0  1.0  1.0\n" +
                "TRANSLATE\n" +
                "0.0  0.0  0.0\n" +
                "ANGLE\n" +
                "#twist angle bias for whole surface  \n" +
                "0.000                                \n" +
                "#====================================================================\n" +
                "SECTION                                            \n" + 
                "#Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]       \n" +
                "0.0000    0.0000    0.0000    %f   0.000    8    3 \n" %(self.c[0])+
                "#Camber nao padrao\n" +
                #"AFIL 0.0 1.0\n"+
                "NACA\n"+
                "2024\n"+
                "#====================================================================\n"+
                "SECTION                                     \n" +
                "#Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]\n" +
                "%f    %f    0.0000    %f   0.000    8    3  \n" %( self.offset[0],  self.b[0], self.c[1])+
                #"AFIL 0.0 1.0\n"+
                "NACA\n"+
                "2024\n"+
                "#====================================================================\n"+
                "SECTION                                                     \n" +
                "#Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]   \n" +
                "%f   %f    0.0000    %f   0.000   13    1      \n" %( self.offset[1],  self.b[1], self.c[2])+
                #"AFIL 0.0 1.0\n"+
                "NACA\n"+
                "2024\n"+
                "#====================================================================\n"+
                "SECTION                                      \n" +
                "#Xle Yle Zle   Chord Ainc   [ Nspan Sspace ] \n" +
                "%f    %f    0.0000    %f   0.000   13    1   \n" %( self.offset[2],  self.b[2], self.c[3])+
                #"AFIL 0.0 1.0\n" +
                "NACA\n"+
                "2024\n"
            )

        # arquivo de setup (caso de angulo de ataque preescrito) 
        with open('case.txt', 'w') as file:
            file.write(
                "LOAD asa.avl\n" +
                "OPER\n" +
                "C1\n" +
                "G\n" +
                "%f\n" %(g) +
                "V\n" +
                "%f\n" %(velocity) +
                "D\n" +
                "%f\n" %(rho) +
                "\n" +
                "A\n" +
                "A %f \n" % (self.angle) +
                "X\n"+
                "FT\n"+ # forças totais
                "saida1.txt\n"+
                "FS\n"+ # forças distribuidas
                "saida2.txt\n"+
                "\n"+
                "\n"+
                "QUIT\n"
            )




    def getDados(self):

        # gerando os arquivos
        self.simulacao()

        # rodando a simulação
        execulta = r'C:\Users\marcy\Desktop\TCC\AeroMan\avl\avl.exe<' + 'case.txt'
        os.system(execulta) # gera os arquivos de saida.
        pass






if __name__ == '__main__':
    c = [2.0, 1.5, 1.25, 1.0]
    b = [1.5, 2.25, 3.0]
    offset = [0.0, 0.0, 0.0]
    asa = Wing(c,b,offset)
    asa.getDados()
    print(asa.S)
    print(asa.B)
# %%
