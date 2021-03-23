import numpy as np
import matplotlib.pyplot as plt

class BezierControl:

    ''' Classe que gera os pontos de controle [A] do aerofólio partindo das coordenadas do aerofólio inicial '''

    def __init__(self, coord):

        self.Points = self._ajusteAmostra(coord)
        self.A, self.B = self._get_bezier_coef(self.Points)

    def _ajusteAmostra(self, coord, n = 11, cos=True): 

        '''
        Dado um conjunto de pontos [coord] obtem os coeficentes de Bezie e ajusta um aerofolio com [n] pontos.

        Parametros:
        coord : conjunto inicial de coordenadas para ajuste
        n : numero final para o ajuste
        cos: concentração de pontos na Borda de ataque
        '''

        # cria um novo vetor de n pontos com x e y
        xy2 = np.zeros((n,2))

        # Cria as coordenadas x do novo aerofólio

        if (cos==True):
            # concentra pontos na extremidade usando função cosseno
            theta = np.linspace(0.0,2*np.pi,n)
            xy2[:,0] = np.cos(theta)*0.5+0.5
        else:   
            #igualmente espaçado
            xy2[:,0] = np.abs(np.linspace(1.0,-1.0,n))
        
        # checa o sentido de rotação do aerofólio
        # caso esteja no sentido horário inverte a ordenação
        dydx = (coord[1,1]- coord[0,1])/(coord[1,0]- coord[0,0])
        # se a derivada for menor q zero -> anti-horario
        if (dydx>0.0):
            coord[:,0] = coord[::-1,0]
            coord[:,1] = coord[::-1,1]    

        # interpola novos pontos a curva
        coord = self._evaluate_bezier(coord, 5)
        m = coord.shape[0] # numero de curvas de bezier

        # encontra o ponto mais próximo e adiciona ao novo vetor
        jj = 1
        for i in range(1,n-1): 
            for j in range(jj,m-1): # varre todas as curvas de bezier

                # calcula a distância até os pontos x[j] e x[j-1]
                dist0 = np.abs(xy2[i,0] -  coord[j-1,0])
                dist  = np.abs(xy2[i,0] -  coord[j,0])

                if (dist > dist0):
                    xy2[i,:] = coord[j-1,:]
                    dist0 = dist
                    jj = j 
                    break

        xy2[0,:] = coord[0,:]
        xy2[n-1,:] = coord[coord.shape[0]-1,:]

        return xy2

    # find the a & b points
    def _get_bezier_coef(self, points):
        # since the formulas work given that we have n+1 points
        # then n must be this:
        n = len(points) - 1

        # build coefficents matrix
        C = 4 * np.identity(n)
        np.fill_diagonal(C[1:], 1)
        np.fill_diagonal(C[:, 1:], 1)
        C[0, 0] = 2
        C[n - 1, n - 1] = 7
        C[n - 1, n - 2] = 2

        # build points vector
        P = [2 * (2 * points[i] + points[i + 1]) for i in range(n)]
        P[0] = points[0] + 2 * points[1]
        P[n - 1] = 8 * points[n - 1] + points[n]

        # solve system, find a & b
        A = np.linalg.solve(C, P)
        B = np.zeros((n,2))
        for i in range(n - 1):
            B[i,:] = 2 * points[i + 1] - A[i + 1]
        B[n - 1,:] = (A[n - 1] + points[n]) / 2

        return A, B

    # returns the general Bezier cubic formula given 4 control points
    def _get_cubic(self, a, b, c, d):
        return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * t * b + 3 * (1 - t) * np.power(t, 2) * c + np.power(t, 3) * d

    # return one cubic curve for each consecutive points
    def _get_bezier_cubic(self, points):
        A, B = self._get_bezier_coef(points)
        return [
            self._get_cubic(points[i], A[i], B[i], points[i + 1])
            for i in range(len(points) - 1)
        ]

    # evalute each cubic curve on the range [0, 1] sliced in n points
    def _evaluate_bezier(self, points, n):
        curves = self._get_bezier_cubic(points)
        return np.array([fun(t) for fun in curves for t in np.linspace(0, 1, n)])


