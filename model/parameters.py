# import libraries

class parameters:
    def __init__(self):

        # Simulation parameters
        self.max_week = 100
        self.n_persons = 100

        # Social parameters
        self.capacity = 50 # This integer represent the maximum capacity of the bar (is userfull if respect_the_max: bool = True)
        self.threshold = 0.5 # This threshold is used to determine if an agent will go to the bar or not depending on his strategy
        self.respect_the_max = True # This boolean rapresent if the bar capacity will be respected or not

        # Epidemic parameters
        self.num_infected_persons = 5 # Identifies the number of starting contagious people
        self.infection_cantStartUntil = 2 # how long a person is resistent to infection
        self.infection_generatesResistance = True # is the agent susceptible to infection?
        self.infection_threshold = 0.5 # Another person gets contagious if his contagious level is greather than contagious_threshold
        self.infection_thresholdNotPresent = 0.7 # the level beyond which an agent is not going to the bar
        self.infection_duration = 10 # An agent is contagious for infection_duration weeks
        self.people_memory_weight_arr = [0.5, 0.2, 0.1] # This is the weight agents give to each single event

        # Agent strategies
        self.strategyOne = 0.5 # StrategyOne: Random strategy
        self.strategyTwo = 1 - self.strategyOne # StrategyOne: Partialy with linearRegression

        # Agent strategyTwo parameters
        self.useRegr = True # da togliere
        self.useRegrFrom = 3
        self.useRegrFor = 1



        # PM parameters
        self.enablePM = True
        self.a1_reductionPerc = 0.3
        self.a1_reductionDuration = 3
        self.a1_InfectedTreshold = 50

        
        
