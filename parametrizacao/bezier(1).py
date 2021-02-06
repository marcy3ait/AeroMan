import numpy as np
import matplotlib.pyplot as plt

# find the a & b points
def get_bezier_coef(points):
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
def get_cubic(a, b, c, d):
    return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * t * b + 3 * (1 - t) * np.power(t, 2) * c + np.power(t, 3) * d

# return one cubic curve for each consecutive points
def get_bezier_cubic(points):
    A, B = get_bezier_coef(points)
    return [
        get_cubic(points[i], A[i], B[i], points[i + 1])
        for i in range(len(points) - 1)
    ]

# evalute each cubic curve on the range [0, 1] sliced in n points
def evaluate_bezier(points, n):
    curves = get_bezier_cubic(points)
    return np.array([fun(t) for fun in curves for t in np.linspace(0, 1, n)])




def findP(A,B,xy0,xyn):
    
    n = A.shape[0]+1
    p = np.zeros((n,2))
    
    p[0,:] = xy0[:]
    p[n-1,:] = xyn[:]

    p[1,:] = A[0,:] + (A[1,:]-p[0,:])*0.5
    for i in range(1,n-2):
        p[i+1,:] = (A[i-1,:] + 4*A[i,:] + A[i+1,:] - 4*p[i,:])*0.5 

    p[n-2,:] = (2*A[n-3,:]+ 7*A[n-2,:] - p[n-1,:])/8.0
    p[n-1,:] = xyn[:]
    print(xyn[:])
    return p



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

    xy = np.zeros((n,2))

    # concentra pontos nas extremidades usando uma função cosseno
    theta  = np.linspace(0.0,2*np.pi,n)
    xy[:,0] = np.cos(theta)*0.5+0.5

    # função sinal: indentifica se estamos no intradorso ou extradorso
    side = np.where(theta>np.pi,-1,1)

    t = t/100.0
    xy[:,1] = -t/0.2*(a0*np.sqrt(xy[:,0]) + a1*xy[:,0] + a2*xy[:,0]**2 + a3*xy[:,0]**3 + a4*xy[:,0]**4)
    xy[:,1] = side*xy[:,1]

    return xy


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

    xy = np.zeros((n,2))

    # concentra pontos nas extremidades usando uma função cosseno
    theta  = np.linspace(0.0,2*np.pi,n)
    xy[:,0] = np.cos(theta)*0.5+0.5


    # função sinal indentifica se estamos no intradorso ou extradorso
    side = np.where(theta>np.pi,-1,1)

    # yt
    xy[:,1] = -t/0.2*(a0*np.sqrt(xy[:,0]) + a1*xy[:,0] + a2*xy[:,0]**2 + a3*xy[:,0]**3 + a4*xy[:,0]**4)
    xy[:,1] = side*xy[:,1]
    
    if (p>0):
        # camber
        yc1 = m/    p**2 * (           2*p* xy[:,0] - xy[:,0]**2 ) # 0  < x < pc
        yc2 = m/(1-p)**2 * ( (1-2*p) + 2*p* xy[:,0] - xy[:,0]**2 ) # pc < x < c

        yc = np.where(np.abs(xy[:,0])>p,yc2,yc1)

        f1 = 2*m/p**2    *(p-xy[:,0]) # 0  < x < pc
        f2 = 2*m/(1-p)**2*(p-xy[:,0]) # pc < x < c

        dydx = np.where(np.abs(xy[:,0])<p,f2,f1)

        theta = np.arctan(dydx)


        xy[:,0] = xy[:,0] - xy[:,1]*np.sin(theta)#*side
        xy[:,1] = yc      + xy[:,1]*np.cos(theta)#*side

    return xy




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



