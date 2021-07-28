
import subprocess as sp
import threading
from multiprocessing import Process 

def infinity():
    i = 0
   
    while True:
        print(f'saida{i}')
        i+=1


if __name__ == '__main__':
    
    acao = Process(target = infinity)
    acao.start()
    acao.join(timeout=5)
    acao.terminate()
    #sp.call(['python', 'teste2.py'], timeout=0.1, shell=True)
