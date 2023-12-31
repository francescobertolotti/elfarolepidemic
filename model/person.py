#import libraries
import random
import numpy as np
import math


class Person:
    def __init__(self, par):

        # Parameters
        self.who = None # Number of the agent
        self.strategyType = 0 # Number of strategy to follow

        # States
        self.person_memory = [] # array to save memory of attendance
        self.levelContagious = 0 # rappresent the contagious threshold
        self.ContagiousWillStopAt = 0 # rappresent the remaning time for how much this agent remains contagious
        self.infectionStartingDay = 0 # Rappresent the day when the infection has started   
        self.infectionResistanceWillStopAt = -1 # As ContagiousWillStopAt but 
        self.infectionLevelsArr = self.getContagiousArr(par)

        # Output
        self.INFECTIONS_infectionsCounter = 0 # How many times an agent got infected
        self.BAR_presenceCounter = 0 # How many times an agent got present in the bar

        # For PM
        self.facemaskType = 0

    
    
    def regrLinStrategyMethod(self, par, gv):
        regr = gv.regLine(par, self.person_memory)
        regr_output = regr[len(regr) - 1]
        return (regr_output * par.useRegrFor) + (self.defaultStrategyMethod() * (1 - par.useRegrFor))
    
    def randomStrategyMethod(self):
        return random.random()
    
    def defaultStrategyMethod(self):
        return self.randomStrategyMethod()
    
    def personStrategyOutputOne(self) -> None: # This function calculates the latest strategy for the agents every day
        s_output = self.defaultStrategyMethod()
        self.person_memory.append(s_output)
        
    
    def personStrategyOutputTwo(self, par, gv) -> None: # This function calculates the latest strategy for the agents every day
        if gv.t >= par.useRegrFrom:
            s_output = self.regrLinStrategyMethod(par, gv)
        else:
            s_output = self.defaultStrategyMethod()
        self.person_memory.append(s_output)
        
    
    def memoryMean(self, par) -> float: # This function returns the actual strategy composed by the last strategy and the ol strategies of the past days. This is done through a weighed average.

        if len(self.person_memory) > 1:
            compiled_memory = []
            compiled_memory_sub = []
            general_weight = (1 - np.sum(par.people_memory_weight_arr)) / (len(self.person_memory) - len(par.people_memory_weight_arr))
            if len(self.person_memory) > len(par.people_memory_weight_arr):
                prov_people_memory_weight_arr = par.people_memory_weight_arr
            else:
                prov_people_memory_weight_arr = []
                cont_sub = 0
                sub_bool = True
                for i, el in enumerate(par.people_memory_weight_arr):
                    if i < len(self.person_memory) - 1:
                        prov_people_memory_weight_arr.append(el)
                        cont_sub += el
                    elif sub_bool:
                        sub_bool = False
                        prov_people_memory_weight_arr.append(1 - cont_sub)
                        
            for i, el in enumerate(self.person_memory):
                if i < (len(self.person_memory) - len(prov_people_memory_weight_arr)):
                    compiled_memory.append(el * general_weight)
                    compiled_memory_sub.append(general_weight)
                else:
                    compiled_memory.append(el * (prov_people_memory_weight_arr[len(self.person_memory) - 1 - i])) 
                    compiled_memory_sub.append(prov_people_memory_weight_arr[len(self.person_memory) - 1 - i])    

                        
            
            ris = np.sum(compiled_memory)
            sub = np.sum(compiled_memory_sub)
            if (sub < 0.99999999 or sub > 1.00000001):
                print("Errore, sub = %.20f = %.2f, len(sefl.person_memory) = %d" % (sub, sub, len(self.person_memory)))
            
            return ris
        
        else:
            return self.person_memory[0]
    
    def personCurrentStrategy(self, par, gv) -> float: # This function is a wrapper for personStrategyOutput and memoryMean
        if self.strategyType == 1:
            self.personStrategyOutputOne()
        if self.strategyType == 2:
            self.personStrategyOutputTwo(par, gv)
        memoryMeanF = self.memoryMean(par)
        return memoryMeanF
    
    def updateLastStrategy(self, gv) -> None: # In case an agent goes to the bar, this function updates the strategy of the agent
        if len(self.person_memory) > 0:
            self.person_memory.pop(len(self.person_memory) - 1)
        else:
            print('Error memory arr day:%d agent:%d memory:%s' % (gv.t, self.who, self.person_memory))
        self.person_memory.append(gv.present_agents_strategy)
    
    def canAgentBeInfected(self, par, gv):
        infectAgentDecisionSIR = False
        infectionStartingDay = gv.t
        if par.infection_generatesResistance:
            if par.infection_cantStartUntil != 0:
                if infectionStartingDay >= self.infectionResistanceWillStopAt:
                    infectAgentDecisionSIR = True
            else:
                if self.INFECTIONS_infectionsCounter == 0:
                    infectAgentDecisionSIR = True
        else:
            infectAgentDecisionSIR = True

        if infectionStartingDay == -1:
            infectAgentDecisionSIR = True
        
        return infectAgentDecisionSIR


    def initiateContagius(self, par, gv) -> bool: # This function is needed to initiate the contagious for the agent (returns a boolean that indicates if the contagious was executed)
        infectAgentDecisionSIR = self.canAgentBeInfected(par, gv)
        infectionStartingDay = gv.t
                
        if infectAgentDecisionSIR:
            self.levelContagious = 1  # This rapresent the initial contagious level
            self.ContagiousWillStopAt = par.infection_duration + infectionStartingDay # This rapresent the remaining time for the agent to remain infected, the first day this is equal to self.timeContagious

            self.infectionStartingDay = infectionStartingDay # This indicate the number of the day in which the agent is infected
            
            self.INFECTIONS_infectionsCounter += 1 # Counts how many time the agent gets infected

            if par.infection_generatesResistance:
                if par.infection_cantStartUntil != 0:
                    self.infectionResistanceWillStopAt = par.infection_cantStartUntil + self.ContagiousWillStopAt + 1
            return True
        else:
            return False

    def getContagiousArr(self, par):
        x, x_max = 0.1, 1
        x_ts = [x]
        t_max = par.infection_duration
        c, d = 0.5, 0.4

        for t in range(1, t_max + 1): 
            x = x + c * (1 - x / x_max) 
            x = x * ( 1 - t / t_max ) 
            x_ts.append(x)
        
        x_ts = np.array(x_ts)
        
        x_ts_toOne = x_ts * (1 + ((1 - max(x_ts))/max(x_ts)))
        
        return x_ts_toOne

    def getContagiousLevel(self, par, gv, current_day: int = -1): # This functions calculates the level of contagious for the agents every day
        if current_day == -1:
            print('Contagious level error')
        

        if self.ContagiousWillStopAt - (current_day - 1) > 0:

            t = (current_day - self.infectionStartingDay)

            # if self.who == 1: print(self.infectionLevelsArr[t - 1], gv.t)
            x = self.infectionLevelsArr[t - 1]
            self.levelContagious = x

            return x
            
        elif self.ContagiousWillStopAt - (current_day - 1) == 0 and gv.t != 1:
            
            self.levelContagious = 0
            self.ContagiousWillStopAt = 0
            self.infectionStartingDay = 0
            self.infectionResistanceWillStopAt = par.infection_cantStartUntil + current_day
            gv.recovered_agents += 1
            
            return 0
        
    def getIfInfected(self): # This function returns a boolean that indicates if the agent is infected
        if self.levelContagious > 0:
            return True
        else:
            return False



    def decisionAttendingBar(self, gv, par):
        
        # if the attenance is already above the bar capacity and it is taken into consideration by agents, do not try to attend
        if gv.attendance >= gv.actualCapacity and par.respect_the_max:
            return

        else:
            a_strat = self.personCurrentStrategy(par, gv) # This float rapresent the strategy of agent each day
                
            c_level = 0 # This float rapresent the contagious level of agent each day
            if self.getIfInfected(): # If agent is infected
                c_level = self.getContagiousLevel(par, gv, current_day=gv.t) # Calculate contagious level
                #if gv.t == 18: print(c_level, gv.t, self.who, self.ContagiousWillStopAt, self.infectionStartingDay)
                #if self.who == 1: print(c_level, gv.t, self.who, self.ContagiousWillStopAt, self.infectionStartingDay)
            if a_strat < par.threshold and c_level <= par.infection_thresholdNotPresent: # If the agent strategy for this day and contagious level is below the not present threshold, he will be in the bare.
                presence_bool = True
                if par.enablePM and par.enableA3 and gv.a3_is_active:
                    if c_level > par.a3_testFailUnder:
                        presence_bool = False

                if presence_bool:
                    gv.attendance += 1
                    self.BAR_presenceCounter += 1
                    gv.present_agents.append(self)





    def infection_dynamics(self, gv, par, al):

        for present_agent in gv.present_agents: # This will calculate contagious_level_sum
            gv.contagious_level_sum += present_agent.levelContagious

        for present_agent in gv.present_agents: # This will calculate n_infected_agents
            if present_agent.getIfInfected():
                gv.n_infected_agents += 1
        
        gv.present_contagious_history.append(gv.n_infected_agents)

        n_susceptible_agents = len(gv.present_agents) - gv.n_infected_agents # This is the n of agents that could be infected this day
        
        try:
            #n_new_infected = int(math.ceil(gv.contagious_level_sum * n_susceptible_agents / (n_susceptible_agents + gv.n_infected_agents))) # This is the n of agents that will be infected this day
            n_new_infected = int(0.5 + par.alpha * gv.contagious_level_sum * n_susceptible_agents / (par.capacity)) # This is the n of agents that will be infected this day
        except:
            print('Error day %d, divison0 %.2f' % (gv.t, (par.capacity)))
            n_new_infected = 0
        
        '''
        cont = 0
        present_agents_susceptible = [ag for ag in gv.present_agents if not ag.getIfInfected()] # This is a list of agents that could be infected
        present_agents_infected = [ag for ag in gv.present_agents if ag.getIfInfected()] # This is a list of agents that are infected
        new_infected = random.sample(present_agents_susceptible, n_new_infected) # This is a list of agents that will be infected
        for agent in new_infected: # This will infect the agents
            agent.initiateContagius(par, gv) 
            cont += 1
        '''

        present_agents_susceptible = [ag for ag in gv.present_agents if not ag.getIfInfected()] # This is a list of agents that could be infected
        present_agents_infected = [ag for ag in gv.present_agents if ag.getIfInfected()] # This is a list of agents that are infected
        present_agents_susceptible_infectable = [ag for ag in gv.present_agents if ag.canAgentBeInfected(par, gv) and not ag.getIfInfected()] # This is a list of agents that could be infected
        cont = 0

        a2_t_1 = par.infection_threshold + par.a2_faceMask1Perc
        a2_t_2 = par.infection_threshold + par.a2_faceMask2Perc

        for infected_agent in present_agents_infected:
            if infected_agent.levelContagious >= par.infection_threshold and infected_agent.levelContagious <= par.infection_thresholdNotPresent:
                for  i in range(n_new_infected):
                    if len(present_agents_susceptible_infectable) > 0:
                        ag_to_infect = random.choice(present_agents_susceptible_infectable)
                        if par.enableA2 and par.enablePM:
                            if ag_to_infect.facemaskType == 1:
                                real_treshold = a2_t_1
                            elif ag_to_infect.facemaskType == 2:
                                real_treshold = a2_t_2
                            elif ag_to_infect.facemaskType == 0:
                                real_treshold = par.infection_threshold       
                        else:
                            real_treshold = par.infection_threshold
                        if infected_agent.levelContagious >= real_treshold:
                            present_agents_susceptible_infectable.remove(ag_to_infect)
                            ag_to_infect.initiateContagius(par, gv)
                            cont += 1
                    else:
                        break

        '''
        cont = 0
        cont_a = 0
        present_agents_infected = [ag for ag in gv.present_agents if ag.getIfInfected()] # This is a list of agents that could be infected
        for p_i_a in present_agents_infected:
            if p_i_a.levelContagious >= par.infection_threshold and p_i_a.levelContagious <= par.infection_thresholdNotPresent:
                present_agents_susceptible = [ag for ag in gv.present_agents if not ag.getIfInfected()] # This is a list of agents that could be infected
                n_new_infected_per_agent = n_new_infected
                if n_new_infected_per_agent >= len(present_agents_susceptible): n_new_infected_per_agent = (len(present_agents_susceptible) - 1)
                new_infected = random.sample(present_agents_susceptible, len(present_agents_susceptible))
                cont_a = 0
                while n_new_infected_per_agent > 0:
                    print(cont_a, n_new_infected_per_agent, len(present_agents_susceptible), n_new_infected, len(new_infected), new_infected)
                    new_infected_by_a = new_infected[cont_a]
                    
                    cont_a += 1
                    if not new_infected_by_a.getIfInfected():
                        contagious_execution = new_infected_by_a.initiateContagius(par, gv)
                        if contagious_execution:
                            cont += 1
                            n_new_infected_per_agent -= 1
        
        '''
        gv.new_infected_history.append(cont)
        # cont_debug = 0
        # totInfectedWeekByAgent = 0 # This is a counter for people infected this week by each agent
        # for present_infectious_agent in gv.present_agents: # For each infectous agents between the present agents
        #     totInfectedWeekByAgent = n_new_infected
        #     if present_infectious_agent.levelContagious >= par.infection_threshold and present_infectious_agent.levelContagious <= par.infection_thresholdNotPresent: # If the agent can infect other agents
        #         for present_agent in gv.present_agents: # For each present agent
        #             if present_agent.getIfInfected() == False: # If not infected
        #                 if totInfectedWeekByAgent > 0: # InitiateContagious for n_new_infected agents
        #                     cont_debug += 1
        #                     contagious_execution = present_agent.initiateContagius(par, gv) # InitiateContagious of present agent
        #                     if contagious_execution:
        #                         totInfectedWeekByAgent -= 1 # The counter for the people that could be infected by de agent, decrease by one
        #print(n_new_infected*gv.n_infected_agents, cont_debug, gv.t)
