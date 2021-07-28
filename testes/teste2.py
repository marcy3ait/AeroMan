import numpy as np

def area(point1,point2,point3):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    x3 = point3[0]
    y3 = point3[1]
    aux1 = x2 - x1
    aux2 = y3 - y1
    aux3 = x3 - x1
    aux4 = y2 - y1

    return 0.5*(aux1*aux2 - aux3*aux4)

def valida(A):
    # valido somente para n par
    A = np.array(A)
    n = len(A) #numero de pontos
    m = n//2
    A_up = A[0:m,:]
    A_down = A[m:,:]
    controle = 1
    
    for i in range(m):
        
        if i+1 < n//2:
            print(i, i+1,m-1-i)
            valor = area( A_up[i], A_up[i+1],A_down[m-1-i] )
        else:
            print(i-1, i,m-1-i)
            valor = area( A_up[i-1],A_up[i],A_down[m-1-i] )

        # verificando a area
        if valor<0:
            controle = -1
            break
        

    return controle

AA = [[ 9.71550359e-01,  2.91322978e-03],
    [ 7.75248631e-01,  1.91806421e-02],
    [ 3.64153844e-01,  4.08603881e-02],
    [ 4.97872062e-02,  2.83040461e-02],
    [ 3.53474364e-07, -1.41520231e-02],
    [ 2.31863952e-01, -4.16582287e-02],
    [ 6.35846184e-01, -2.96215949e-02],
    [ 9.43100719e-01, -5.82645955e-03]]

controle= valida(AA)
print(controle)
