# import libraries
import numpy as np

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

        # PM
        self.capacityHistory = []
        self.a2History_x = []
        self.a2History_y = []
        self.a2_is_active = False
        self.a3History_x = []
        self.a3History_y = []
        self.a3_is_active = False

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



class agents_list:
    def __init__(self):


        #insert list initialized with []
        self.persons_list = []

        


            
