#import libraries
import random
import numpy as np

class Person:
    def __init__(self):

        # PARAMETERS
        self.who = None #number of the agent

        # STATES
        self.person_memory = [] # array to save memory of attendance
        self.levelContagious = 0 # rappresent the contagious threshold
        self.ContagiousWillStopAt = 0 # rappresent the remaning time for how much this agent remains contagious
        self.infectionStartingWeek = 0 # Rappresent the week when the infection has started   
        self.SIRWillStopAt = -1 # as ContagiousWillStopAt but 

        # OUTPUT
        self.SIR_infectionsCounter = 0 # how many times an agent got infected
 
        
    def personStrategyOutput(self) -> None: # This function calculates the latest strategy for the agents every week
        s_output = random.random()
        self.person_memory.append(s_output)
        
    
    def memoryMean(self, par) -> float: # This function returns the actual strategy composed by the last strategy and the ol strategies of the past weeks. This is done through a weighed average.

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
            if sub < 0.9999 or sub > 1.0001:
                print("Errore, sub = %.2f, len(sefl.person_memory) = %d" % (sub, len(self.person_memory)))
            
            
            return ris
        
        else:
            return self.person_memory[0]
    
    def personCurrentStrategy(self, par) -> float: # This function is a wrapper for personStrategyOutput and memoryMean
        self.personStrategyOutput()
        memoryMeanF = self.memoryMean(par)
        return memoryMeanF
    
    def updateLastStrategy(self, gv) -> None: # In case an agent goes to the bar, this function updates the strategy of the agent
        if len(self.person_memory) > 0:
            self.person_memory.pop(len(self.person_memory) - 1)
        else:
            print('Error memory arr day:%d agent:%d memory:%s' % (gv.t, self.who, self.person_memory))
        self.person_memory.append(gv.present_agents_strategy)
    
    #par, gv
    def initiateContagius(self, par, gv) -> bool: # This function is needed to initiate the contagious for the agent (returns a boolean that indicates if the contagious was executed)
        infectAgentDecisionSIR = False
        contagiousTime = par.infection_duration
        infectionStartingWeek = gv.t
        if par.infection_generatesResistance:
            if par.infection_cantStartUntil != 0:
                if infectionStartingWeek >= self.SIRWillStopAt:
                    infectAgentDecisionSIR = True
            else:
                if self.SIR_infectionsCounter == 0:
                    infectAgentDecisionSIR = True
        else:
            infectAgentDecisionSIR = True

        if infectionStartingWeek == -1:
            infectAgentDecisionSIR = True
                
        if infectAgentDecisionSIR:
            self.levelContagious = 1  # This rapresent the initial contagious level
            self.timeContagious = contagiousTime # This rapresent for how much time the agent will remain infected
            self.ContagiousWillStopAt = self.timeContagious + infectionStartingWeek # This rapresent the remaining time for the agent to remain infected, the first day this is equal to self.timeContagious

            self.infectionStartingWeek = infectionStartingWeek # This indicate the number of the week in which the agent is infected
            
            self.SIR_infectionsCounter += 1 # Counts how many time the agent gets infected

            if par.infection_generatesResistance:
                if par.infection_cantStartUntil != 0:
                    self.SIRWillStopAt = par.infection_cantStartUntil + self.ContagiousWillStopAt + 1
            return True
        else:
            return False


    def getContagiousLevel(self, current_week: int = -1): # This functions calculates the level of contagious for the agents every week
        if current_week == -1:
            raise Exception('Contagious level error')
        
        if self.ContagiousWillStopAt - current_week >= 0:

            x, x_max = 0.1, 1
            x_ts = [x]
            t_max = self.timeContagious
            c, d = 0.5, 0.4

            t = (current_week - self.infectionStartingWeek)

            x = x + c * (1 - x / x_max) 
            x = x * ( 1 - t / t_max )
            
            self.levelContagious = x

            return x
            
        else:
            self.levelContagious = 0
            self.ContagiousWillStopAt = 0
            self.infectionStartingWeek = 0
            self.SIRWillStopAt = self.infection_cantStartUntil + current_week
            
            return 0
        
    def getIfInfected(self): # This function returns a boolean that indicates if the agent is infected
        if self.levelContagious > 0:
            return True
        else:
            return False



    def decisionAttendingBar(self, gv, par):
        
        # if the attenance is already above the bar capacity and it is taken into consideration by agents, do not try to attend
        if gv.attendance >= par.capacity and par.respect_the_max:
            return

        else:
            a_strat = self.personCurrentStrategy(par) # This float rapresent the strategy of agent each week
                
            c_level = 0 # This float rapresent the contagious level of agent each week
            if self.getIfInfected(): # If agent is infected
                c_level = self.getContagiousLevel(current_week=gv.t) # Calculate contagious level

            if a_strat < par.threshold and c_level <= par.infection_thresholdNotPresent: # If the agent strategy for this week and contagious level is below the not present threshold, he will be in the bare.
                gv.attendance += 1
                gv.present_agents.append(self)





    def infection_dynamics(self, gv, par, al):

        for present_agent in gv.present_agents: # This will calculate contagious_level_sum
            gv.contagious_level_sum += present_agent.levelContagious

        for present_agent in gv.present_agents: # This will calculate n_infected_agents
            if present_agent.getIfInfected():
                gv.n_infected_agents += 1
            
        n_susceptible_agents = len(gv.present_agents) - gv.n_infected_agents # This is the n of agents that could be infected this week
        
        try:
            n_new_infected = int(gv.contagious_level_sum * n_susceptible_agents / (n_susceptible_agents + gv.n_infected_agents)) # This is the n of agents that will be infected this week
        except:
            #print('Error week %d, divison0 %.2f' % (week, (n_susceptible_agents + n_infected_agents)))
            n_new_infected = 0

        totInfectedWeekByAgent = 0 # This is a counter for people infected this week by each agent
        for present_infectious_agent in gv.present_agents: # For each infectous agents between the present agents
            totInfectedWeekByAgent = n_new_infected
            if present_infectious_agent.levelContagious >= par.infection_threshold and present_infectious_agent.levelContagious <= par.infection_thresholdNotPresent: # If the agent can infect other agents
                for present_agent in gv.present_agents: # For each present agent
                    if present_agent.getIfInfected() == False: # If not infected
                        if totInfectedWeekByAgent > 0: # InitiateContagious for n_new_infected agents
                            contagious_execution = present_agent.initiateContagius(par, gv) # InitiateContagious of present agent
                            if contagious_execution:
                                totInfectedWeekByAgent -= 1 # The counter for the people that could be infected by de agent, decrease by one
