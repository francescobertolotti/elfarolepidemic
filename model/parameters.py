# import libraries

class parameters:
    def __init__(self):

        # simulation parameters
        self.max_week = 90
        self.n_persons = 90

        # social parameters
        self.capacity = 50 # This integer represent the maximum capacity of the bar (is userfull if respect_the_max: bool = True)
        self.threshold = 0.5 # This threshold is used to determine if an agent will go to the bar or not depending on his strategy
        self.respect_the_max = True # This boolean rapresent if the bar capacity will be respected or not

        # epidemic parameters
        self.num_contagious_persons = 2 # Identifies the number of starting contagious people
        self.SirTime = 10 # how long a person is resistent to infection
        self.agentSIR = True # is the agent susceptible to infection?
        self.contagious_threshold = 0.5 # Another person gets contagious if his contagious level is greather than contagious_threshold
        self.contagious_thresholdNotPresent = 0.7 # the level beyond which an agent is not going to the bar
        self.contagious_duration = 10 # An agent is contagious for contagious_duration weeks
        self.people_memory_weight = 0.7 # This is the weight agents give to each single event








        
        
