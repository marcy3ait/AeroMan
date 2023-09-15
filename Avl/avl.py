#%%
import os 
import sys
import subprocess as sp
import numpy as np
from itertools import islice
from pathlib import Path

import signal

from numpy.core.function_base import _linspace_dispatcher


if str(Path(Path().absolute())).split('\\')[-1] == 'AeroMan':
    path = str(Path(Path().absolute())) + r'\avl'
    sys.path.insert(1, path)
else:
    path = str(Path(Path().absolute()))



class Wing:
    count = 0

    def __init__(self, c, b, offset, twist, t, claf = 1, angle = 3):#, lh, c_htail, envH, offset_htail, c_vtail, envV, offset_vtail, angle = 3, twist = None):

        '''
        Parametros:
        
        ASA
        c : cordas da asa [c1, c2, c3];
        b : envergadura [b1, b2];
        offset : distancia de recuo do borda de ataque [offset1, offset2, offset3].
        t: espessura.
        CLAf : parametro de correção da curva cl(a) claf = dcl_da/2pi

        lh: distancia ate o borda de ataque das empenagens
        c_htail: cordas da empenagem horizontal [cr, ct]
        envH: semi-enrgadura da empenagem horizontal
        offset_Htail: offset da empenagem horizontal
        
        c_vtail: cordas da empenagem vertical [cr, ct]
        envV: semi-enrgadura da empenagem vertical
        offset_vtail: offset da empenagem vertical
        
        '''
        
        self.id = Wing.count
        Wing.count += 1 
        Espessura = [10,11,12,13,15,18,21,24]
        self.airfoil = Espessura[int(t)]

        #ASA
        ##vetores
        self.c = c
        self.b = b
        self.offset = offset
        self.twist = twist

       


        ##escalares
        self.angle = angle
        self.S = 2*((c[0]+c[1])*b[0]/2 + (c[1]+c[2])*(b[1])/2) # area projetada a asa
        self.B = 2*sum(b) # envergadura total
        
        self.Ar = self.B**2/self.S # razão de aspecto da asa
        self.Lamb = c[-1]/c[0] # afilamento
        self.Mac = (2/3)*c[0]*(1 + self.Lamb + (self.Lamb)**2)/(1 + self.Lamb) # c media aerodinamca
        self.claf = claf 

        

        
    def simulacao(self, velocity = 35, viscosity = 1.5*10**-5 , g = 9.81, rho = 1.225 ):
        '''criando arquivo txt de input do avl'''

        Re = (velocity/viscosity)*np.array(self.c)
        

        
        # arquivo avl
        with open(path +'\\' +f'asa_{self.id}.avl', 'w') as file:

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
                "20        5.0\n" +
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
                "#------------------------------------------------------------------------\n" +
                "SECTION                                            \n" + 
                "#Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]       \n" +
                "0.0000    0.0000    0.0000    %f   %f    8    3 \n" %(self.c[0], 0.0)+
                "#Camber nao padrao\n" +
                "AFILE\n"+
                "naca24%s.dat\n"%(self.airfoil)+
                "CLAF \n"+
                "%f \n"%(self.claf)+
                "#------------------------------------------------------------------------\n" +
                "SECTION                                     \n" +
                "#Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]\n" +
                "%f    %f    0.0000    %f    %f    8    3  \n" %( self.offset[0],  self.b[0], self.c[1], self.twist[0])+
                "AFILE\n"+
                "naca24%s.dat\n"%(self.airfoil)+
                "CLAF \n"+
                "%f \n"%(self.claf)+
                "#------------------------------------------------------------------------\n" +
                "SECTION                                                     \n" +
                "#Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]   \n" +
                "%f   %f    0.0000    %f    %f   13    1      \n" %( self.offset[0]+self.offset[1],  self.b[0]+self.b[1], self.c[2], self.twist[1])+
                "AFILE\n"+
                "naca24%s.dat\n"%(self.airfoil)+
                "CLAF \n"+
                "%f \n"%(self.claf))
                #+
                #"#------------------------------------------------------------------------\n" +
                #"SECTION                                      \n" +
                #"#Xle Yle Zle   Chord Ainc   [ Nspan Sspace ] \n" +
                #"%f    %f    0.0000    %f   %f   13    1   \n" %( self.offset[0]+self.offset[1]+self.offset[2],  self.b[0]+self.b[1]+self.b[2], self.c[3], self.twist[3])+
                #"AFILE\n"+
                #"%s.dat\n"%(self.airfoil)+
                #"CLAF \n"+
                #"%f \n"%(self.claf)
            

        # arquivo de setup (caso de angulo de ataque preescrito) 
        with open(path +'\\' + f'case_{self.id}.txt', 'w') as file:
            file.write(
                f"LOAD asa_{self.id}\n" +
                "OPER\n" +
                "C1\n" +
                "G\n" +
                "%f\n" %(g) +
                "V\n" +
                "%f\n" %(velocity) +
                "D\n" +
                "%f\n" %(rho) +
                "\n" +
                "M\n" +
                "CD\n" +
                "0.01\n" +
                "\n" +
                "A\n" +
                "A\n" +
                "%f \n" % (self.angle) +
                "X\n"+
                "FT\n"+ # forças totais
                f"saida1_{self.id}.txt\n"+
                "FS\n"+ # forças distribuidas
                f"saida2_{self.id}.txt\n"+
                "\n"+
                "\n"+
                "\n"+
                "QUIT\n"
            )


    def getDados(self):

        # gerando os arquivos
        self.simulacao()

        # rodando a simulação
        #execulta = r'C:\Users\marcy\Desktop\TCC\AeroMan\avl\avl.exe<' + 'case.txt'
        #os.system(execulta) # gera os arquivos de saida.

        wd = os.getcwd()
        os.chdir("/")
        
        p = sp.Popen(f'avl.exe < case_{self.id}.txt',  shell=True, cwd = path)
        try:
            p.wait(20)
        except sp.TimeoutExpired:
            try:
                dev_null = open(os.devnull, 'w')
                command = ['TASKKILL', '/F', '/T', '/PID', str(p.pid)]
                proc = sp.Popen(command, stdin=dev_null, stdout=sys.stdout, stderr=sys.stderr)
                proc.wait(5)
            
            except:
                pass
       
        try:
            #CX_line = (procura('CXtot', 'saida1.txt')) - 1
            CL_line = (procura('CLtot', f'saida1_{self.id}.txt')) - 1

        
            #CXtot_line = leitura(CX_line, 'saida1.txt')
            #CYtot_line = leitura(CX_line + 1, 'saida1.txt')
            #CZtot_line = leitura(CX_line + 2, 'saida1.txt')

            CLtot_line = leitura(CL_line, f'saida1_{self.id}.txt')
            CDtot_line = leitura(CL_line + 1, f'saida1_{self.id}.txt')
            #CDvis_line = leitura(CL_line + 2, f'saida1_{self.id}.txt')
            #CLff_line =  leitura(CL_line + 3, 'saida1.txt')
            #CYff_line =  leitura(CL_line + 4, 'saida1.txt')

            #coeficientes
            CLtot = CLtot_line[2]    # coef. sustentacao total
            CDtot = CDtot_line[2]    # coef. de arrasto total ( avl nao calcula o arrasto viscoso)
            #CDvis = CDvis_line[2]    
            #CDind = CDvis_line[5]   

            eficiencia = float(CLtot)/float(CDtot)
            #CLff = CLff_line[2]   # Trefftz Plane
            #CDff = CLff_line[5]   # Trefftz Plane
            #CYff = CYff_line[2] # Trefftz Plane
            print(CLtot)
            print(CDtot)

            with open(f'{path}\log.txt', 'a') as file:
                file.write(f'cl: \t {CLtot}, cd: \t {CDtot}'+'\n')

        except:
            eficiencia = 0.
            #stal = 1. # se der erro o stal é considerado na ponta 

        # remover arquivos de output
        finally:
         
            if os.path.exists(path +'\\' + f'case_{self.id}.txt'):
                os.remove(path +'\\' + f'case_{self.id}.txt')
            if os.path.exists(path +'\\' + f'asa_{self.id}.avl'):
                os.remove(path +'\\' + f'asa_{self.id}.avl')
            if os.path.exists(path +'\\'+f'saida1_{self.id}.txt'):
                os.remove(path +'\\'+ f'saida1_{self.id}.txt')
            if os.path.exists(path +'\\'+f'saida2_{self.id}.txt'):
                os.remove(path +'\\'+ f'saida2_{self.id}.txt')
    

        return eficiencia#CLtot, CDtot#



        