'''
def naca(number,n):

    m = float(number[0])/100.0
    p = float(number[1])/10.0
    t = float(number[2:])/100.0

    # coeficientes da equação
    t = t/100.0
    p = p/10.0
    m = m/100.0    

    a0 = +0.2969
    a1 = -0.1260
    a2 = -0.3516
    a3 = +0.2843
    a4 = -0.1015 # bordo de fuga espesso
    # a4 = -0.1036 # bordo de fuga colapsado

    coord = np.zeros((n,2))

    # concentra pontos nas extremidades usando uma função cosseno
    theta  = np.linspace(0.0,2*np.pi,n)
    coord[:,0] = np.cos(theta)*0.5+0.5


    # função sinal indentifica se estamos no intradorso ou extradorso
    side = np.where(theta>np.pi,-1,1)

    # yt
    coord[:,1] = -t/0.2*(a0*np.sqrt(coord[:,0]) + a1*coord[:,0] + a2*coord[:,0]**2 + a3*coord[:,0]**3 + a4*coord[:,0]**4)
    coord[:,1] = side*coord[:,1]
    
    if (p>0):
        # camber
        yc1 = m/    p**2 * (           2*p* coord[:,0] - coord[:,0]**2 ) # 0  < x < pc
        yc2 = m/(1-p)**2 * ( (1-2*p) + 2*p* coord[:,0] - coord[:,0]**2 ) # pc < x < c

        yc = np.where(np.abs(coord[:,0])>p,yc2,yc1)

        f1 = 2*m/p**2    *(p-coord[:,0]) # 0  < x < pc
        f2 = 2*m/(1-p)**2*(p-coord[:,0]) # pc < x < c

        dydx = np.where(np.abs(coord[:,0])<p,f2,f1)

        theta = np.arctan(dydx)


        coord[:,0] = coord[:,0] - coord[:,1]*np.sin(theta)#*side
        coord[:,1] = yc      + coord[:,1]*np.cos(theta)#*side

    return coord

def ReadAirfoil(name):

  num_lines = sum(1 for line in open(name))
  var  = np.zeros((num_lines,2))
    
  file1 = open(name,"r")
  for i in range(num_lines):
    dummy = file1.readline()
    pair = dummy.split()
    for j in range(2):
       var[i,j] =float(pair[j])
  
  file1.close()
  return var

'''

if __name__ == "__main__":
    import bezie_1 as bz1
    def naca00xx(t,n):
        # naca 0012
        # t = 12  # dois últimos digitos do naca (série 4 digitos)
        # n = 30  # número de pontos

        # coeficientes da equação
        a0 = +0.2969
        a1 = -0.1260
        a2 = -0.3516
        a3 = +0.2843
        a4 = -0.1015 # bordo de fuga espesso
        a4 = -0.1036 # bordo de fuga colapsado

        coord = np.zeros((n,2))

        # concentra pontos nas extremidades usando uma função cosseno
        theta  = np.linspace(0.0,2*np.pi,n)
        coord[:,0] = np.cos(theta)*0.5+0.5

        # função sinal: indentifica se estamos no intradorso ou extradorso
        side = np.where(theta>np.pi,-1,1)

        t = t/100.0
        coord[:,1] = -t/0.2*(a0*np.sqrt(coord[:,0]) + a1*coord[:,0] + a2*coord[:,0]**2 + a3*coord[:,0]**3 + a4*coord[:,0]**4)
        coord[:,1] = side*coord[:,1]

        return coord
    naca0012 = naca00xx(8,40)
    geraCoef = BezierControl(naca0012)
    
    parametrizacao = bz1.BezierCoord(geraCoef.A)
    coordParametrizadas = parametrizacao._getCoord()
    plt.plot(naca0012[:,0],naca0012[:,1],'-k', label = 'Airfoil nao parametrizado')
    plt.plot(coordParametrizadas[:,0],coordParametrizadas[:,1],'--r', label = 'Airfoil parametrizado')

    naca0012 = naca00xx(12,40)
    geraCoef = BezierControl(naca0012)
    parametrizacao = bz1.BezierCoord(geraCoef.A)
    print(geraCoef.A)
    coordParametrizadas = parametrizacao._getCoord()
    plt.plot(naca0012[:,0],naca0012[:,1],'-g', label = 'Airfoil nao parametrizado')
    #plt.plot(coordParametrizadas[:,0],coordParametrizadas[:,1],'--r', label = 'Airfoil parametrizado')
    plt.legend()
    plt.show()