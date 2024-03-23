# TO-DO LIST

# COSE DA GGIUNGERE
# 0) testare altre strategie decisionali per gli agenti


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

        # Restoring q-table
        json_table_id = self.gv.restore_q_table(self.par)

        # Running model
        for _ in range(self.par.max_days): go(self.par, self.gv, self.al, self.pm)
        if self.par.draw_conclusions: conclusions().Chart(par=self.par, gv=self.gv)
        

        # Saving q-table
        self.gv.save_q_table(self.par, precedent_id=json_table_id)
            
        return self.gv
    
    


