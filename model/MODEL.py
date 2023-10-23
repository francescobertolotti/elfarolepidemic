# TO-DO LIST
# 1) contagiuslevel cambiare nome
# 2) cambiare SIR con altro

# COSE DA GGIUNGERE
# 0) testare altre strategie decisionali per gli agenti
# 1) metrica per contare quante volte un agente va al bar


from model.parameters import *
from model.global_vars import *
from model.person import *
from model.setup import *
from model.go import *
from model.conclusion import *
import numpy as np

class model():
    def __init__(self, my_seed):
        
        random.seed(my_seed)
        np.random.seed(seed=my_seed)

        self.al = agents_list()
        self.par = parameters()
        self.gv = glob_vars(self.par)

    def run(self, my_seed):
        
        np.random.seed(seed=my_seed)
        random.seed(my_seed)
        setup(self.par, self.gv, self.al)

        for _ in range(self.par.max_week): go(self.par, self.gv, self.al)

        conclusions().Chart(par=self.par, gv=self.gv)

        return self.gv


