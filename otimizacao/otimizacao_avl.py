from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from pathlib import Path
import sys
import random
import numpy as np

if str(Path(Path().absolute())).split('\\')[-1] == 'AeroMan':
    path_avl = str(Path(Path().absolute())) + r'\avl'
else:
    path_avl = str(Path(Path().absolute().parents[0])) + r'\avl'

sys.path.insert(1, path_avl)
import avl as avl

####### Definições #######
# ASA
    ## CORDA
C1_INF = 1.4
C1_SUP = 1.6

C2_INF = 1.3
C2_SUP = 1.6

C3_INF = 1.2
C3_SUP = 1.6

C4_INF = 1.0
C4_SUP = 1.6

    ## ENVERGADURA
B1_INF = 0.5
B1_SUP = 1.0

B2_INF = 1.5
B2_SUP = 2.5

B3_INF = 0.5
B3_SUP = 1.0

    ## OFFSET
OFFSET1_INF = 0.0
OFFSET1_SUP = 0.2

OFFSET2_INF = 0.0
OFFSET2_SUP = 0.2

OFFSET3_INF = 0.0
OFFSET3_SUP = 0.2

# EMPENAGE HORIZONTAL
LH_INF = 4.2
LH_SUP = 4.2

    ## RAIZ
CH_R_INF = 1.0
CH_R_SUP = 1.3

    ## PONTA
CH_T_INF = 0.7
CH_T_SUP = 1.0

    ## ENVERGADURA
BH_INF = 1.3
BH_SUP = 1.6

    ## OFFSET
OFFSET_EMPH_INF = 0.0 
OFFSET_EMPH_SUP = 0.3 

# EMPENAGE VERTICAL

    ## RAIZ
CV_R_INF = 1.3
CV_R_SUP = 1.5

    ## PONTA
CV_T_INF = 0.7
CV_T_SUP = 1.0

    ## ENVERGADURA
BV_INF = 1.3
BV_SUP = 2.0

    ## OFFSET
OFFSET_EMPV_INF = 0.3
OFFSET_EMPV_SUP = 0.8 



SIZE_INDIVIDUO = 19 # numero de variaveis de otimização
creator.create("FitnessMax", base.Fitness, weights = (1.,)) # função fitness de maximação
creator.create("Individuo", list, fitness = creator.FitnessMax)

toolbox = base.Toolbox()

# ASA
## seções de corda
toolbox.register("c1", random.uniform, C1_INF, C1_SUP)
toolbox.register("c2", random.uniform, C2_INF, C2_SUP)
toolbox.register("c3", random.uniform, C3_INF, C3_SUP)
toolbox.register("c4", random.uniform, C4_INF, C4_SUP)

## seções de envergadura
toolbox.register("b1", random.uniform, B1_INF, B1_SUP)
toolbox.register("b2", random.uniform, B2_INF, B2_SUP)
toolbox.register("b3", random.uniform, B3_INF, B3_SUP)

## seções de offset
toolbox.register("offset1", random.uniform, OFFSET1_INF, OFFSET1_SUP)
toolbox.register("offset2", random.uniform, OFFSET2_INF, OFFSET2_SUP)
toolbox.register("offset3", random.uniform, OFFSET3_INF, OFFSET3_SUP)

# EMPENAGE - HORIZONTAL
#toolbox.register("lh", random.uniform, LH_INF, LH_SUP) 
#
### cordas
#toolbox.register("ch1", random.uniform, CH_R_INF, CH_R_SUP)
#toolbox.register("ch2", random.uniform, CH_T_INF, CH_T_SUP)
#
### seções de envergadura
#toolbox.register("bh1", random.uniform, BH_INF,BH_SUP)
#
### seções de offset
#toolbox.register("offseth1", random.uniform, OFFSET_EMPH_INF, OFFSET_EMPH_SUP)
#
## EMPENAGE - VERTICAL
#
### cordas
#toolbox.register("cv1", random.uniform, CV_R_INF, CV_R_SUP)
#toolbox.register("cv2", random.uniform, CV_T_INF, CV_T_SUP)
#
### seções de envergadura
#toolbox.register("bv1", random.uniform, BV_INF,BV_SUP)
#
### seções de offset
#toolbox.register("offsetv1", random.uniform, OFFSET_EMPV_INF, OFFSET_EMPV_SUP)
#


# tipo de inicialização de individuo 
toolbox.register("individuo", tools.initCycle, creator.Individuo, 
            (toolbox.c1,toolbox.c2,toolbox.c3,toolbox.c4, # CORDA ASA 
            toolbox.b1,toolbox.b2,toolbox.b3, # ENVERGADUA ASA
            toolbox.offset1,toolbox.offset2,toolbox.offset3, # OFFSET ASA
            #toolbox.lh, toolbox.ch1, toolbox.ch2, toolbox.bh1, toolbox.offseth1,  # EMPENAGE HORIZONTAL
            #toolbox.cv1, toolbox.cv2, toolbox.bv1, toolbox.offsetv1,  # EMPENAGE VERTICAL
            ))  


# congifuração do AG
toolbox.register("population", tools.initRepeat, list, toolbox.individuo) # tipo de inicialização de população
toolbox.register("mate", tools.cxTwoPoint) # mutação tipo dois pontos de troca (flip)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=2) # seleção por torneio 

