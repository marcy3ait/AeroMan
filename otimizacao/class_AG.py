#%%
import numpy as np
import random
import matplotlib.pyplot as plt

# importar interface xfoil

func = lambda a: sum(a)
parents = 5

class Genetic_simple(object):
    ''' Functions SGA '''

    def __init__(self, ngen, npop, pmut, best, lim_up, lim_down):
        
        self.ngen = int(ngen) # numero de geracoes 
        self.npop = int(npop) # tamanho da populacao
        self.pmut = float(pmut) # probalidade de mutacao de cada gene

        self.lim_up = lim_up # limite inferior
        self.lim_down = lim_down # limite superior

        self.best = best # quantos dos melhores individuos passam para proxima

        self.nvar = len(self.lim_up) # numero de genes do cromossso

    # ------- inicialização -----------
    def restricao(self, ind):

        ''' inserir restrições geometricas por exemplo '''

        return ind

    def _pop_init(self):

        ''' retorna um individuo considerando codificacao em ponto flutuante '''

        individuo = [0]*self.nvar

        for i in range(0,self.nvar):
            individuo[i] = random.uniform(self.lim_down[i],self.lim_up[i])

        return self.restricao(individuo)

    def population(self):

        ''' cria a pop. de individuos '''
        populacao = list()

        for _ in range(self.npop):

            populacao.append( self._pop_init() )

        return populacao
        

    #-------------- funcoes basicas AGs ------------------

    
    def mutacao(self, populacao):

        ''' recebe um populacao para aplicar o operador de mutacao '''

        for i in range(len(populacao)):
            # cada indiv.
            
            ## mutacao -> mod. 1 ind
            if random.random() <= self.pmut:

                point = random.randint(0, self.nvar - 1) # ponto do cromosso para realizar  a mutacao
                novo_valor  = random.uniform( self.lim_down[point], self.lim_up[point] )
                
                # verificar se esse novo valor é diferente
                while (novo_valor == populacao[i][point]):
                    novo_valor  = random.uniform(self.lim_down[point],self.lim_up[point])

                populacao[i][point] = novo_valor

                populacao[i] = self.restricao(populacao[i])

        return populacao
        
    
    def selecao(self, populacao):
        
        melhores = [ (self.fitness(func, ind), ind) for ind in populacao ]
        melhores = sorted(melhores)
        melhores = [indiv for _, indiv in melhores]

        populacao = melhores # pop. ordenada

        for i in range(len(populacao) - self.best):

            point = random.randint(1, self.nvar - 1)
            parent = random.sample(melhores, 2)
            filho = self.crossover(parent[0], parent[1])
            populacao[i][:] = filho

        return populacao
    

    def crossover(self, individuoA, individuoB):

        ''' operador de crossover - um ponto de troca (mais simples) '''

        pontoTroca = random.randint(1, self.nvar - 1) # nao pegar as extremidades
        individuoA[pontoTroca:], individuoB[pontoTroca:] = individuoB[pontoTroca:], individuoA[pontoTroca:]

        return self.restricao(individuoA)


    def fitness(self, func, individuo):

        try:
            getValue = func(individuo)
        except:
            getValue = -1

        return getValue


    def run(self):

        plt.figure()

        for j in range(0, self.ngen):
            # cada pop.

            if j == 0:
                # inicializando o vetor populacao self.pop[n_geracao][n_individuos]
               
                pop = self.population() # inicializa a pop.

            pop = self.selecao(pop)
            # passando a pop toda para o operador de mutacao
            pop = self.mutacao(pop)
            
            #print(len(pop),pop)
            # melhor individuo e fitness
            fitness, melhor = self.melhorInd(pop)


            print( f' Geracao: {j} | Tamanho da pop.: {len(pop)}')
            print( f' Melhor fitness: {fitness} , {melhor} \n')
            #print(pop)
            #print( f' Melhor individuo: {melhor} ')
            plt.plot(j, fitness, 'or')

        plt.grid()
        plt.xlabel('geracoes')
        plt.ylabel('fitness')
        plt.show()

        return pop

    #-------------- visualizar ------------------------
    
    def melhorInd(self, populacao):
        
        aux = []
        aux = ( [self.fitness(func, ind), ind] for ind in populacao )
        #print(sorted(melhores, reverse=True)[:numInd])
        #_, aux = sorted(melhores, reverse=True)[:numInd]
        #print(sorted(aux, reverse=True)[0])
        fitness, melhor = sorted(aux, reverse=True)[0]
    

        return fitness, melhor
        


if __name__ == "__main__":
    inf = [0.3, 0.3, 0.3, 0.3] 
    sup = [0.7, 0.7, 0.7, 0.7] 
    #algoritmo_genetico = Genetic_simple()
    # npop deve ser par

    validacao = Genetic_simple(ngen = 200, npop = 50, pmut = 0.2, best = 5, lim_up= sup, lim_down = inf )
    pop = validacao.run()

   




# %%
