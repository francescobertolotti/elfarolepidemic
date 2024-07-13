
from model.global_vars import glob_vars
from model.parameters import *
import matplotlib.pyplot as plt


par = parameters()
g_v = glob_vars(par)

arr_1 = [100, 200, 300, 250, 400, 550, 600, 700, 675, 750, 700, 800, 900, 875, 925]

res_arr = g_v.regLine(par, [100, 200, 300, 250, 400, 550, 600, 700, 675, 750, 700, 800, 900, 875, 925], par.RL_PM_t_min * 2)

print(len(res_arr), len(arr_1))
print(res_arr)
print(arr_1)

plt.plot(res_arr)
plt.plot(arr_1)
plt.show()