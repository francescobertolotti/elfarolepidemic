#import libraries
import numpy as np
import random

class PM:

    __RL_Full_Actions = {
        0: (0, 0, 0),
        1: (1, 0, 0),
        2: (0, 1, 0),
        3: (0, 0, 1),
        4: (1, 1, 0),
        5: (1, 0, 1),
        6: (0, 1, 1),
        7: (1, 1, 1),
    }

    def __init__(self, par) -> None:
        
        # Parameters (Default)
        self.operationsArr = []
        if not par.enableRL or (par.enableRL and par.RL_mode == 1):
            if par.enableA1:
                self.operationsArr.append("a1InitCheck")
            if par.enableA2:
                self.operationsArr.append("a2InitCheck")
            if par.enableA3:
                self.operationsArr.append("a3InitCheck")
        else:
            self.operationsArr.append("aInitCheck")
        
        # States
        self.a1OldCapacity = 0
        self.a1StartingDayReduction = par.a1_reductionDuration

        self.a2StartingDayReduction = par.a2_reductionDuration

        self.a3StartingDayReduction = par.a3_reductionDuration
    
        self.aStartingDayReduction = par.a_reductionDuration


        # Output
        self.PM_interactionCounter = 0 # Indentifies a conunter that indicates the number of times the PM interacts with the system

        # Mode 1 Reinforcement learning
        self.aviable_strategies = []
        if par.enableA1: self.aviable_strategies.append(0)
        if par.enableA2: self.aviable_strategies.append(1)
        if par.enableA3: self.aviable_strategies.append(2)
        self.action_is_active = False

        # RL
        self.current_RL_data = {}

    
    # Legacy (No PM, Mode 1)

    def a1Init_capacityReductionInit(self, par, gv):
        gv.a1_is_active_history.append(0)

        proceed = False
        if not par.enableRL or (par.enableRL and par.RL_mode == 1):
            if (gv.infected_attendance >= (par.a1_InfectedTreshold * par.n_persons)):
                proceed = True
        else:
            proceed = True

        if proceed:
            self.operationsArr.remove("a1InitCheck")
            self.PM_interactionCounter += 1
            self.a1StartingDayReduction = gv.t
            gv.actualCapacity = par.capacity * (1 - par.a1_reductionPerc)
            self.operationsArr.append("a1EndCheck")
            self.action_is_active = True
            gv.a1_is_active = True
            return True
        else:
            return False
    
    def a1Init_capacityReductionEnd(self, par, gv):
        gv.a1_is_active_history.append(1)

        proceed = False
        if not par.enableRL or (par.enableRL and par.RL_mode == 1):
            if gv.t > (self.a1StartingDayReduction + par.a1_reductionDuration):
                self.a1StartingDayReduction = gv.t
                if gv.infected_attendance < (par.a1_InfectedTreshold * par.n_persons) or par.enableRL:
                    proceed = True
        else:
            proceed = False

        if proceed:
            self.operationsArr.remove("a1EndCheck")
            self.a1StartingDayReduction = 0
            gv.actualCapacity = par.capacity
            self.operationsArr.append("a1InitCheck")
            self.action_is_active = False
            gv.a1_is_active = False
            if par.enableRL and par.RL_mode == 1: self.update_RL_q_table(par, gv)
            if par.enableRL and par.RL_mode == 2: self.update_RL_q_table_mode2(par, gv)
        
        

    
    def a2Init_faceMaskInit(self, par, gv):
        gv.a2_is_active_history.append(0)

        proceed = False
        if not par.enableRL or (par.enableRL and par.RL_mode == 1):
            if (gv.infected_attendance >= (par.a2_InfectedTreshold * par.n_persons)):
                proceed = True
        else:
            proceed = True

        if proceed:
            self.a2StartingDayReduction = gv.t
            self.operationsArr.remove("a2InitCheck")
            self.operationsArr.append("a2EndCheck")
            gv.a2_is_active = True
            self.action_is_active = True
            return True
        else:
            return False
    
    def a2Init_faceMaskEnd(self, par, gv):
        gv.a2History_x.append(gv.t)
        gv.a2History_y.append(- (par.n_persons * 0.05))
        gv.a2_is_active_history.append(1)

        proceed = False
        if not par.enableRL or (par.enableRL and par.RL_mode == 1):
            if gv.t > (self.a2StartingDayReduction + par.a2_reductionDuration):
                self.a2StartingDayReduction = gv.t
                if gv.infected_attendance < (par.a2_InfectedTreshold * par.n_persons) or par.enableRL:
                    proceed = True
        else:
            proceed = False
        
        if proceed:
            self.operationsArr.remove("a2EndCheck")
            self.operationsArr.append("a2InitCheck")
            gv.a2_is_active = False
            self.action_is_active = False
            if par.enableRL and par.RL_mode == 1: self.update_RL_q_table(par, gv)
            if par.enableRL and par.RL_mode == 2: self.update_RL_q_table_mode2(par, gv)


    def a3Init_entranceTestInit(self, par, gv):
        gv.a3_is_active_history.append(0)

        proceed = False
        if not par.enableRL or (par.enableRL and par.RL_mode == 1):
            if (gv.infected_attendance >= (par.a3_InfectedTreshold * par.n_persons)):
                proceed = True
        else:
            proceed = True

        if proceed:
            self.a3StartingDayReduction = gv.t
            self.operationsArr.remove("a3InitCheck")
            self.operationsArr.append("a3EndCheck")
            gv.a3_is_active = True
            self.action_is_active = True
            return True
        else:
            return False

    def a3Init_entranceTestEnd(self, par, gv):
        gv.a3History_x.append(gv.t)
        gv.a3History_y.append(- (par.n_persons * 0.1))
        gv.a3_is_active_history.append(1)

        proceed = False
        if not par.enableRL or (par.enableRL and par.RL_mode == 1):
            if gv.t > (self.a3StartingDayReduction + par.a3_reductionDuration):
                self.a3StartingDayReduction = gv.t
                if gv.infected_attendance < (par.a3_InfectedTreshold * par.n_persons) or par.enableRL:
                    proceed = True
        else:
            proceed = False

        
        if proceed:
            self.operationsArr.remove("a3EndCheck")
            self.operationsArr.append("a3InitCheck")
            gv.a3_is_active = False
            self.action_is_active = False
            if par.enableRL and par.RL_mode == 1: self.update_RL_q_table(par, gv)
            if par.enableRL and par.RL_mode == 2: self.update_RL_q_table_mode2(par, gv)
                


    def update_RL_q_table(self, par, gv):
        state = self.current_RL_data['state']
        action = self.current_RL_data['action']
        
        if action == 0:
            cost_u = par.a1_cost
            revenues_u = par.a1_reduction_revenues
        if action == 1:
            #utlità = alpha * costo_economico + (beta * numero_contagiati)
            cost_u = par.a2_cost
            revenues_u = par.a2_reduction_revenues
        if action == 2:
            cost_u = par.a3_cost
            revenues_u = par.a3_reduction_revenues
        

        n_i_h = gv.new_infected_history
        r_a_h = gv.recovered_agents_history
        n_i_h_c = sum(n_i_h[self.current_RL_data['start_date'] : (gv.t - 1)])
        r_a_h_c = sum(r_a_h[self.current_RL_data['start_date'] : (gv.t - 1)])
        
        revenues = r_a_h_c * revenues_u
        costs = n_i_h_c * cost_u 

        reward = revenues - costs
        
        gv.q_table[state][action] = gv.q_table[state][action] + (par.alpha_RL * reward)

    # RL Mode 2
        

    def general_init(self, gv):
        self.PM_interactionCounter += 1
        self.aStartingDayReduction = gv.t
        self.action_is_active = True
        self.operationsArr.remove("aInitCheck")
        self.operationsArr.append("aEndCheck")

    def general_end(self):
        self.operationsArr.append("aInitCheck")
        self.operationsArr.remove("aEndCheck")
        self.action_is_active = False
        

    def a1Init_mode2(self, par, gv):
        gv.actualCapacity = par.capacity * (1 - par.a1_reductionPerc)
        gv.a1_is_active = True

    def a2Init_mode2(self, par, gv):
        gv.a2_is_active = True

    def a3Init_mode2(self, par, gv):
        gv.a3_is_active = True

    def aEnd_mode2(self, par, gv):
        
        if gv.t > (self.aStartingDayReduction + par.a_reductionDuration):

            dict_actions = self.current_RL_data['dict_action']

            self.general_end()

            if dict_actions[0] == 1 and gv.a1_is_active:
                gv.actualCapacity = par.capacity
                gv.a1_is_active = False

            if dict_actions[1] == 1 and gv.a2_is_active:
                gv.a2_is_active = False

            if dict_actions[2] == 1 and gv.a3_is_active:
                gv.a3_is_active = False

            self.update_RL_q_table_mode2(par, gv)

    def general_for_day(self, par, gv):
        
        if gv.a1_is_active:
            gv.a1_is_active_history.append(1)
        else:
            gv.a1_is_active_history.append(0)
        
        if gv.a2_is_active:
            gv.a2History_x.append(gv.t)
            gv.a2History_y.append(- (par.n_persons * 0.05))
            gv.a2_is_active_history.append(1)
        else:
            gv.a2_is_active_history.append(0)

        if gv.a3_is_active:
            gv.a3History_x.append(gv.t)
            gv.a3History_y.append(- (par.n_persons * 0.1))
            gv.a3_is_active_history.append(1)
        else:
            gv.a3_is_active_history.append(0)

    def update_RL_q_table_mode2(self, par, gv):
        action = self.current_RL_data['action']
        state = self.current_RL_data['state']
        dict_actions = self.current_RL_data['dict_action']

        cost_u = 0
        revenues_u = 0
        if dict_actions[0] == 1:
            cost_u += par.a1_cost
            revenues_u += par.a1_reduction_revenues
        if dict_actions[1] == 1:
            #utlità = alpha * costo_economico + (beta * numero_contagiati)
            cost_u += par.a2_cost
            revenues_u += par.a2_reduction_revenues
        if dict_actions[2] == 1:
            cost_u += par.a3_cost
            revenues_u += par.a3_reduction_revenues

        n_i_h = gv.new_infected_history
        r_a_h = gv.recovered_agents_history
        n_i_h_c = sum(n_i_h[self.current_RL_data['start_date'] : (gv.t - 1)])
        r_a_h_c = sum(r_a_h[self.current_RL_data['start_date'] : (gv.t - 1)])
        
        revenues = r_a_h_c * revenues_u
        costs = n_i_h_c * cost_u 

        reward = revenues - costs

        gv.q_table[state][action] = gv.q_table[state][action] + (par.alpha_RL * reward)


    def operationForDay(self, par, gv):
        
        if not par.enableRL:
            
            if "a1EndCheck" in self.operationsArr:
                self.a1Init_capacityReductionEnd(par, gv)
            if "a1InitCheck" in self.operationsArr:
                self.a1Init_capacityReductionInit(par, gv)
            
            if "a2EndCheck" in self.operationsArr:
                self.a2Init_faceMaskEnd(par, gv)
            if "a2InitCheck" in self.operationsArr:
                self.a2Init_faceMaskInit(par, gv)
            
            if "a3EndCheck" in self.operationsArr:
                self.a3Init_entranceTestEnd(par, gv)
            if "a3InitCheck" in self.operationsArr:
                self.a3Init_entranceTestInit(par, gv)
            
            

           
        elif par.RL_mode == 1:

            if "a1EndCheck" in self.operationsArr:
                self.a1Init_capacityReductionEnd(par, gv)
            if "a2EndCheck" in self.operationsArr:
                self.a2Init_faceMaskEnd(par, gv)
            if "a3EndCheck" in self.operationsArr:
                self.a3Init_entranceTestEnd(par, gv)
            
            
            if not self.action_is_active:
                
                infected_on_total = gv.infected_attendance / par.n_persons

                if infected_on_total >= 0 and infected_on_total < 0.25: quart_t = 0
                elif infected_on_total >= 0.25 and infected_on_total < 0.5: quart_t = 1
                elif infected_on_total >= 0.5 and infected_on_total < 0.75: quart_t = 2
                elif infected_on_total >= 0.75 and infected_on_total <= 1: quart_t = 3

                quart_st_arr = [0, 3, 6, 9]
                quart_st = quart_st_arr[quart_t]
                

                slope = round(gv.regCoeff_q_learning(par)[0], 3)
                if slope > 0: slope_t = 0
                elif slope == 0: slope_t = 1
                elif slope < 0: slope_t = 2
                
                state = quart_st + slope_t
                
                q_table_i = gv.q_table[state]

                if np.max(q_table_i) == 0:
                    action = random.choice(self.aviable_strategies)
                else:
                    if random.random() >= par.epsilon_RL:
                        action = random.choice(self.aviable_strategies)
                    else:    
                        action = np.argmax(q_table_i)
                

                if action == 0:
                    self.a1Init_capacityReductionInit(par, gv)
                if action == 1:
                    self.a2Init_faceMaskInit(par, gv)                    
                if action == 2:
                    self.a3Init_entranceTestInit(par, gv)
                    
                

                self.current_RL_data = {
                    'start_date': (gv.t - 1),
                    'state': state,
                    'action': action,
                }
            
                
        else:
            
            self.general_for_day(par, gv)
            
            if "aEndCheck" in self.operationsArr:
                self.aEnd_mode2(par, gv)

            if "aInitCheck" in self.operationsArr and gv.infected_attendance > 0 and gv.t > par.RL_PM_t_min:
                    
                infected_on_total = gv.infected_attendance / par.n_persons

                if infected_on_total >= 0 and infected_on_total < 0.25: quart_t = 0
                elif infected_on_total >= 0.25 and infected_on_total < 0.5: quart_t = 1
                elif infected_on_total >= 0.5 and infected_on_total < 0.75: quart_t = 2
                elif infected_on_total >= 0.75 and infected_on_total <= 1: quart_t = 3

                quart_st_arr = [0, 3, 6, 9]
                quart_st = quart_st_arr[quart_t]
                

                slope = round(gv.regCoeff_q_learning(par)[0], 3)
                if slope > 0: slope_t = 0
                elif slope == 0: slope_t = 1
                elif slope < 0: slope_t = 2
                
                state = quart_st + slope_t

                current_dict = PM.__RL_Full_Actions

                
                if gv.a1_is_active:
                    if 0 in current_dict.keys(): current_dict.pop(0)
                    if 2 in current_dict.keys(): current_dict.pop(2)
                    if 3 in current_dict.keys(): current_dict.pop(3)
                    if 6 in current_dict.keys(): current_dict.pop(6)

                
                if gv.a2_is_active:
                    if 0 in current_dict.keys(): current_dict.pop(0)
                    if 1 in current_dict.keys(): current_dict.pop(1)
                    if 3 in current_dict.keys(): current_dict.pop(3)
                    if 5 in current_dict.keys(): current_dict.pop(5)
                
                
                if gv.a3_is_active:
                    if 0 in current_dict.keys(): current_dict.pop(0)
                    if 1 in current_dict.keys(): current_dict.pop(1)
                    if 2 in current_dict.keys(): current_dict.pop(2)
                    if 4 in current_dict.keys(): current_dict.pop(4)

                

                q_table_i = gv.q_table[state]

                if np.max(q_table_i) == 0:
                    action = random.choice(list(current_dict.keys()))
                    # print('Action on random zero: ', action)
                else:
                    if random.random() >= par.epsilon_RL:
                        action = random.choice(list(current_dict.keys()))
                        # print('Action on random: ', action)
                    else:    
                        action = 0
                        current_max = 0
                        for i, el in enumerate(q_table_i):
                            
                            if i in current_dict.keys() and el > current_max:
                                current_max = el
                                action = i
                        # print('Action on max: ', action)

                
                

                if current_dict[action][0] == 1:
                    self.a1Init_mode2(par, gv)
                if current_dict[action][1] == 1:
                    self.a2Init_mode2(par, gv)                    
                if current_dict[action][2] == 1:
                    self.a3Init_mode2(par, gv)

                if current_dict[action][0] != 0 or current_dict[action][1] != 0 or current_dict[action][2] != 0:
                    self.general_init(gv)

                self.current_RL_data = {
                    'start_date': (gv.t - 1),
                    'state': state,
                    'action': action,
                    'dict_action': current_dict[action]
                }

                