####### Validação #######
def checkGeometria(gene):

    # ASA
    corda1 = gene[0]
    corda2 = gene[1]
    corda3 = gene[2]
    corda4 = gene[3]
    
    envergadura1 = gene[4]
    envergadura2 = gene[5]
    envergadura3 = gene[6]

    offset1 = gene[7]
    offset2 = gene[8]
    offset3 = gene[9]

    # EMPENAGE HORIZONTAL 
    #lh = gene[10]
    #cordaH1 = gene[11]
    #cordaH2 = gene[12]
    #
    #envergaduraH1 = gene[13]
    #
    #offsetH1 = gene[14]
    #
    ## EMPENAGE VERTICAL 
    #cordaV1 = gene[15] # corda na raiz 
    #cordaV2 = gene[16] # corda na ponta
    #
    #envergaduraV1 = gene[17]
    #offsetV1 = gene[18]
    
    if ( (corda1 >= C1_INF and corda1 <= C1_SUP) and (corda2 >= C2_INF and corda2 <= C2_SUP) and (corda3 >= C3_INF and corda3 <= C3_SUP) and (corda4 >= C4_INF and corda4 <= C4_SUP) \
    and (envergadura1 > B1_INF and envergadura1 <= B1_SUP) and (envergadura2 > B2_INF and envergadura2 <= B2_SUP) and (envergadura3 > B3_INF and envergadura3 <= B3_SUP) \
    and (offset1 >= OFFSET1_INF and offset1 <= OFFSET1_SUP) and (offset2 >= OFFSET2_INF and offset2 <= OFFSET2_SUP) and (offset3 >= OFFSET3_INF and offset3 <= OFFSET3_SUP)): return True
    #and \
    #(cordaH1 >= CH_R_INF and cordaH1 <= CH_R_SUP) and (cordaH2 >= CH_T_INF and cordaH2 <= CH_T_SUP) #and (envergaduraH1 >= BH_INF and envergaduraH1 <= BH_SUP) and (offsetH1 >= OFFSET_EMPH_INF and  #offsetH1 <= OFFSET_EMPH_SUP) and \
    #(cordaV1 >= CV_R_INF and cordaV1 <= CV_R_SUP) and (cordaV2 >= CV_T_INF and cordaV2 <= CV_T_SUP) #and (envergaduraV1 >= BV_INF and envergaduraV1 <= BV_SUP) and (offsetV1 >= OFFSET_EMPV_INF and  #offsetV1 <= OFFSET_EMPV_SUP)):
    # Calculo do volume de cauda vertical
    #    afilamentoV = cordaV2/cordaV1
    #    macV = (2/3)*cordaV1*(1 + afilamentoV + (afilamentoV)**2)/(1 + afilamentoV)
    #    lhv = 0.25*macV + lh
    #    sv = (cordaV1+cordaV2)*envergaduraV1/2 # area da empenagem vertical
    #    sw = 2*((corda1+corda2)*envergadura1 + (corda2+corda3)*envergadura2 + (corda3+ corda4)#*envergadura3)# area da asa
    #    b = 2*(envergadura1+envergadura2+envergadura3) #envergadura da asa
    #    Vv = lhv*sv/(sw*b)
    #    # Calculo do volume de cauda horizontal
    #    afilamentoH = cordaH2/cordaH1
    #    afilamento = corda4/corda1
    #    cmac = (2/3)*corda1*(1 + afilamento + (afilamento)**2)/(1 + afilamento)
    #    macH = (2/3)*cordaH1*(1 + afilamentoH + (afilamentoH)**2)/(1 + afilamentoH)
    #    lhh = 0.25*macH + lh
    #    sh = (cordaH1+cordaH2)*envergaduraH1
    #    Vh = lhh*sh/(cmac*sw)
    #    
    #    print(Vh, Vv)
    #    if ( Vh >= 0.3 and Vh<= 0.5) and (Vv >= 0.03 and Vv<= 0.05):
    #        return True
    return False
    


####### Fitness #######
def funcaoObjetivo(gene):
    ''' recebe o gene do individuo '''
    print(gene)
    # Asa
    corda = gene[0:4]
    envergadura = gene[4:7]
    offset = gene[7:10]
    
    # EMPENAGE HORIZONTAL 
    #lh = gene[10]
    #cordaH = gene[11:13]
    #envergaduraH = gene[13]
    #offsetH = gene[14]
    #
    ## EMPENAGE VERTICAL 
    #cordaV = gene[15:17]  
    #envergaduraV = gene[17]
    #offsetV = gene[18]

    #lh, c_htail, envH, offset_htail, c_vtail, envV, offset_vtail,
    individuo  = avl.Wing(corda, envergadura, offset)#, lh, cordaH, envergaduraH, offsetH, cordaV, envergaduraV, offsetV )

    fit = individuo.getDados()

    return [fit,]


toolbox.register("evaluate", funcaoObjetivo)
toolbox.decorate("evaluate", tools.DeltaPenalty(checkGeometria, [-1.0, ]))

####### Display #######

def main():
    # individuo por populacao
    number_ind = 150
    pop = toolbox.population(n=number_ind)  
    hof = tools.HallOfFame(int(0.25*number_ind))  
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop, logger = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=35, stats=stats, halloffame=hof, verbose=True)
    return [pop, logger, hof]


# Run main function
[pop, logger, hof] = main()

# Plot the results
best = hof.items[0]
print()
print("Melhor Solucao = ", best)
print("Fitness do melhor individuo = ", best.fitness.values[0])
#print(hof[0])
#print(hof[1])
#print(hof[2])
#print(hof[3])
#print(hof[4])

#print('# #=============================================================================######################')
#print('Score:', best.fitness.values[0])
#print('# #=============================================================================######################')

print(logger)
import matplotlib.pyplot as plt
gen = logger.select("gen")
fit = logger.select("max")
avg = logger.select("avg")
plt.plot(gen,fit, '--r', label = "melhores individuos")
plt.plot(gen,avg, '--b', label = "media dos individuos")
plt.xlabel('fitness')
plt.ylabel('geração')
plt.title('Pontuação dos melhores individuos')
plt.grid()
plt.show()

