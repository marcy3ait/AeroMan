from scipy.optimize import minimize
import matplotlib.pyplot as plt 
import numpy as np


class Bezier:

    ''' Classe usada para parametrização com base nos pontos de controle  - 
    Bezier composto usando um polinomio quadratico.
    
    
    '''

    def __init__(self, x_coor, pts_control):
        self.x_coord = x_coor
        self.pts_control = self.get_control(pts_control)
    

    def bezier2N(self,t,points):

        '''
        Parametros
        
        points: pontos de controle (3 pontos -> Bezier quadrada)
        t: variação de zero a um conforme o numero de pontos da parametrização 

        '''
        
        #B_x=(1-t)*((1-t)*points[0][0]+t*points[1][0])+t*((1-t)*points[1][0]+t*points[2][0])
        B_y=(1-t)*((1-t)*points[0][1]+t*points[1][1])+t*((1-t)*points[1][1]+t*points[2][1])

        return B_y

    def parametriza(self):

        curva = []
        total_pts = len(self.pts_control)
        for i in range(0, total_pts-1):

            # primeira curva
            if i == 0:

                x_meio = (self.pts_control[1][0] + self.pts_control[2][0])/2
                y_meio = (self.pts_control[1][1] + self.pts_control[2][1])/2

                x_ord = sorted(self.x_coord[np.where(self.x_coord > x_meio)], reverse=True)
                t_bezier = [self.get_t(index, [self.pts_control[0], self.pts_control[1], [x_meio, y_meio]]) for index in x_ord]

                y_bezier = self.bezier2N(np.asarray(t_bezier),  [self.pts_control[0], self.pts_control[1], [x_meio, y_meio]])
                curva.append(self.pts_control[0]) 
                curva = curva+list(zip(x_ord,y_bezier))

            # curvas do meio
            if i >=1 and i < total_pts-3:
                x_meio1 = (self.pts_control[i][0] + self.pts_control[i+1][0])/2
                y_meio1 = (self.pts_control[i][1] + self.pts_control[i+1][1])/2
                
                x_meio2 = (self.pts_control[i+1][0] + self.pts_control[i+2][0])/2
                y_meio2 = (self.pts_control[i+1][1] + self.pts_control[i+2][1])/2

                if x_meio1 > x_meio2: # extradorso
                    x_ord = sorted(self.x_coord[(self.x_coord > x_meio2) & (self.x_coord <= x_meio1)], reverse= True)
                
                if x_meio1 < x_meio2: # intradorso
                    x_ord = sorted(self.x_coord[(self.x_coord < x_meio2) & (self.x_coord >= x_meio1)], reverse= False)


                t_bezier = [self.get_t(index, [[x_meio1,y_meio1], self.pts_control[i+1], [x_meio2, y_meio2]]) for index in x_ord]

                y_bezier = self.bezier2N(np.asarray(t_bezier), [[x_meio1,y_meio1], self.pts_control[i+1], [x_meio2, y_meio2]])
                curva = curva+list(zip(x_ord,y_bezier))

            # curva final 
            if i == total_pts - 2:
                x_meio = (self.pts_control[-3][0] + self.pts_control[-2][0])/2
                y_meio = (self.pts_control[-3][1] + self.pts_control[-2][1])/2

                x_ord = sorted(self.x_coord[self.x_coord > x_meio], reverse=False)
                t_bezier = [self.get_t(index, [[x_meio, y_meio], self.pts_control[-2], self.pts_control[-1]]) for index in x_ord]

                y_bezier = self.bezier2N(np.asarray(t_bezier),  [[x_meio, y_meio], self.pts_control[-2], self.pts_control[-1]])
                curva = curva+list(zip(x_ord,y_bezier))
                curva.append(self.pts_control[-1])


        return curva



    def get_t(self, x, points):

        ''' resolve a eq. B_x para obter t dado as coord x. '''

        a = points[0][0]
        b = points[1][0]
        c = points[2][0]

        delta = abs(b**2-a*c+a*x+c*x-2*b*x)
        t0 = ((a-b) + np.sqrt(delta))/(a+c-2*b)
        t1 = ((a-b) - np.sqrt(delta))/(a+c-2*b)

        root = np.array([t0, t1])
        t = root[np.where((np.abs(root) <= 1.0001) & (np.abs(root) >= 0.0))][0]

        if t>1:
            t=1

        return t

    def get_control(self,points):

        ''' pontos de controle - 13 GDL (pensar em como inserir restrições construtivas) '''

        tick = 0.0015
        te_top = [1, tick]
        te_bot = [1, -tick]
        le = 0
        le_rad = points[0]

        control = [
            te_top, # fixo
            [points[1],points[2]],
            [points[3],points[4]],
            [points[5],points[6]],
            [le,le_rad],
            [le,-le_rad],
            [points[7],points[8]],
            [points[9],points[10]],
            [points[11],points[12]],
            te_bot # fixo
        ]

        return control

if __name__ == '__main__':
    airfoil = []
    with open(r'airfoil_01.dat') as airfoil_dat:
        for index, row in enumerate(airfoil_dat.readlines()):
            x, y = row.strip().split()
            airfoil.append([float(x),float(y)])

    airfoil = np.asarray(airfoil)


    x_pts = np.linspace(0,0.99,len(airfoil))
    print(len(airfoil))
    inicial_airfoil = [0.03, 0.76, 0.08, 0.48, 0.13, 0.15, 0.12, 0.15, -0.08, 0.37, -0.01, 0.69, 0.04]
    
    def shape(controle_pts, x_pts = x_pts, ta =  airfoil):

        ''' Função usada para obter os pontos de controle dado um aerofolio  - minimizando essa função de custo'''
        para = Bezier(x_pts,controle_pts)

        control = np.array(para.parametriza())
        a = 0
        for i in range(min([len(ta),len(control)])):
            
            a += 1000*(abs(control[i,0] - ta[i,0]) + abs(control[i,1] - ta[i,1]))
        return a
    
    res = minimize(shape, inicial_airfoil, method = 'Powell', tol = 1e-10, options={'disp': True, 'maxiter': 10000 })
    print(res.x)
    matched_airfoil = np.array(Bezier(x_pts, res.x).parametriza())
    print(matched_airfoil)
    x1,y1 = zip(*matched_airfoil)
    fig, ax = plt.subplots(figsize=(14,5))
    plt.plot(x1, y1, label='final')

    ax.set_aspect('equal')
    plt.ylim(-0.15,0.15)
    plt.legend()
    plt.show()
    