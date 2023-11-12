# import libraries

class parameters:
    def __init__(self):

        # simulation parameters
        self.max_week = 90
        self.n_persons = 100

        # social parameters
        self.capacity = 50 # This integer represent the maximum capacity of the bar (is userfull if respect_the_max: bool = True)
        self.threshold = 0.5 # This threshold is used to determine if an agent will go to the bar or not depending on his strategy
        self.respect_the_max = True # This boolean rapresent if the bar capacity will be respected or not

        # epidemic parameters
        self.num_infected_persons = 2 # Identifies the number of starting contagious people
        self.infection_cantStartUntil = 10 # how long a person is resistent to infection
        self.infection_generatesResistance = True # is the agent susceptible to infection?
        self.infection_threshold = 0.5 # Another person gets contagious if his contagious level is greather than contagious_threshold
        self.infection_thresholdNotPresent = 0.7 # the level beyond which an agent is not going to the bar
        self.infection_duration = 10 # An agent is contagious for infection_duration weeks
        self.people_memory_weight_arr = [0.5, 0.2, 0.1] # This is the weight agents give to each single event

        #AgentDecision parameters
        self.useRegr = True
        self.useRegrFrom = 3
        self.useRegrFor = 1





        
        
