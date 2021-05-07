
import sys
from pathlib import Path


if str(Path(Path().absolute())).split('\\')[-1] == 'AeroMan':
    path = str(Path(Path().absolute())) + r'\xfoil'
else:
    path = str(Path(Path().absolute().parents[0])) + r'\xfoil'

sys.path.insert(1, path)

import xfoil as xf

def fitness(pontosControle):

    #geraCoordenadas()

    #rodarXfoil()

    # cl max 
    # menor arrasto para aoa fixo
    # l/d


    pass