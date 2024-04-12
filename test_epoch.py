
from model.MODEL import model
import numpy as np
import warnings

warnings.filterwarnings('ignore')

seed = np.random.randint(1000000)
print(seed)
seed = 180673
# 1101 il contagio si ferma

#mod.par.a1_reductionPerc = 0.99


infetion_sum = []

epsilon_RL = 0.2

for i in range(0, 200):
    
    seed = np.random.randint(1000000)
    mod = model(seed)
    mod.par.draw_conclusions = False

    if i == 0:
        mod.par.clear_q_table_memory = True
    else:
        mod.par.clear_q_table_memory = False
    if i < 125: epsilon_RL += 0.8 / 125
    mod.par.RL_PM_t_min = 0
    mod.par.epsilon_RL = epsilon_RL
    if i == 99 :
        mod.par.draw_conclusions = True
        print(mod.par.epsilon_RL)
    mod.run(seed)

    infetion_sum.append(sum(mod.gv.contagious_history))

    print(f'Run {i + 1} / 200 excecuted')


arr_x = []
for i in range(1, len(infetion_sum) + 1):
    arr_x.append(i)

import matplotlib.pyplot as plt

plt.plot(arr_x, infetion_sum)
plt.show()