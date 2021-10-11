from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import multiprocessing
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
C1_INF = 1.2
C1_SUP = 1.6

C2_INF = 1.2
C2_SUP = 1.6

C3_INF = 1.2
C3_SUP = 1.6

C4_INF = 1.2
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

    ## TORÇÃO
TWIST1_INF = -3.0
TWIST1_SUP = 3.0

TWIST2_INF = -3.0
TWIST2_SUP = 3.0

TWIST3_INF = -3.0
TWIST3_SUP = 3.0

TWIST4_INF = -3.0
TWIST4_SUP = 3.0


'''
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
'''

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

## seções de torção
toolbox.register("twist1", random.randint, TWIST1_INF, TWIST1_SUP)
toolbox.register("twist2", random.randint, TWIST2_INF, TWIST2_SUP)
toolbox.register("twist3", random.randint, TWIST3_INF, TWIST3_SUP)
toolbox.register("twist4", random.randint, TWIST4_INF, TWIST4_SUP)

# tipo de inicialização de individuo 
toolbox.register("individuo", tools.initCycle, creator.Individuo, 
            (toolbox.c1,toolbox.c2,toolbox.c3,toolbox.c4, # CORDA ASA 
            toolbox.b1,toolbox.b2,toolbox.b3, # ENVERGADUA ASA
            toolbox.offset1,toolbox.offset2,toolbox.offset3, # offset
            toolbox.twist1,toolbox.twist2,toolbox.twist3,toolbox.twist4)) #torção))  


# congifuração do AG
toolbox.register("population", tools.initRepeat, list, toolbox.individuo) # tipo de inicialização de população
toolbox.register("mate", tools.cxTwoPoint) # crossover tipo dois pontos de troca (flip)
#toolbox.register("mutate", tools.mutFlipBit, indpb=0.05) # mutação de flip
toolbox.register("select", tools.selTournament, tournsize=5) # seleção por torneio 


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
    
    twist1 = gene[10]
    twist2 = gene[11]
    twist3 = gene[12]
    twist4 = gene[13]
    
    if ( (corda1 >= C1_INF and corda1 <= C1_SUP) and (corda2 >= C2_INF and corda2 <= C2_SUP) and (corda3 >= C3_INF and corda3 <= C3_SUP) and (corda4 >= C4_INF and corda4 <= C4_SUP) \
    and (envergadura1 > B1_INF and envergadura1 <= B1_SUP) and (envergadura2 > B2_INF and envergadura2 <= B2_SUP) and (envergadura3 > B3_INF and envergadura3 <= B3_SUP) \
    and (offset1 >= OFFSET1_INF and offset1 <= OFFSET1_SUP) and (offset2 >= OFFSET2_INF and offset2 <= OFFSET2_SUP) and (offset3 >= OFFSET3_INF and offset3 <= OFFSET3_SUP) \
    and (twist1 >= TWIST1_INF and twist1 <= TWIST1_SUP) and (twist2 >= TWIST2_INF and twist2 <= TWIST2_SUP) and (twist3 >= TWIST3_INF and twist3 <= TWIST3_SUP) and (twist4 >= TWIST4_INF and twist4 <= TWIST4_SUP)): return True
    
    return False



####### Fitness #######
def funcaoObjetivo(gene):
    ''' recebe o gene do individuo '''
    efici = funcaoAvl(gene)

    return [efici,]

def funcaoAvl(gene):

    corda = gene[0:4]
    envergadura = gene[4:7]
    offset = gene[7:10]
    twist = gene[10:14]
    
   
    individuo  = avl.Wing(corda, envergadura, offset, twist)

    efici = individuo.getDados()
    

    return efici




toolbox.register("evaluate", funcaoObjetivo)
#toolbox.decorate("evaluate", tools.DeltaPenalty(checkGeometria, [1.0, ]))

####### Display #######

def main(number_ind, geracao):
    # individuo por populacao
    
    random.seed(64)
    
    pool = multiprocessing.Pool(processes=2)
    toolbox.register("map", pool.map)

    pop = toolbox.population(n=number_ind)  
    hof = tools.HallOfFame(5)  
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop, logger = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=geracao, stats=stats, halloffame=hof, verbose=True)
    return [pop, logger, hof]

if __name__ == "__main__":
    # Run main function
    import time 
    start = time.time()
    [pop, logger, hof] = main(50, 15)
    finish = time.time()

    # Plot the results
    best = hof.items[0]
    print()
    print("Tempo: ", finish-start)
    print("Melhor Solucao = ", best)
    print("Fitness do melhor individuo = ", best.fitness.values[0])
   

    print(logger)
    import matplotlib.pyplot as plt
    gen = logger.select("gen")
    fit = logger.select("max")
    avg = logger.select("avg")
    plt.plot(gen, fit, '--r', label = "melhores individuos")
    plt.plot(gen, avg, '--b', label = "media dos individuos")
    plt.xlabel('fitness')
    plt.ylabel('geração')
    plt.legend()
    plt.title('Pontuação dos melhores individuos')
    plt.grid()
    plt.show()

