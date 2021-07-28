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

    def __init__(self, c, b, offset, angle = 3, twist = None):#, lh, c_htail, envH, offset_htail, c_vtail, envV, offset_vtail, angle = 3, twist = None):

        '''
        Parametros:
        
        ASA
        c : cordas da asa [c1, c2, c3, c4];
        b : envergadura [b1, b2, b3];
        offset : distancia de recuo do borda de ataque [offset1, offset2, offset3].

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

        #ASA
        ##vetores
        self.c = c
        self.b = b
        self.offset = offset

        ##EMPENAGEM
#
        ###horizontal
        #self.lh = lh
        #self.c_htail = c_htail
        #self.envH = envH
        #self.offset_htail = offset_htail
        #
        ###vertical
        #self.c_vtail = c_vtail
        #self.envV = envV
        #self.offset_vtail = offset_vtail


        ##escalares
        self.angle = angle
        self.S = 2*((c[0]+c[1])*b[0]/2 + (c[1]+c[2])*(b[1])/2 + (c[2]+c[3])*(b[2])/2) # area projetada a asa
        self.B = 2*sum(b) # envergadura total
        self.Ar = self.B**2/self.S # razão de aspecto da asa
        self.Lamb = c[-1]/c[0] # afilamento
        self.Mac = (2/3)*c[0]*(1 + self.Lamb + (self.Lamb)**2)/(1 + self.Lamb) # c media aerodinamca

        

        
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
                "0.0000    0.0000    0.0000    %f   0.000    8    3 \n" %(self.c[0])+
                "#Camber nao padrao\n" +
                #"AFIL 0.0 1.0\n"+
                "NACA\n"+
                "2024\n"+
                "#------------------------------------------------------------------------\n" +
                "SECTION                                     \n" +
                "#Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]\n" +
                "%f    %f    0.0000    %f   0.000    8    3  \n" %( self.offset[0],  self.b[0], self.c[1])+
                #"AFIL 0.0 1.0\n"+
                "NACA\n"+
                "2024\n"+
                "#------------------------------------------------------------------------\n" +
                "SECTION                                                     \n" +
                "#Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]   \n" +
                "%f   %f    0.0000    %f   0.000   13    1      \n" %( self.offset[0]+self.offset[1],  self.b[0]+self.b[1], self.c[2])+
                #"AFIL 0.0 1.0\n"+
                "NACA\n"+
                "2024\n"+
                "#------------------------------------------------------------------------\n" +
                "SECTION                                      \n" +
                "#Xle Yle Zle   Chord Ainc   [ Nspan Sspace ] \n" +
                "%f    %f    0.0000    %f   0.000   13    1   \n" %( self.offset[0]+self.offset[1]+self.offset[2],  self.b[0]+self.b[1]+self.b[2], self.c[3])+
                #"AFIL 0.0 1.0\n" +
                "NACA\n"+
                "2024\n"

                #EMPENAGE
                #"#====================================================================\n"+
                #"SURFACE                      \n" +
                #"Horizontal tail\n"+
                #"5  1.0  7  -1.5  ! Nchord   Cspace\n"+
                #"YDUPLICATE\n"+
                #"0.00000\n"+
                #"#--------------------------------------------------------------\n"+
                #"SECTION\n"+
                ##!Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace
                #"%f     0.00000     0.00000     %f         0.000   7  -1.5\n"%(self.lh, self.c_htail#[0])+ #( distancia da empenage, corda na raiz)
                #"\n"+
                #"#-----------------------\n"+
                #"SECTION\n"+
                ##!Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace
                #"%f        %f         0.00000     %f         0.000   1   0\n"%(self.offset_htail+self.#lh, self.envH, self.c_htail[1])+ #(offset da ponta, semi-envegadura, corda na ponta)
#
                #"#====================================================================\n"+
                #"SURFACE                      \n" +
                #"Vertical tail\n"+
                #"6  1.0  10  0.5  ! Nchord   Cspace \n"+
                #"#-------------------------------------------------------------- \n"+
                #"SECTION \n"+
                ##!Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace
                #"%f   0.00000    0.00000     %f     0.000   3   1.5 \n"%(self.lh, self.c_vtail[0])+
                #"#----------------------- \n"+
                #"SECTION \n"+
                ##!Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace
                #"%f   0.00000     %f       %f     0.000   1   0 \n"%(self.lh + self.offset_vtail, #self.envV,  self.c_vtail[1])
            )

        # arquivo de setup (caso de angulo de ataque preescrito) 
        with open(path +'\\' + f'case.txt', 'w') as file:
            file.write(
                f"LOAD asa_{self.id}.avl\n" +
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
                f"saida1_{self.id}.txt\n"+
                #"FS\n"+ # forças distribuidas
                #"saida2.txt\n"+
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
        
        p = sp.Popen(f'avl.exe < case.txt',  shell=True, cwd = path)
        try:
            p.wait(10)
        except sp.TimeoutExpired:
            dev_null = open(os.devnull, 'w')
            command = ['TASKKILL', '/F', '/T', '/PID', str(p.pid)]
            proc = sp.Popen(command, stdin=dev_null, stdout=sys.stdout, stderr=sys.stderr)
            proc.wait(5)
       
        try:
            #CX_line = (procura('CXtot', 'saida1.txt')) - 1
            CL_line = (procura('CLtot', f'saida1_{self.id}.txt')) - 1

        
            #CXtot_line = leitura(CX_line, 'saida1.txt')
            #CYtot_line = leitura(CX_line + 1, 'saida1.txt')
            #CZtot_line = leitura(CX_line + 2, 'saida1.txt')

            CLtot_line = leitura(CL_line, f'saida1_{self.id}.txt')
            CDtot_line = leitura(CL_line + 1, f'saida1_{self.id}.txt')
            CDvis_line = leitura(CL_line + 2, f'saida1_{self.id}.txt')
            #CLff_line =  leitura(CL_line + 3, 'saida1.txt')
            #CYff_line =  leitura(CL_line + 4, 'saida1.txt')

            #coeficientes
            CLtot = CLtot_line[2]    # coef. sustentacao total
            CDtot = CDtot_line[2]    # coef. de arrasto total ( avl nao calcula o arrasto viscoso)
            CDvis = CDvis_line[2]    
            CDind = CDvis_line[5]   

            eficiencia = float(CLtot)/float(CDtot)
            #CLff = CLff_line[2]   # Trefftz Plane
            #CDff = CLff_line[5]   # Trefftz Plane
            #CYff = CYff_line[2] # Trefftz Plane

        except:
            eficiencia = 0.

        # remover arquivos de output
        #try:
        if os.path.exists(path +'\\' + f'asa_{self.id}.avl'):
            os.remove(path +'\\' + f'asa_{self.id}.avl')
        
        if os.path.exists(path +'\\' + f'case.txt'):
            os.remove(path +'\\' + f'case.txt')

        if os.path.exists(path +'\\'+f'saida1_{self.id}.txt'):
            os.remove(path +'\\'+ f'saida1_{self.id}.txt')
        #except:
        #    pass
       

        return eficiencia



        


def procura( palavra, arquivo):

    with open(path +'\\'+ arquivo, 'r') as file:
        number_line = 0
        for number, line in enumerate(file,1):
            if palavra in line:
                number_line = number
    return number_line


def leitura( linha, arquivo): 


    with open(path +'\\'+ arquivo, 'r') as file:
        for line in islice(file, linha-1, linha+1):

            output = line.split()


    return output



##### TESTE #####
if __name__ == '__main__':
    gene1 = [1.4299984002640278, 1.3075239875751472, 1.2539656163535653, 1.2801193159007793, 0.9248098839369392, 2.3740222355264318, 0.93637788583294, 0.0039061492849629567, 0.15742830782377398, 0.0]
    gene2 = [1.4205196683390515, 1.3023889430828597, 1.226986381071515, 1.048941939987578, 0.9864347040865333, 2.498559993240941, 0.9826185802935963, 0.0, 0.17229260412172306, 
0.0]
    corda = gene2[0:4]
    envergadura = gene2[4:7]
    offset = gene2[7:10]
    
    
    individuo  = Wing(corda, envergadura, offset)
    individuo.getDados()