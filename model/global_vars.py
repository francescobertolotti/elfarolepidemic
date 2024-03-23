# import libraries
import numpy as np
import json
import os

class glob_vars:
    
    def __init__(self, par):
        
        # Global Variables
        self.t = 0 #time step of the simulation
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

        self.infected_cost_history = []
        self.a1_cost_history = []
        self.a2_cost_history = []
        self.a3_cost_history = []


        # PM
        self.capacityHistory = []
        self.a2History_x = []
        self.a2History_y = []
        self.a2_is_active = False
        self.a3History_x = []
        self.a3History_y = []
        self.a3_is_active = False

        # Q - Learning
        self.q_table = np.zeros([12, 3])


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

        self.infected_cost_history.append(par.a1_cost * self.infected_attendance)

       

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

    def last_infected(self, n):
        if n >= len(self.contagious_history):
            return self.contagious_history  # Se n è maggiore o uguale alla lunghezza dell'array, restituisce l'intero array
        else:
            return self.contagious_history[-n:]


    def regCoeff_q_learning(self, par, arr_y = []):
        if arr_y == []: arr_y = self.last_infected(n=par.infection_slope_regr_len)
        
        arr_x = np.arange(1, len(arr_y) + 1)
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
                json.dump(content, file)
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
                    self.q_table = np.array(q_table_raw)
                
                else:
                    print('No stored q-table to start')
                    json_table_id = 'First or new'
        
            return json_table_id

    def save_q_table(self, par, precedent_id):
        if par.enableRL and par.store_q_table:
            json_q_table = self.jsonLoader('model/qTable/qData.json')


            arr = json_q_table['data']
            arr.append(
                {
                   'id': str(len(arr) + 1),
                   'precedent': str(precedent_id),
                   'q-table': self.q_table.tolist()
                }
            )

            json_q_table['data'] = arr
            
            self.jsonWriter('model/qTable/qData.json', json_q_table)

    def clear_q_table(self, par):
        if par.clear_q_table_memory:
            self.jsonWriter('model/qTable/qData.json', {"selected": 1, "data": []})

class agents_list:
    def __init__(self):


        #insert list initialized with []
        self.persons_list = []
        


            