def procura( palavra, arquivo):

    with open(path +'\\'+ arquivo, 'r') as file:
        number_line = 0
        for number, line in enumerate(file,1):
            if palavra in line:
                number_line = number
    return number_line


def procura2( palavra, arquivo):

    with open(path +'\\'+ arquivo, 'r') as file:
        number_coluna = 0
        number_linha = 0
        for number, line in enumerate(file,0):
            for numero, word in enumerate(line.split(),0):
                if word == palavra:
                    number_coluna = numero
                    number_linha = number
                    return number_coluna, number_linha
    return None, None

def leitura( linha, arquivo): 


    with open(path +'\\'+ arquivo, 'r') as file:
        for line in islice(file, linha-1, linha+1):

            output = line.split()


    return output

def leitura2( linha,coluna, arquivo): 

    output = []
    try:
        with open(path +'\\'+ arquivo, 'r') as file:
            for line in islice(file, linha+1,linha+30):

                output.append(line.split()[coluna])
    except:
        pass


    return np.array(output,dtype='float32')


##### TESTE #####
if __name__ == '__main__':
    """
    gene1 = [1.4299984002640278, 1.3075239875751472, 1.2539656163535653, 1.2801193159007793, 0.9248098839369392, 2.3740222355264318, 0.93637788583294, 0.0039061492849629567, 0.15742830782377398, 0.0]
    gene2 = [1.4205196683390515, 1.3023889430828597, 1.226986381071515, 1.048941939987578, 0.9864347040865333, 2.498559993240941, 0.9826185802935963, 0.0, 0.17229260412172306, 
0.0]
    gene3 = [1.4915805298378915, 1.3294853797760648, 1.2134534861505892, 1.0217896566221618, 0.5038513571137645, 2.4508275412980844, 0.9943552655584549, 0.0, 0.13128054906723288, 0.07506751396389462, -2.971715086233403, -2.8267390616039467, -2.7149356113583876,-2.7149356113583876 ] 

    corda =         gene3[0:4]
    envergadura =   gene3[4:7]
    offset =        gene3[7:10]
    twist =         gene3[10:14]
    
    
    individuo  = Wing(corda, envergadura, offset,twist)
    print(individuo.getDados())
    """
    gene3 = [1.4915805298378915, 1.3294853797760648, 1.2134534861505892, 0.5038513571137645, 2.4508275412980844, 0.0, 0.13128054906723288, 0.07506751396389462, -2.971715086233403, -2.8267390616039467, -2.7149356113583876,-2.7149356113583876 ] 
    gene4 = [1.2635346662878382, 1.2092590534360208, 1.2461015144146927, 4.725533012502635, 1.5975386298325058, 0.1227857094532735, 0.19057217660461323, 2.9006432526953043, 1.5999506650518658, 1.0]

    corda =         gene4[0:3]
    envergadura =   gene4[3:5]
    offset =        gene4[5:7]
    twist =         gene4[7:9]
    t = gene4[-1]
        # ASA
        ## CORDA

         # ASA
        ## CORDA
    C1_INF = 1.2#0.5#
    C1_SUP = 1.8#2.5#


    C2_INF = 0.3#1.0#
    C2_SUP = 2.3#1.6#

    C3_INF = 0.2#0.8
    C3_SUP = 2.2#1.6


        ## ENVERGADURA
    B1_INF = 2.75#2.25#
    B1_SUP = 4.75#5.25#

    B2_INF = 0.625 #0.75
    B2_SUP = 2.265#1.75



        ## OFFSET
    OFFSET1_INF = 0.0#0.0#
    OFFSET1_SUP = 0.3#0.7#

    OFFSET2_INF = 0.0#0.0 #
    OFFSET2_SUP = 0.6#1.0 #



        ## TORÇÃO
    TWIST1_INF = -3.0  #-5#
    TWIST1_SUP = 3.0 #5# 

    TWIST2_INF = -5#-3.0
    TWIST2_SUP = 5#3.0



    t = 15 #[10, 11, 13, 15, 18, 21, 24 ]
    
    
    c1_teste =0.5*(C1_INF+C1_SUP) 

   
    c2_teste =0.5*(C2_INF+C2_SUP) 

   
    c3_teste =0.5*(C3_INF+C3_SUP) 


        ## ENVERGADURA
    
    b1_teste =0.5*(B1_INF+B1_SUP) 

    
    b2_teste =0.5*(B2_INF+B2_SUP) 

    

        ## OFFSET
    
    of1_teste =0.5*(OFFSET1_INF+OFFSET1_SUP) 

    
    of2_teste =0.5*(OFFSET2_INF+OFFSET2_SUP) 

   

        ## TORÇÃO
   
    tw1_teste =0.5*(TWIST1_INF+TWIST1_SUP) 

   
    tw2_teste =0.5*(TWIST2_INF+TWIST2_SUP) 

    

    #gene3 = []
    #corda =         gene3[0:4]
    #envergadura =   gene3[4:7]
    #offset =        gene3[7:10]
    #twist =         gene3[10:14]
    for i in range(0,7):
        
        individuo  = Wing( [c1_teste,c2_teste,c3_teste], [b1_teste,b2_teste], [of1_teste,of2_teste], [tw1_teste, tw2_teste],i)
        #individuo  = Wing( corda, envergadura, offset, twist, t)
        parametros = individuo.getDados()

        with open(f'{path}\Parametros.txt', 'a') as file:
            file.write(f'CL: \t {parametros[0]}, CD: \t {parametros[1]}, \t {i}'+'\n')
# %%
