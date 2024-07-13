#import libraries
import numpy as np
import random
import matplotlib.pyplot as plt

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

        # With already used action 3
        8: (0, 0, 1),
        9: (1, 0, 1),
        10: (0, 1, 1),
        11: (1, 1, 1),
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
        self.states_actions_history = []

    
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
        
        revenues = sum(gv.R_revenues_history[self.current_RL_data['start_date'] : (gv.t - 1)])
        costs = sum(gv.C_cost_history[self.current_RL_data['start_date'] : (gv.t - 1)])

        reward = revenues - costs
        
        gv.q_table[state][action] = gv.q_table[state][action] + (par.alpha_RL * reward)
        self.states_actions_history.append([state, action])

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
        gv.a3_used_at_least_once = True

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

    def get_state(self, par, gv, infected_on_total = 0, slope_pre = True):
        
        if infected_on_total == 0: infected_on_total = gv.infected_attendance / par.n_persons
        else: infected_on_total = infected_on_total

        if infected_on_total >= 0 and infected_on_total < 0.25: quart_t = 0
        elif infected_on_total >= 0.25 and infected_on_total < 0.5: quart_t = 1
        elif infected_on_total >= 0.5 and infected_on_total < 0.75: quart_t = 2
        elif infected_on_total >= 0.75: quart_t = 3
        else:
            print(f'Error in get_state:\n - f1: {infected_on_total >= 0 and infected_on_total < 0.25}\n - f2: {infected_on_total >= 0.25 and infected_on_total < 0.5}\n - f3: {infected_on_total >= 0.5 and infected_on_total < 0.75}\n - f4: {infected_on_total >= 0.75}\n - infected_on_total: {infected_on_total}')

        quart_st_arr = [0, 3, 6, 9]
        quart_st = quart_st_arr[quart_t]
        
        if slope_pre == True: slope = round(gv.regCoeff_q_learning(par)[0], 3)
        else: slope = slope_pre

        if slope > 0: slope_t = 0
        elif slope == 0: slope_t = 1
        elif slope < 0: slope_t = 2
        
        state = quart_st + slope_t

        return state
    
    def predict_future_state(self, par, gv):
        
        infection_data = gv.contagious_history[-par.RL_PM_t_min:]
        
        infection_regr = gv.regLine(par, infection_data, par.RL_PM_t_min * 2)

        infection_regr_last = infection_regr[-1]
        if infection_regr[-1] < 0: infection_regr_last = 0    
        if infection_regr[-1] > par.n_persons: infection_regr_last = par.n_persons    
        
        infected_on_total = infection_regr_last / par.n_persons

        # slope = round(gv.regCoeff_q_learning(par, int(par.RL_PM_t_min / 5), infection_regr)[0], 3)
        slope = round(gv.regCoeff_q_learning(par, int(par.RL_PM_t_min / 7), infection_data)[0], 3)
        # print(slope)
        # plt.plot(infection_regr)
        # plt.plot(infection_data)
        # plt.show()

        future_state = self.get_state(par, gv, infected_on_total, slope)

        gv.txt_output += f'\n  - Future state: {future_state}, Slope {slope}, Infected on totale {infected_on_total}, effect on q-table:'
        
        return future_state

    def update_RL_q_table_mode2(self, par, gv):
        action = self.current_RL_data['action']
        state = self.current_RL_data['state']
        dict_actions = self.current_RL_data['dict_action']

        revenues = sum(gv.R_revenues_history[self.current_RL_data['start_date'] : (gv.t - 1)])
        costs = sum(gv.C_cost_history[self.current_RL_data['start_date'] : (gv.t - 1)])



        

        #if action == 0: print(sum(gv.C_n_i_cost_history[self.current_RL_data['start_date'] : (gv.t - 1)]))

        reward = revenues - costs

        
        prev = gv.q_table[state][action]
        gv.q_table[state][action] = (gv.q_table[state][action] * (1 - par.alpha_RL)) + (par.alpha_RL * reward)
        self.states_actions_history.append([state, action])
        gv.txt_output += f'\n\n  - Updating Q-Table: ({action}, {state}) (a, s)\n    Old: {prev}, Next: {gv.q_table[state][action]}, Costs: {costs}, Revenues {revenues}'
        #print(gv.t, gv.q_table[state][action], state, action, gv.q_table[state])
        #print('\n\n')

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
                

                slope = round(gv.regCoeff_q_learning(par)[0])
                
                if slope > 0: slope_t = 0
                elif slope == 0: slope_t = 1
                elif slope < 0: slope_t = 2
                
                state = quart_st + slope_t
                
                q_table_i = gv.q_table[state]

                gv.txt_output += f'\n\n - PM RL Mode 1'

                if np.max(q_table_i) == 0:
                    action = random.choice(self.aviable_strategies)

                    gv.txt_output += f'\n  - Action on random zero: {action}, State {state}, Aviable {self.aviable_strategies}, q-table: {q_table_i}'

                    gv.action_on_max.append(0)
                    gv.action_on_random_zero.append(1)
                    gv.action_on_random.append(0)
                else:
                    if random.random() >= par.epsilon_RL:
                        action = random.choice(self.aviable_strategies)

                        gv.txt_output += f'\n  - Action on random: {action}, State {state}, Aviable {self.aviable_strategies}, q-table: {q_table_i}'

                        gv.action_on_max.append(0)
                        gv.action_on_random_zero.append(0)
                        gv.action_on_random.append(1)
                    else:    
                        action = np.argmax(q_table_i)

                        gv.txt_output += f'\n  - Action on max: {action}, State {state}, Aviable {self.aviable_strategies}, q-table: {q_table_i}'

                        gv.action_on_max.append(1)
                        gv.action_on_random_zero.append(0)
                        gv.action_on_random.append(0)

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

                gv.txt_output += f'\n  - Current RL data: {self.current_RL_data}'
            
            else:
                gv.action_on_max.append(0)
                gv.action_on_random_zero.append(0)
                gv.action_on_random.append(0)
                
        else:
            
            
            
            if "aEndCheck" in self.operationsArr:
                self.aEnd_mode2(par, gv)
            
            self.general_for_day(par, gv)

            if "aInitCheck" in self.operationsArr and gv.infected_attendance > 0 and gv.t > par.RL_PM_t_min:
                    
                infected_on_total = gv.infected_attendance / par.n_persons
                
                state = self.get_state(par, gv, infected_on_total)
                
                
                # Compile currenti dict
                current_dict = {}
                for el in PM.__RL_Full_Actions.keys():
                    current_dict[el] = PM.__RL_Full_Actions[el]
                
                # print(f'Pre: {current_dict.keys()}', PM.__RL_Full_Actions.keys())

                # If active

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

                # If active on parameters
                
                if not par.enableA1:
                    if 1 in current_dict.keys(): current_dict.pop(1)
                    if 4 in current_dict.keys(): current_dict.pop(4)
                    if 5 in current_dict.keys(): current_dict.pop(5)
                    if 7 in current_dict.keys(): current_dict.pop(7)

                
                if not par.enableA2:
                    if 2 in current_dict.keys(): current_dict.pop(2)
                    if 4 in current_dict.keys(): current_dict.pop(4)
                    if 6 in current_dict.keys(): current_dict.pop(6)
                    if 7 in current_dict.keys(): current_dict.pop(7)
                
                
                if not par.enableA3:
                    # print(f'Not enable A3')
                    if 3 in current_dict.keys(): current_dict.pop(3)
                    if 5 in current_dict.keys(): current_dict.pop(5)
                    if 6 in current_dict.keys(): current_dict.pop(6)
                    if 7 in current_dict.keys(): current_dict.pop(7)
                    if 8 in current_dict.keys(): current_dict.pop(8)
                    if 9 in current_dict.keys(): current_dict.pop(9)
                    if 10 in current_dict.keys(): current_dict.pop(10)
                    if 11 in current_dict.keys(): current_dict.pop(11)


                # If a3 already used save values in (8-10)
                
                if gv.a3_used_at_least_once:
                    # print(f'Tolgo 3-7 {gv.a3_used_at_least_once}')
                    if 3 in current_dict.keys(): current_dict.pop(3)
                    if 5 in current_dict.keys(): current_dict.pop(5)
                    if 6 in current_dict.keys(): current_dict.pop(6)
                    if 7 in current_dict.keys(): current_dict.pop(7)
                
                if not gv.a3_used_at_least_once:
                    # print(f'Tolgo 9-11 {gv.a3_used_at_least_once}')
                    if 8 in current_dict.keys(): current_dict.pop(8)
                    if 9 in current_dict.keys(): current_dict.pop(9)
                    if 10 in current_dict.keys(): current_dict.pop(10)
                    if 11 in current_dict.keys(): current_dict.pop(11)
                
                
                if par.enable_at_least_one_A:
                    if 0 in current_dict.keys(): current_dict.pop(0)

                q_table_i = gv.q_table[state]

                gv.txt_output += f'\n - PM RL Mode 2'

                # print(f'End: {current_dict.keys()}')

                q_table_real_zero = []
                for el in current_dict.keys():
                    if q_table_i[el] == 0:
                        q_table_real_zero.append(el)


                if len(q_table_real_zero) > 0:

                    
                    action_table_zero = []
                    for i, el in enumerate(q_table_i):
                        if el == 0 and i in current_dict.keys():
                            action_table_zero.append(i)
                    
                    if len(action_table_zero) == 0:
                        action_table_zero = list(current_dict.keys())
                   
                    action = random.choice(action_table_zero)
                    
                    
                    gv.txt_output += f'\n  - Action on random zero: {action}, State {state}, Aviable {action_table_zero}, q-table: {gv.q_table[state]}'
                    
                    gv.action_on_max.append(0)
                    gv.action_on_random_zero.append(1)
                    gv.action_on_random.append(0)
                else:
                    if random.random() >= par.epsilon_RL:
                        action = random.choice(list(current_dict.keys()))
                        
                        gv.txt_output += f'\n  - Action on random: {action}, State {state}, Aviable {current_dict.keys()}, q-table: {gv.q_table[state]}'

                        gv.action_on_max.append(0)
                        gv.action_on_random_zero.append(0)
                        gv.action_on_random.append(1)
                    else:    
                        action = 0
                        current_max = -10000000000000000000000
                        future_state = self.predict_future_state(par, gv)
                        for i, el in enumerate(q_table_i):
                            
                            if i in current_dict.keys():
                                c = el + gv.q_table[future_state][i]
                                
                                gv.txt_output += f'\n    - Action: {i}, State {state}, Element {el}, Future element {gv.q_table[future_state][i]}, Element + Future element {c}'
                                
                                if c > current_max:
                                    current_max = c  
                                    action = i

                        gv.action_on_max.append(1)
                        gv.action_on_random_zero.append(0)
                        gv.action_on_random.append(0)
                        gv.txt_output += f'\n  - Action on max: {action}, State {state}, Aviable {current_dict.keys()}, current max: {current_max}, q-table: {gv.q_table[state]}'
                        
                
                

                if current_dict[action][0] == 1:
                    self.a1Init_mode2(par, gv)
                if current_dict[action][1] == 1:
                    self.a2Init_mode2(par, gv)                    
                if current_dict[action][2] == 1:
                    self.a3Init_mode2(par, gv)

    
                self.general_init(gv)

                self.current_RL_data = {
                    'start_date': (gv.t - 1),
                    'state': state,
                    'action': action,
                    'dict_action': current_dict[action]
                }

                gv.txt_output += f'\n  - Current RL data: {self.current_RL_data}'
            
            else:
                gv.action_on_max.append(0)
                gv.action_on_random_zero.append(0)
                gv.action_on_random.append(0)


    # Old
    def update_qTable_on_totals(self, par, gv):
        
        total_cost_sum = -1 * (sum(gv.C_a_cost_history) + (sum(gv.C_n_i_cost_history) * par.infections_on_total_action_RL))
        
        gv.txt_output += f'\n\n  - Q-Table totals update (Total cost sum: {total_cost_sum}):'

        for el in self.states_actions_history:
            state = el[0]
            action = el[1]
            prev = gv.q_table[state][action]
            gv.q_table[state][action] = (gv.q_table[state][action] * (1 - par.alpha_RL)) + ((total_cost_sum * par.total_on_action_RL) * par.alpha_RL)
            gv.txt_output += f'\n    - ({state}, {action}): {prev} -> {gv.q_table[state][action]}'
            