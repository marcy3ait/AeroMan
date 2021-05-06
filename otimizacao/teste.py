import random
import matplotlib.pyplot as plt

lim_inf = 0.3
lim_sup = 0.7

plt.figure()
for i in range(100):   
    plt.plot(i,random.uniform(lim_inf,lim_sup), 'or')

plt.grid()
plt.show()
