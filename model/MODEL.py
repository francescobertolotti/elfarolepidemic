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
        if self.par.restore_parameters:
            self.gv.restore_parameters(par=self.par)
        self.pm = PM(self.par)


    def run(self, my_seed):
    
        np.random.seed(seed=my_seed)
        random.seed(my_seed)
        setup(self.par, self.gv, self.al)

        # Restoring q-table
        json_table_id = self.gv.restore_q_table(self.par)

        # Running model
        for _ in range(self.par.max_days): go(self.par, self.gv, self.al, self.pm)

        
        c = conclusions(self.par)
        if self.par.draw_conclusions or self.par.save_conclusions:
            c.Chart(par=self.par, gv=self.gv)
            c.Chart_cost(par=self.par, gv=self.gv)
        if self.par.csv_conclusions:
            c.CSV_data(par=self.par, gv=self.gv)
        if self.par.save_parameters:
            c.save_parameters(par=self.par)
        
        

        # Saving q-table
        if self.par.enableRL and self.par.enablePM:
            self.gv.save_q_table(self.par, precedent_id=json_table_id)
            if self.par.save_current_q_table: c.save_current_q_table(gv=self.gv)
            
        return self.gv
    
    


