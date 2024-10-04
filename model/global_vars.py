# import libraries
import numpy as np
import json
import os
import warnings

class glob_vars:
    
    def __init__(self, par):
        
        # Global Variables
        self.t = 0 #time step of the simulation
        self.t_history = []
        self.attendance = 0  # This integer rapresent the n of the agents going to the bar each time step
        self.present_agents = [] # This is the array containing al the agents that will be in the bar each day
        self.infected_attendance = 0 # This integer rapresent the n of the agents which are infected each day
        self.present_agents_strategy = 0 # This float rapresent the strategy of agent each day
        self.n_new_infected = 0 # SCRIVERE
        self.contagious_level_sum = 0 # SCRIVERE
        self.n_infected_agents = 0 # SCRIVERE
        self.actualCapacity = par.capacity
        self.recovered_agents = 0


        # Statistics
        self.attendance_history = [] # This array is composed from a series of integers rapresenting the number of people in the bar
        self.contagious_history = [] # This array is composed from a series of integers rapresenting the number of contagious people
        self.present_contagious_history = [] # This array is composed from a series of integers rapresenting the number of contagious people in the bar
        
        self.new_infected_history = []
        self.recovered_agents_history = []

        self.txt_output = ''
        


        # PM
        self.capacityHistory = []
        self.a1_is_active = False
        self.a1_is_active_history = []
        self.a2History_x = []
        self.a2History_y = []
        self.a2_is_active = False
        self.a2_is_active_history = []
        self.a3History_x = []
        self.a3History_y = []
        self.a3_is_active = False
        self.a3_is_active_history = []
        self.a3_cost_is_relevant = True
        self.a3_used_at_least_once = False

        # Q - Learning
        if par.RL_mode == 1: self.q_table = np.zeros([12, 3])
        else:
            self.q_table = np.zeros([12, 12])
            self.q_table_delta_infections = np.zeros([12, 12])

        self.export_q_table = {}

        self.action_on_random = []
        self.action_on_random_zero = []
        self.action_on_max = []

        # Value
        self.a1_cost_history = []
        self.a2_cost_history = []
        self.a3_cost_history = []

        self.C_a_cost_history = []
        self.C_n_i_cost_history = []

        self.C_cost_history = []

        self.R_revenues_history = []
        
        # Epoch
        self.epoch_id = 0
        self.is_epoch = False

    def compute_globals(self, al, par):

        # Calculating n of infected agents

        for agent in al.persons_list: 
            if agent.getIfInfected():
                self.infected_attendance += 1
        
        self.attendance = len(self.present_agents)
        # print('day %d, attendance %d, infected_attendance %d' % (self.t, self.attendance, self.infected_attendance))
        self.attendance_history.append(self.attendance)
        self.contagious_history.append(self.infected_attendance)

        self.recovered_agents_history.append(self.recovered_agents)
        self.capacityHistory.append(self.actualCapacity)

        

       

    def regLine(self, par, arr_y, next_val = "", arr_x = ""):
        if arr_x == "":
            arr_x = np.arange(1, len(arr_y) + 1)
        if next_val == "":
            arr_x_n = np.arange(1, len(arr_y) + 2)
        else:
            arr_x_n = np.arange(1, next_val + 1)

        coefficients = np.polyfit(arr_x, arr_y, par.regression_type)
        regression_line = np.poly1d(coefficients)
        res_arr = regression_line(arr_x_n)

        return res_arr

    def last_infected(self, n, arr = []):
        if arr == []: arr_l_i = self.contagious_history
        else: arr_l_i = arr

        if n >= len(arr_l_i):
            return arr_l_i  # Se n è maggiore o uguale alla lunghezza dell'array, restituisce l'intero array
        else:
            return arr_l_i[-n:]


    def regCoeff_q_learning(self, par, n_pre = 0, arr_y_pre = []):
        if n_pre == 0: n = par.infection_slope_regr_len
        else: n = n_pre

        if len(arr_y_pre) > 0: arr_y = self.last_infected(n)
        else: arr_y = self.last_infected(n, arr_y_pre)
        
        # print(arr_y)
        arr_x = np.arange(1, len(arr_y) + 1)
        
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', r'All-NaN (slice|axis) encountered')
            coefficients = np.polyfit(arr_x, arr_y, 1)

        return coefficients
    
    def initialize_gv(self):
        self.attendance = 0 # This integer rapresent the n of the agents going to the bar
        self.present_agents = [] # This is the array containing al the agents that will be in the bar each day
        self.infected_attendance = 0 # This integer rapresent the n of the agents which are infected each day
        self.n_new_infected = 0 # SCRIVERE
        self.contagious_level_sum = 0 # SCRIVERE
        self.n_infected_agents = 0 # SCRIVERE
        self.recovered_agents = 0

        
        
    def update_present_agents_strategy(self, par):
        if par.respect_the_max:
            self.present_agents_strategy = self.attendance / par.capacity
        else:
            self.present_agents_strategy = self.attendance / par.n_persons



    # Json
    
    def jsonLoader(self, name: str) -> str:
        if os.path.exists(name):
            try:
                with open(name, encoding="utf-8") as file:
                    content = json.load(file)
            except Exception:
                print("Unable to load %s file, unexpected error." % name)
        else:
            print("Unable to find %s file in current directory." % name)
        return content
    
    def jsonWriter(self, name: str, content) -> str:
        if os.path.exists(name):
            #try:
            with open(name, 'w') as file:
                json.dump(content, file, indent=4)
            #except Exception:
                #print("Unable to write %s file, unexpected error." % name)
        else:
            print("Unable to write %s file in current directory." % name)



    def restore_q_table(self, par):
        if par.enableRL:
            if par.stat_from_stored_q_table:
                json_q_table = self.jsonLoader('model/qTable/qData.json')
                if len(json_q_table['data']) > 0 or par.stored_q_table_id == 'new':
                    if par.stored_q_table_id == 'last':
                        json_table_id = len(json_q_table['data']) - 1
                    else:
                        json_table_id = par.stored_q_table_id - 1
                    
                    q_table_raw = json_q_table['data'][json_table_id]['q-table']
                    q_table_raw_delta_infections = json_q_table['data'][json_table_id]['q-table-delta-infections']
                    
                    self.q_table = np.array(q_table_raw)
                    self.q_table_delta_infections = np.array(q_table_raw_delta_infections)
                
                else:
                    print('No stored q-table to start')
                    json_table_id = 'First or new'
            else:
                json_table_id = 'First or new'
            return json_table_id

    def save_q_table(self, par, precedent_id):
        if par.enableRL and par.store_q_table:
            json_q_table = self.jsonLoader('model/qTable/qData.json')


            arr = json_q_table['data']
            self.export_q_table = {
                   'id': str(len(arr) + 1),
                   'precedent': str(precedent_id),
                   'q-table': self.q_table.tolist(),
                   'q-table-delta-infections': self.q_table_delta_infections.tolist()
                }
            arr.append(self.export_q_table)
            
            json_q_table['data'] = arr
            
            self.jsonWriter('model/qTable/qData.json', json_q_table)

    def clear_q_table(self, par):
        if par.clear_q_table_memory:
            self.jsonWriter('model/qTable/qData.json', {"selected": 1, "data": []})


    def calculate_value(self, par):
        if par.enablePM:

            if par.enableA1 and self.a1_is_active: a1_cost = round((par.capacity - self.actualCapacity) * par.a1_cost * 1, 2) # Da rivedere
            else: a1_cost = 0

            self.a1_cost_history.append(a1_cost)
            
            if par.enableA2 and self.a2_is_active:
                # a2_cost = round(self.actualCapacity * par.a2_cost, 2) # Da sistemare con suddivisione mascherine
                a2_type_0 = 0
                a2_type_1 = 0
                a2_type_2 = 0
                for agent in self.present_agents:
                    if agent.facemaskType == 0: a2_type_0 += 1
                    elif agent.facemaskType == 1: a2_type_1 += 1
                    elif agent.facemaskType == 2: a2_type_2 += 1
                a2_cost = round((a2_type_1 * par.a2_cost_1) + (a2_type_2 * par.a2_cost_2), 2)

            else: a2_cost = 0
            
            

            self.a2_cost_history.append(a2_cost)
            
            if par.enableA3 and self.a3_is_active and self.a3_cost_is_relevant:
                a3_cost = par.a3_cost 
                self.a3_cost_is_relevant = False
            else: a3_cost = 0
                
            self.a3_cost_history.append(a3_cost)

            C_a_cost = a1_cost + a2_cost + a3_cost
            self.C_a_cost_history.append(C_a_cost)
        else:
            a1_cost = 0
            a2_cost = 0
            a3_cost = 0
            C_a_cost = 0

        C_n_i_cost = par.delta * self.new_infected_history[-1]
        self.C_n_i_cost_history.append(C_n_i_cost)

        # print(f'a1: {a1_cost}, a2: {a2_cost}, a3: {a3_cost}, C_a {C_a_cost}, C_n_i {C_n_i_cost}, C{C_a_cost + C_n_i_cost}')
        self.C_cost_history.append(C_a_cost + C_n_i_cost)

        R_rev = self.recovered_agents * par.r
        self.R_revenues_history.append(R_rev)

        # print(f'R_rev: {R_rev}, a_1: {a1_cost}, a_2: {a2_cost}, a3: {a3_cost}, C_a {C_a_cost}, C_n_i {C_n_i_cost}, {self.new_infected_history}')

    def restore_parameters(self, par):
        cwd = os.getcwd()
        if cwd.split('/')[-1] != 'model': cwd += '/model'
        cwd += '/output'

        cwd += f'/{str(par.restore_parameters_path)}/parameters.json'

        if os.path.exists(cwd):
            
            par_dict = self.jsonLoader(cwd)

            for key, value in par_dict.items():
                setattr(par, key, value)
                    
        else: print('Error! par.restore_parameters_path -> path does not exist')

        

class agents_list:
    def __init__(self):


        #insert list initialized with []
        self.persons_list = []
        


            
