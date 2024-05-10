# import libraries

class parameters:
    def __init__(self):

        # Simulation parameters
        self.max_days = 100 # Number of days for each simulation
        self.n_persons = 2000 # Represents the number of people for each simulation.

        # Social parameters
        self.capacity = 1500 # This integer represent the maximum capacity of the bar (is userfull if respect_the_max: bool = True)
        self.threshold = 0.5 # This threshold is used to determine if an agent will go to the bar or not depending on his strategy
        self.respect_the_max = True # This boolean represent if the bar capacity will be respected or not

        # Agent strategies
        self.strategyOne = 0.1 # StrategyOne: Random strategy
        self.strategyTwo = 1 - self.strategyOne # StrategyOne: Partialy with linearRegression

        # Agent strategyTwo parameters
        self.useRegrFrom = 10 # Indicates the day from which the regression line will be used
        self.useRegrFor = 1 # Of the total output of the strategy defined by the agent each week, the value defined by the linear regression of the previous ones impacts by a percentage defined by the parameter

        # Epidemic parameters
        self.num_infected_persons = 100 # Identifies the number of starting contagious people
        self.infection_cantStartUntil = 2 # how long a person is resistent to infection
        self.infection_generatesResistance = True # is the agent susceptible to infection?
        self.infection_threshold = 0.4 # Another person gets contagious if his contagious level is greather than contagious_threshold
        self.infection_thresholdNotPresent = 0.8 # the level beyond which an agent is not going to the bar
        self.infection_duration = 10 # An agent is contagious for infection_duration day
        self.people_memory_weight_arr = [0.5, 0.2, 0.1] # This is the weight agents give to each single event
        self.alpha = 0.2 # This is the weight to the new infected agents
        self.regression_type = 1 # Indicates the regression line degree for np.polyfit function (1 = Linear regression)
        self.infection_randomness = 0.25 # this treshold changes the level contagius by a value rangin from -self.infection_randomness to self.infection_randomness


        # PM parameters
        self.enablePM = True # Enable Policy Maker
        self.enableA1 = True # Enable strategy a1
        self.enableA2 = True # Enable strategy a2
        self.enableA3 = True # Enable strategy a3

        self.enable_at_least_one_A = False

        self.delta = 150 # The cost that new infections have

        self.r = 0 # Revenue for each recovered agent

        # PM a1
        self.a1_reductionPerc = 0.8
        self.a1_reductionDuration = 10
        self.a1_InfectedTreshold = 0.375 # Percentage of infected above to activate strategy a1 for PM, calculated on self.n_persons
        self.a1_cost = 2

        # PM a2
        self.a2_faceMask1Agents = 0.65
        self.a2_faceMask2Agents = 0.3
        self.a2_faceMask0Agents = 1 - self.a2_faceMask1Agents - self.a2_faceMask2Agents
        self.a2_faceMask1Perc = 0.3775
        self.a2_faceMask2Perc = 0.5
        self.a2_reductionDuration = 1
        self.a2_InfectedTreshold = 0.1 # Percentage of infected above to activate strategy a2 for PM, calculated on self.n_persons
        self.a2_cost = 15

        # PM a3
        self.a3_testFailUnder = 0.45 # Nei casi in cui fa dovrebbe funzuionare comunque sbaglia e fa entrare
        self.a3_reductionDuration = 1
        self.a3_InfectedTreshold = 0.2
        self.a3_cost = 50000

        # PM Reinforcement leaning
        self.enableRL = True
        self.RL_mode = 2

        self.a_reductionDuration = 15 # General reduction duration for self.RL_mode = 2

        self.epsilon_RL = 0.2
        self.alpha_RL = 0.3

        self.RL_PM_t_min = 15

        self.infection_slope_regr_len = 5

        # Settings
        self.draw_conclusions = True
        self.save_conclusions = True
        self.save_duplicate_q_table = True

        self.restore_parameters = False
        self.restore_parameters_path = '3'

        self.store_q_table = True
        self.stat_from_stored_q_table = True
        self.stored_q_table_id = 'last'

        self.clear_q_table_memory = False