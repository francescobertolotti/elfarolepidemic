# TO-DO LIST

# COSE DA GGIUNGERE
# 0) testare altre strategie decisionali per gli agenti

from joblib import Parallel, delayed
from model.parameters import *
from model.global_vars import *
from model.person import *
from model.setup import *
from model.go import *
from model.conclusion import *
import numpy as np
from model.policy_maker import *

class model():
    def __init__(self, my_seed):
        
        random.seed(my_seed)
        np.random.seed(seed=my_seed)

        self.qTable = np.zeros([2,4])


        self.al = agents_list()
        self.par = parameters()
        self.gv = glob_vars(self.par)
        self.pm = PM(self.par)

    def run(self, my_seed):
        
        np.random.seed(seed=my_seed)
        random.seed(my_seed)
        setup(self.par, self.gv, self.al)

        for _ in range(self.par.max_days): go(self.par, self.gv, self.al, self.pm)
        #Parallel(n_jobs=-1)(delayed(go)(self.par, self.gv, self.al, self.pm) for _ in range(self.par.max_days))
        conclusions().Chart(par=self.par, gv=self.gv)

        return self.gv
    
    def run_qTable(self, my_seed: int = 0):
        
        self.par.enablePM = False
        self.par.enableA1 = False
        self.par.enableA1 = False
        self.par.enableA1 = False
        self.pm = PM(self.par)
        self.run(my_seed=my_seed)
        
        self.qTable[0, 0] = sum(self.gv.infected_cost_history)

        self.al = agents_list()
        self.par = parameters()
        self.gv = glob_vars(self.par)
        self.par.enablePM = False
        self.par.enableA1 = False
        self.par.enableA1 = False
        self.par.enableA1 = False
        self.pm = PM(self.par)
        setup(self.par, self.gv, self.al)
        self.run(my_seed=my_seed)
        
        self.qTable[0, 1] = sum(self.gv.infected_cost_history)


        self.al = agents_list()
        self.par = parameters()
        self.gv = glob_vars(self.par)
        self.par.enablePM = True
        self.par.enableA1 = False
        self.par.enableA1 = True
        self.par.enableA1 = False
        self.pm = PM(self.par)
        setup(self.par, self.gv, self.al)
        self.run(my_seed=my_seed)

        self.qTable[0, 2] = sum(self.gv.infected_cost_history)


        self.al = agents_list()
        self.par = parameters()
        self.gv = glob_vars(self.par)
        self.par.enablePM = True
        self.par.enableA1 = True
        self.par.enableA1 = False
        self.par.enableA1 = True
        self.pm = PM(self.par)
        setup(self.par, self.gv, self.al)
        self.run(my_seed=my_seed)

        self.qTable[0, 3] = sum(self.gv.infected_cost_history)

        print(self.qTable)