def AjusteAmostra(xy,n,cos=True): 

    '''
    Parametros:
    xy : conjunto inicial de coordenadas para ajuste
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
    dydx = (xy[1,1]- xy[0,1])/(xy[1,0]- xy[0,0])
    # se a derivada for menor q zero -> anti-horario
    if (dydx>0.0):
        xy[:,0] = xy[::-1,0]
        xy[:,1] = xy[::-1,1]    

    # interpola novos pontos a curva
    xy = evaluate_bezier(xy, 5)
    m = xy.shape[0] # numero de curvas de bezier

    
    # encontra o ponto mais próximo e adiciona ao novo vetor
    jj = 1
    for i in range(1,n-1): 
        for j in range(jj,m-1): # varre todas as curvas de bezier

            # calcula a distância até os pontos x[j] e x[j-1]
            dist0 = np.abs(xy2[i,0] -  xy[j-1,0])
            dist  = np.abs(xy2[i,0] -  xy[j,0])

            if (dist > dist0):
                xy2[i,:] = xy[j-1,:]
                dist0 = dist
                jj = j 
                break

    xy2[0,:] = xy[0,:]
    xy2[n-1,:] = xy[xy.shape[0]-1,:]

    return xy2





# exemplo 
# le o perfil com 81 pontos
#xy  = ReadAirfoil(r'C:/Users/marcy/Desktop/TCC/AeroMan/parametrizacao/selig1223.dat')
xy = naca00xx(10,40)

# reduz a quantidade de pontos para 11 usando bezier
xy2 = AjusteAmostra(xy,11)

# Calcula o novo aerofolio usando apenas 11 pontos e 10 pontos de controle(ai, demodo q bj depende de ai)
path = evaluate_bezier(xy2, 50)
A, B = get_bezier_coef(xy2)
print(A)

plt.plot(xy[:,0] , xy[:,1], '-',label="aerofólio de entrada P=81")
plt.plot(path[:,0], path[:,1], '--',label="aerofólio novo interpolado com P=11")
plt.plot(xy2[:,0], xy2[:,1], 'o',label="P novo")
plt.plot(A[:,0], A[:,1], 'xr',label="A novo")
plt.plot(B[:,0], B[:,1], 'xb',label="B novo")
plt.axis('equal')
plt.legend(loc=4)
plt.xlabel("x/c",fontsize=15)
plt.ylabel("y/c",fontsize=15)

plt.show()












# calcula a geometria dos perfis
points1 = naca00xx(10,11)
points2 = naca00xx(18,11)
# points1 = naca('0012',11)
# points2 = naca('2412',11)

# encontra os coeficientes das curvas de Bezier
A1, B1 = get_bezier_coef(points1)
A2, B2 = get_bezier_coef(points2)

# interpola coeficientes
A3 = (A1 + A2)*0.5
B3 = (B1 + B2)*0.5
n = points1.shape[0]

# condição de contorno
xy0 = (points1[0,:]   + points2[0,:]  )*0.5
xyn = (points1[n-1,:] + points2[n-1,:])*0.5


# Recalcula os pontos para os coeficientes interpolados
points3 =  findP(A3,B3,xy0,xyn)



# traça uma curva entre os pontos interpolados usando 50 pontos para cada seguimento
path = evaluate_bezier(points3, 50)

# separando as coordenadas
x1, y1 = points1[:,0], points1[:,1]
x2, y2 = points2[:,0], points2[:,1]
x3, y3 = points3[:,0], points3[:,1]
px, py = path[:,0],    path[:,1]



plt.figure(figsize=(11, 8))
plt.subplot(2,1,1)
# plt.plot(px, py, 'b-')
plt.plot(x1, y1, 'C1-o',label="geo 1")
# plt.plot(x2, y2, 'C2-o',label="geo 2")
plt.plot(A3[:,0], A3[:,1], 'C1x',label="A")
plt.plot(B3[:,0], B3[:,1], 'C2x',label="B")
# plt.plot(x3, y3, 'C3-o',label="geo nova")
plt.legend(loc=4)
plt.axis('equal')
# plt.xlabel("x/c",fontsize=15)
plt.ylabel("y/c",fontsize=15)

plt.subplot(2,1,2)
plt.plot(px, py, 'b-',label="interpolado")
plt.plot(A3[:,0], A3[:,1], 'C1x',label="A")
plt.plot(B3[:,0], B3[:,1], 'C2x',label="B")
plt.plot(x3, y3, 'C3o',label="P")
plt.axis('equal')
plt.legend(loc=4)
plt.xlabel("x/c",fontsize=15)
plt.ylabel("y/c",fontsize=15)

plt.show()
