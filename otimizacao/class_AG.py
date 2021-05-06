#%%
import numpy as np
import random

# importar interface xfoil

func = lambda a: sum(a)

class Genetic_simple(object):
    ''' Functions SGA '''

    def __init__(self, ngen, npop, pmut, lim_up, lim_down):
        
        self.ngen = int(ngen) # numero de geracoes 
        self.npop = int(npop) # tamanho da populacao
        self.pmut = float(pmut) # probalidade de mutacao de cada gene

        self.lim_up = lim_up # limite inferior
        self.lim_down = lim_down # limite superior

        self.nvar = len(self.lim_up) # numero de genes do cromossso


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

        for i in range(self.npop):

            populacao.append( self._pop_init() )

        return populacao
        

    #-------------- funcoes basicas AGs ------------------

    def mutacao_float(self, individuo):

        ''' operador de mutacao para cod. em ponto flutuante  - mutacao uniforme '''
        # verificar uma outra implentação -> gaussiana ou outra conviniente pob = 0.05
        
        for i, xl, xu in zip(range(self.nvar), self.lim_down, self.lim_up):
            if random.random() < self.pmut:
                individuo[i] = random.uniform(xl, xu)
        

        return self.restricao(individuo)
    
    def mutacao(self, populacao):

        ''' recebe um populacao para aplicar o operador de mutacao '''

        for i in range(len(populacao)):
            # cada indiv.
            
            ## mutacao -> mod. 1 ind
            populacao[i] = self.mutacao_float(populacao[i])

        return populacao
  

    def crossover(self, individuoA, individuoB):

        ''' operador de crossover - um ponto de troca (mais simples) '''

        pontoTroca = random.randint(1, self.nvar - 1) # nao pegar as extremidades
        individuoA[pontoTroca:], individuoB[pontoTroca:] = individuoB[pontoTroca:], individuoA[pontoTroca:]

        return self.restricao(individuoA), self.restricao(individuoB) 

    def filhos(self, pop):
        
        ''' gera a pop. de filhos '''
        populacao = pop.copy()
        pop_aux = list()

        while( len(populacao) > 0):
            
            pai = random.choice(populacao)
            populacao.remove(pai)
            mae = random.choice(populacao)
            populacao.remove(mae)
            
            filho1, filho2 = self.crossover(pai,mae)

            pop_aux.append( filho1 )
            pop_aux.append( filho2 )

        return pop_aux

        

    def mistura(self, populacaoA, populacaoB):
        

        pop_total = list()

        pop_total.extend(populacaoA)
        pop_total.extend(populacaoB)
        
        return pop_total


    def selecao(self, populacao, numInd):
        
        ''' operador selecao - seleciona os melhores individuos '''
        melhores = list()
        aux = list()
        aux = ( [self.fitness(func, ind), ind] for ind in populacao )
        #print(sorted(melhores, reverse=True)[:numInd])
        #_, aux = sorted(melhores, reverse=True)[:numInd]
        ord = sorted(aux, reverse=True)[:numInd]
        melhores = [a for _, a in ord]

        return melhores

    def fitness(self, func, individuo):

        try:
            getValue = func(individuo)
        except:
            getValue = -1

        return getValue


    def run(self):

        for j in range(0, self.ngen):
            # cada pop.

            if j == 0:
                # inicializando o vetor populacao self.pop[n_geracao][n_individuos]
               
                pop = self.population() # inicializa a pop.

            #print(len(pop))
            # passando a pop toda para o operador de mutacao
            
            #print('\n')
            #print(' antes da mutacao' ,pop)
            pop = self.mutacao(pop)
            #print('\n')
            #print(' depois da mutacao' ,pop)
           

            #print(len(pop))
            ## crossover -> mod. 2 ind. (filhos)]
            pop1 = pop.copy()
            filhos = self.filhos(pop1)

            #print('len filhos ',len(filhos))
            ## mistura
            pop_aux = self.mistura(pop, filhos) 

            #print(len(pop),pop)
            # melhor individuo e fitness
            fitness, melhor = self.melhorInd(pop)
            print( f' Geracao: {j} ')
            print( f' Melhor fitness: {fitness} , {melhor}')
            print( f' Tamanho da pop.: {len(pop)}')
            #print( f' Melhor individuo: {melhor} ')

            ## selecao
            pop = self.selecao(pop_aux, len(pop))
            

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
    inf = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3] 
    sup = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7] 
    #algoritmo_genetico = Genetic_simple()
    # npop deve ser par

    sga = Genetic_simple(ngen = 500, npop = 200, pmut = 0.05, lim_up= sup, lim_down = inf )
    sga.run()

   




# %%
