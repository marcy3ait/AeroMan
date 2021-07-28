#%%
import numpy as np
import matplotlib.pyplot as plt

class BezierCoord:

    ''' Classe que gera as coordenadas do aerofólio partindo dos pontos de controle [A] '''
    # não resolve-se o sistema aqui

    def __init__(self, A, name = 'airfoils_bezie_coord'):

        self.name = name
        self.A_ = np.array(A)
        self.Points = self.findPoints()
        self.B_ = self.calcB()

    def calcB(self):

        ''' Calcula os pontos de controle [B] partindo do [A] '''

        n = self.A_.shape[0] +1 # n

        B = np.zeros((n-1,2))

        
        for i in range(n-2):
            B[i,:] = 2*self.Points[i+1,:] - self.A_[i+1,:]

        B[n-2,:] = 0.5*(self.A_[n-2] + self.Points[n-1])
        

        return B

    def findPoints(self,xy0 = [1.0, 0.0], xyn = [1.0, 0.0]):

        ''' Calcula-se as coordenadas do aerfólio partindo dos pontos de controle [A] '''
    
        n = self.A_.shape[0] + 1 # n da formulação matematica
        p = np.zeros((n,2))
        
        p[0,:] = xy0[:]
        p[n-1,:] = xyn[:]

        p[1,:] = self.A_[0,:] + (self.A_[1,:]-p[0,:])*0.5
        for i in range(1,n-2):
            p[i+1,:] = (self.A_[i-1,:] + 4.*self.A_[i,:] + self.A_[i+1,:] - 4*p[i,:])*0.5 

        p[n-2,:] = (2*self.A_[n-3,:]+ 7.*self.A_[n-2,:] - p[n-1,:])/8.0
        return p

    def _get_cubic(self, a, b, c, d):
        return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * t * b + 3 * (1 - t) * np.power(t, 2) * c + np.power(t, 3) * d
    
    def _get_bezier_cubic(self):
        return [
            self._get_cubic(self.Points[i], self.A_[i], self.B_[i], self.Points[i + 1])
            for i in range(len(self.Points) - 1)
        ]

    # evalute each cubic curve on the range [0, 1] sliced in n points
    def _evaluate_bezier(self, n = 10):
        curves = self._get_bezier_cubic()
        return np.array([fun(t) for fun in curves for t in np.linspace(0, 1, n)])
    
    def _getCoord(self):
        return self._evaluate_bezier()
    
    def saveCoord(self):
        coord = self._getCoord()
        
        with open(f'coord_{self.name}.txt', 'w') as file:
            for line in range(0,len(coord)):
                file.write(" %1.6f    %1.6f\n" %(coord[line,0],coord[line,1]))



        
    
        
   
if __name__ == "__main__":
   
    AA = [[ 9.71550359e-01,  2.91322978e-03],
       [ 7.75248631e-01,  1.91806421e-02],
       [ 3.64153844e-01,  4.08603881e-02],
       [ 4.97872062e-02,  2.83040461e-02],
       [ 3.53474364e-07, -1.41520231e-02],
       [ 2.31863952e-01, -4.16582287e-02],
       [ 6.35846184e-01, -2.96215949e-02],
       [ 9.43100719e-01, -5.82645955e-03]]
            
    coord_airfooil = BezierCoord(AA)
    coord_airfooil.saveCoord()
  
    pontosP = coord_airfooil.Points
    print(pontosP[:,0])
    print(pontosP[:,1])
  
    coord = coord_airfooil._getCoord()
    plt.plot(coord[:,0], coord[:,1], '--k')
    plt.plot(coord_airfooil.Points[:,0], coord_airfooil.Points[:,1], 'Xg', label ='p')
    #plt.plot(coord_airfooil.A_[:,0], coord_airfooil.A_[:,1], 'xr', label = 'Pontos de controle A',)
    #plt.plot(coord_airfooil.B_[:,0], coord_airfooil.B_[:,1],  'ok', label = 'Pontos de controle B',)
    AA = np.array(AA)
    plt.plot(AA[:,0], AA[:,1],'or')

    plt.legend()
    plt.show()
    
# %%
