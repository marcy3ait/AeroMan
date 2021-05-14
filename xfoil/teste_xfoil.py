import os
import numpy as np
import subprocess as sp

name = "airfoil_geracao_10.txt"
path = r'xfoil.exe < ' + name
print(path)
print(path.split())
process = sp.Popen(path.split(), stdout = sp.PIPE, shell = True)
out, err = process.communicate()

print(err)
print(out)