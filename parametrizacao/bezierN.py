import matplotlib.pyplot as plt 
import numpy as np
from scipy.optimize import minimize

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
            temp = self.binom[0]
            for ii in range (1,i):
                temp2 = self.binom[ii]
                self.binom[ii] = temp+self.binom[ii]
                temp = temp2
                

    def polinomio(self,coefs, n ): 

        ''' Gera o polinomio de bezier tomando os pontos de controle com input e numero de pontos da curva'''
        output = [0]*(n+1)
        step = 1.0/float(n)
        t = 0
        output[0] = coefs[0]
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
    
    n=100
    Bezier = BezierN(6)
    
    pupx  = Bezier.polinomio(upx   ,n)
    pupy  = Bezier.polinomio(upy   ,n)
    pdownx= Bezier.polinomio(downx ,n)
    pdowny= Bezier.polinomio(downy ,n)

    plt.figure()

    #plt.plot(upx,upy,'or')
    #plt.plot(downx,downy,'ob')
    plt.plot(pupx,pupy,'r')
    plt.plot(pdownx,pdowny,'b')

    plt.show()
    '''
    def saveAirfoil(name):
        with open(f'{name}.txt','w') as file:
            for i in range(len(pupx)-1,-1,-1): # começando no borda de fuga
                file.write('{0:2.4f}  {1:2.4f} \n'.format(pupx[i],pupy[i]))
            for i in range(len(pdownx)): # terminando no borda de fuga
                file.write('{0:2.4f}  {1:2.4f} \n'.format(pdownx[i],pdowny[i]))
 
    saveAirfoil('airfoilTeste')
    airfoilData = []
    with open(r'Xfoil/airfoil_01.dat','r') as file:
        lines = file.readlines()
        for line in lines:
            xairfoil, yairfoil = line.split()
            airfoilData.append([float(xairfoil), float(yairfoil)])
    airfoilData = np.array(airfoilData)
    
    
    def distancia(pontosControle, airfoil = airfoilData):
        """
        Parametros:
        pontoControle[0:6] :  upx 
        pontoControle[6:12] :  upy 
        pontoControle[12:18] :  downx 
        pontoControle[18:24] :  downy 

        """
        
        # fixando dois pontos de controle no BA e um no BF
        pontosControle = [0]*24
        # Borda de ataque
        
        pontosControle[0] = 0.0 # upx
        pontosControle[6] = 0.0 #upy
        pontosControle[12] = 0.0 #downx
        pontosControle[18] = 0.0 #downy

        # Bordad de fuga
        pontosControle[5] = 1.0 #upx
        pontosControle[11] = 0.0 #upy
        pontosControle[17] = 1.0 #downx
        pontosControle[23] = 0.0 #downy

        pontosControle[1:5] = pontosC[0:4]
        pontosControle[7:11] = pontosC[4:9]
        pontosControle[13:17] = pontosC[9:13]
        pontosControle[19:23] = pontosC[13:17]
        
        
        pupx  = Bezier.polinomio(pontosControle[0:6] ,n)
        pupy  = Bezier.polinomio(pontosControle[6:12] ,n)
        pdownx = Bezier.polinomio(pontosControle[12:18] ,n)
        pdowny = Bezier.polinomio(pontosControle[18:24] ,n)
        
        xpara = pupx[::-1].copy()
        xpara.extend(pdownx[1::])

        ypara = pupy[::-1].copy()
        ypara.extend(pdowny[1::])
        para = []
        para.extend([xpara,ypara])
        para = np.asarray(para)

        try:
            A = 1000 * np.sum(abs(para[0,:] - airfoil[:,0]) + abs(para[1,:] - airfoil[:,1]))
            print(A)
            return A
        except:
            return 10**9

    #upx,upy,downx,downy
    #x0 = [0,0.25,0.5,0.75,0.05,0.2,0.15,0.1,0,0.25,0.5,0.75,-0.05,-0.1,0.10,0.05]
    x0 = upx.copy()
    x0.extend(upy)
    x0.extend(downx)
    x0.extend(downy)    
    
    
    res = minimize(distancia, x0, method='Powell', tol=1e-6, options={'disp': True, 'maxiter':100})
    print(res.fun)
    print(res.values)
    print(res.x)
    Controle = res.x
    

    #print(distancia([upx,upy,downx,downy]))
    pontosControle1 = [0]*24
    # Borda de ataque
    
    pontosControle1[0] = 0.0 # upx
    pontosControle1[6] = 0.0 #upy
    pontosControle1[12] = 0.0 #downx
    pontosControle1[18] = 0.0 #downy

    # Bordad de fuga
    pontosControle1[5] = 1.0 #upx
    pontosControle1[11] = 0.0 #upy
    pontosControle1[17] = 1.0 #downx
    pontosControle1[23] = 0.0 #downy

    pontosControle1[1:5] = Controle[0:4]
    pontosControle1[7:11] = Controle[4:9]
    pontosControle1[13:17] = Controle[9:13]
    pontosControle1[19:23] = Controle[13:17]


    



    pupxf  = Bezier.polinomio(Controle[0:6] ,n)
    pupyf  = Bezier.polinomio(Controle[6:12] ,n)
    pdownxf = Bezier.polinomio(Controle[12:18] ,n)
    pdownyf = Bezier.polinomio(Controle[18:24] ,n)

    plt.figure()

    #plt.plot(upx,upy,'or')
    #plt.plot(downx,downy,'ob')
    plt.plot(pupxf,pupyf,'r')
    plt.plot(pdownxf,pdownyf,'b')

    plt.show()


    '''