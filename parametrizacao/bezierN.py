class BezierN:
    order = 1
    binom = []
    tts   = []
    ts    = []
    
    def __init__(self, order_N):
        ''' Inicializa os termos da curva de Bezier e gera o binomio de acordo com a ordem de precisão '''
        self.order = order_N
        self.binom = [0]* self.order
        self.ts    = [0]* self.order
        self.tts   = [0]* self.order
        self.binom[0]=1
        for i in range (1,self.order+1):
            temp=self.binom[0]
            for ii in range (1,i):
                temp2= self.binom[ii]
                self.binom[ii]=temp+self.binom[ii]
                temp = temp2
                

    def polinomio(self,coefs, n ): 

        ''' Gera o polinomio de bezier tomando os pontos de controle com input e numero de pontos da curva'''
        output = [0]*(n+1)
        step = 1.0/float(n)
        t = 0
        output[0]=coefs[0]
        for i in range (1,n+1):
            t+=step
            tt=1.0-t
            ttemp=1.0
            tttemp=1.0
            for j in range (0,self.order):  # generate powers of t
                self.ts[j] = ttemp
                self.tts[self.order-j-1] = tttemp
                ttemp*=t
                tttemp*=tt
            output[i]=0
            for j in range (0,self.order):  
                output[i]+=coefs[j]*self.tts[j]*self.ts[j]*self.binom[j]
        return output


if __name__ == '__main__':

    upx = [0, 0,  0.25,0.5,0.75,1]
    downx = upx

    upy =   [0,  0.05,    0.2,  0.15,  0.1 ,       0]
    downy = [0, -0.05,   -0.1,  0.10,  0.05,       0]

    n=50
    Bezier = BezierN(6)

    #=MyBesier.polinomio([0,3,2,1,0],10)
    #print besierout

    pupx  = Bezier.polinomio(upx   ,n)
    pupy  = Bezier.polinomio(upy   ,n)
    pdownx= Bezier.polinomio(downx ,n)
    pdowny= Bezier.polinomio(downy ,n)

    import matplotlib.pyplot as plt 
    plt.figure()

    plt.plot(upx,upy,'or')
    plt.plot(downx,downy,'ob')
    plt.plot(pupx,pupy,'r')
    plt.plot(pdownx,pdowny,'b')
    plt.show()



