#%%
import numpy as np
import random
import matplotlib.pyplot as plt


class Genetic_simple(object):
    ''' Functions SGA '''

    def __init__(self, ngen, npop, pmut, best, pcross, function, lim_up, lim_down):
        
        self.ngen = int(ngen) # numero de geracoes 
        self.npop = int(npop) # tamanho da populacao
        self.pmut = float(pmut) # probalidade de mutacao de cada gene
        self.pcross = float(pcross) # porcentagem da melhor pop. a cruzar
        self.lim_up = lim_up # limite inferior
        self.lim_down = lim_down # limite superior

        self.best = best # quantos dos melhores individuos passam para proxima

        self.nvar = len(self.lim_up) # numero de genes do cromossso

        # defininfo a função fitness
        self.function = function

    # ------- inicialização -----------
    def restricao(self, ind):

        ''' inserir restrições geometricas por exemplo '''
        #intra = ind[:]
        #extra = ind[:]

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
        
        melhores = [ (self.fitness(ind), ind) for ind in populacao ]
        melhores = sorted(melhores)
        melhores = [indiv for _, indiv in melhores]

        populacao = melhores # pop. ordenada
        metchPool = round(len(populacao)*(1-self.pcross))

        melhores = melhores[metchPool:]
        #print('len melhores ', len(melhores))

        for i in range(len(populacao) - self.best):

            parent = random.sample(melhores, 2)
            filho1, filho2 = self.crossover(parent[0], parent[1])
            
            populacao[i][:] = filho1

            if i+1 > (len(populacao) - self.best):
                break

            populacao[i+1][:] = filho2

        return populacao
    

    def crossover(self, individuoA, individuoB):

        ''' operador de crossover - um ponto de troca (mais simples) '''

        pontoTroca = random.randint(1, self.nvar - 1) # nao pegar as extremidades
        individuoA[pontoTroca:], individuoB[pontoTroca:] = individuoB[pontoTroca:], individuoA[pontoTroca:]

        return self.restricao(individuoA), self.restricao(individuoB)


    def fitness(self, individuo):

        try:
            getValue = self.function(individuo)
        except:
            getValue = -1

        return getValue


    def run(self):

        plt.figure()

        for j in range(0, self.ngen):
            # cada pop.

            if j == 0:
               
                pop = self.population() # inicializa a pop.

            pop = self.selecao(pop)
            # passando a pop toda para o operador de mutacao
            pop = self.mutacao(pop)
            
            #print(len(pop),pop)
            # melhor individuo e fitness
            fitness, melhor = self.melhorInd(pop)


            print( f' Geracao: {j+1} | Tamanho da pop.: {len(pop)}')
            print( f' Melhor fitness: {fitness} , {melhor} \n')
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
        aux = ( [self.fitness(ind), ind] for ind in populacao )
        fitness, melhor = sorted(aux, reverse=True)[0]
    

        return fitness, melhor
        


if __name__ == "__main__":
    
    inf = [0.3, 0.3, 0.3, 0.3] 
    sup = [0.7, 0.7, 0.7, 0.7] 
    #algoritmo_genetico = Genetic_simple()
    # npop deve ser par
    func = lambda x : sum(x)

    validacao = Genetic_simple(ngen = 30, npop = 300, pmut = 0.015, best = 30, pcross = 0.95, function = func, lim_up= sup, lim_down = inf )
    pop = validacao.run()
    
   




# %%
