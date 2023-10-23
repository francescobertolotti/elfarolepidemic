# import libraries

class glob_vars:
    
    def __init__(self, par):
        
        # GLOBAL VARIABLES
        self.t = 0 #time step of the simulation
        self.attendance = 0  # This integer rapresent the n of the agents going to the bar each time step
        self.present_agents = [] # This is the array containing al the agents that will be in the bar each week
        self.infected_attendance = 0 # This integer rapresent the n of the agents which are infected each week
        self.present_agents_strategy = 0 # This float rapresent the strategy of agent each week
        self.n_new_infected = 0 # SCRIVERE
        self.contagious_level_sum = 0 # SCRIVERE
        self.n_infected_agents = 0 # SCRIVERE

        # STATISTICS
        self.attendance_history = [] # This array is composed from a series of integers rapresenting the number of people in the bar
        self.contagious_history = [] # This array is composed from a series of integers rapresenting the number of contagious people
        self.present_contagious_history = [] # This array is composed from a series of integers rapresenting the number of contagious people in the bar



    def compute_globals(self, al, par):

        n_infected_agents = 0                
        for present_agent in self.present_agents: # Updating n_infected_agents
            if present_agent.getIfInfected():
                n_infected_agents += 1

        self.present_contagious_history.append(n_infected_agents)
        # Calculating n of infected agents

        for agent in al.persons_list: 
            if agent.getIfInfected():
                self.infected_attendance += 1
        
        self.attendance_history.append(self.attendance)
        self.contagious_history.append(self.infected_attendance)





    
    def initialize_gv(self):
        self.attendance = 0 # This integer rapresent the n of the agents going to the bar
        self.present_agents = [] # This is the array containing al the agents that will be in the bar each week
        self.infected_attendance = 0 # This integer rapresent the n of the agents which are infected each week
        self.n_new_infected = 0 # SCRIVERE
        self.contagious_level_sum = 0 # SCRIVERE
        self.n_infected_agents = 0 # SCRIVERE

        
    def update_present_agents_strategy(self, par):
        if par.respect_the_max:
            self.present_agents_strategy = self.attendance / par.capacity
        else:
            self.present_agents_strategy = self.attendance / par.n_persons



class agents_list:
    def __init__(self):


        #insert list initialized with []
        self.persons_list = []

        


            