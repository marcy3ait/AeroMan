def leitura(path, inicio, fim, coluna):
    f = open(path,'r')
    lines = f.readlines()
    rows = []
    for line in range(inicio,fim): 
        rows.append(lines[line].strip().split()[coluna])
    

    return rows

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np
    plt.figure('Método comparativo - VLM')
    path = r'C:\Users\marcy\Desktop\TCC\AeroMan\avl\saida2.txt'
    inicio = 20
    fim = 49
    coluna = 7
    saida_cl1 = leitura(path, inicio, fim, 7)
    saida_x1 = leitura(path, inicio, fim, 1)
    saida_x2 = leitura(path, 64, 93, 1)
    saida_cl2 = leitura(path, 64, 93, 7)
    saida_x1 = np.array(saida_x1,dtype=float)
    saida_x2 = np.array(saida_x2,dtype=float)
    saida_cl1 = np.array(saida_cl1,dtype=float)
    saida_cl2 = np.array(saida_cl2,dtype=float)
    plt.plot(saida_x1,saida_cl1, 'r')
    plt.plot(saida_x2,saida_cl2,'r', label = 'avl')

    #xflr5 - vlm1
    path = r'C:\Users\marcy\Desktop\TCC\AeroMan\avl\validacao\MainWing_a=3.00_v=10.00ms.txt'
    x = leitura(path, 22,59,0)
    cl = leitura(path, 22,59,3)
    x = np.array(x, dtype=float)
    cl = np.array(cl, dtype=float)
    #xflr5 - vlm2
    path = r'C:\Users\marcy\Desktop\TCC\AeroMan\avl\validacao\MainWing_a=3.00_v=10.00ms_vlm2.txt'
    x2 = leitura(path, 22,59,0)
    cl2 = leitura(path, 22,59,3)
    x2 = np.array(x2, dtype=float)
    cl2 = np.array(cl2, dtype=float)
    #print(x)
    #print(cl)
    plt.plot(x,cl,'--b',label = 'xflr5 (VLM1)')
    plt.plot(x2,cl2,'--g',label = 'xflr5 (VLM2)')
    plt.xlabel('Envergadura [m] ')
    plt.ylabel('CL')
    plt.legend()
    plt.grid()

    plt.figure('Comparação')

    #xflr5 - llt
    path = r'C:\Users\marcy\Desktop\TCC\AeroMan\avl\validacao\MainWing_a=3.00_v=10.00ms_llt.txt'
    x3 = leitura(path, 22,40,0)
    cl3 = leitura(path, 22,40,3)
    x3= np.array(x3, dtype=float)
    cl3 = np.array(cl3, dtype=float)

    #xflr5 - paineis
    path = r'C:\Users\marcy\Desktop\TCC\AeroMan\avl\validacao\MainWing_a=3.00_v=10.00ms_paineis.txt'
    x4 = leitura(path, 22,59,0)
    cl4 = leitura(path, 22,59,3)
    x4 = np.array(x4, dtype=float)
    cl4 = np.array(cl4, dtype=float)

    plt.plot(saida_x1,saida_cl1, 'r')
    plt.plot(saida_x2,saida_cl2,'r', label = 'avl')
    plt.plot(x,cl,'--b',label = 'xflr5 (VLM1)')
    plt.plot(x2,cl2,'--g',label = 'xflr5 (VLM2)')
    plt.plot(x3,cl3,'--k',label = 'xflr5 (LLT)')
    plt.plot(x4,cl4,'--m',label = 'xflr5 (PAINEIS)')
    plt.xlabel('Envergadura [m] ')
    plt.ylabel('CL')
    plt.legend()
    plt.grid()

    
    plt.show()
        