#%%
import numpy as np
import random
# importar interface xfoil

func = lambda a: sum(a)

class Genetic_simple:
    ''' Functions SGA '''

    def __init__(self, ngen, npop, pmut, pcross, lim_up, lim_down):
        self.ngen = int(ngen) # numero de geracoes 
        self.npop = int(npop) # tamanho da populacao
        self.pmut = float(pmut) # probalidade de mutacao de cada gene
        self.pcross = float(pcross) # probabilidade de crossing 

        self.lim_up = lim_up # limite inferior
        self.lim_down = lim_down # limite superior

        self.nvar = len(self.lim_up) # numero de genes do cromossso

        # gerando a populacao
        self.pop = np.zeros((self.npop, self.nvar)) #self.population() # vetor(nº de indiviuos da pop., nº de cromossos de cada individuo)
        

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

        for i in range(self.npop):
            self.pop[i][:] = self._pop_init()
        

    #-------------- funcoes basicas AGs ------------------

    def mutacao_float(self, individuo):

        ''' operador de mutacao para cod. em ponto flutuante  - mutacao uniforme '''
        # verificar uma outra implentação -> gaussiana ou outra conviniente
        
        for i, xl, xu in zip(self.nvar, self.lim_down, self.lim_up):
            if random.random() < self.pmut:
                individuo[i] = random.uniform(xl, xu)
        

        return self.restricao(individuo)
    
    def crossover(self, individuoA, individuoB):

        ''' operador de crossover - um ponto de troca (mais simples) '''

        pontoTroca = random.randint(1, self.nvar - 1) # nao pegar as extremidades
        individuoA[pontoTroca:], individuoB[pontoTroca:] = individuoB[pontoTroca:], individuoA[pontoTroca:]

        return self.restricao(individuoA), self.restricao(individuoB) 


    def selecao(self, numInd):
        
        ''' operador selecao - seleciona os melhores individuos '''
        melhores = []
        aux = []
        melhores = ( [self.fitness(func, ind), ind] for ind in self.pop)
        #print(sorted(melhores, reverse=True)[:numInd])
        #_, aux = sorted(melhores, reverse=True)[:numInd]
        ord = sorted(melhores, reverse=True)[:numInd]
        aux = [a for _, a in ord]

        return np.array(aux)

    def fitness(self, func, individuo):

        try:
            getValue = func(individuo)
        except:
            getValue = -1

        return getValue

    #-------------- visualizar ------------------------
    
    def display(self):
        pass

class runSga(Genetic_simple):
    ''' Run SGA - simple genetic algorith '''

    def __init__(self):

        super().__init__()

    def run(self):

        for j in range(0, self.ngen):
            # cada pop.

            if j == 0:
               self.population() # inicializa a pop.

            for i in range(0, self.npop):
                # cada indiv.

                ## mutacao -> mod. 1 ind
                self.pop[j][i] = self.mutacao_float(self.pop[j][i])

            ## selecao

            ## crossover -> mod. 2 ind.
            





if __name__ == "__main__":
    inf = [0.3, 0.3, 0.3, 0.3, 0.3] 
    sup = [0.7, 0.7, 0.7, 0.7, 0.7] 
    sga = Genetic_simple(ngen = 10, npop = 20, pmut = 0.05, pcross = 0.002, lim_down = inf, lim_up= sup )




# %%
