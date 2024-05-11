import os
from model.MODEL import model
import numpy as np
import warnings
from datetime import datetime
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

class mt:
    
    def __init__(self):
        
        self.runs = 2
        self.starting_epsilon_RL = 0.2


        self.start_time = datetime.now()

    def end(self):
        self.end_time = datetime.now()
        time = (self.end_time - self.start_time)
        time_seconds = time.total_seconds()
        hour = int(time_seconds // 3600)
        minutes = int((time_seconds % 3600) // 60)
        seconds = int(time_seconds % 60)
        milliseconds = time.microseconds // 1000   
        print(f'Epoch simulation in: {hour}:{minutes}:{seconds}:{milliseconds}')     

    def run_epoch(self):

        runs = self.runs
        epsilon_RL = self.starting_epsilon_RL
        starting_epsilon_RL = self.starting_epsilon_RL
        starting_folder = 0
        ending_folder = 0

        epoch_dict = {
            'Epoch': [],
            'Attendance': [],
            'Contagion': [],
            'Present contagion': [],
            'A1': [],
            'A2': [],
            'A3': [],
            'Action on random': [],
            'Action on random zero': [],
            'Action on max': [],
            'Actions': [],
            'A1 cost': [],
            'A2 cost': [],
            'A3 cost': [],
            'Action cost': [],
            'New infections': [],
            'New infected cost': [],
            'Total cost': [], 
            'Total revenues': [],
            'Epoch txt': f'\n------- Epochs: {200}, Starting Epsilon: {starting_epsilon_RL} -----------------------------------------------------------------------------\n\n'
        }

        for i in range(0, runs):
            
            seed = np.random.randint(1000000)
            mod = model(seed, is_epoch=True)
            mod.par.draw_conclusions = False
            mod.par.save_conclusions = True


            if i == 0:
                mod.par.clear_q_table_memory = True
            else:
                mod.par.clear_q_table_memory = False

            
            if i < int(runs * 0.625): epsilon_RL += (1 - starting_epsilon_RL) / int(runs * 0.625)
            mod.par.epsilon_RL = epsilon_RL

            
            mod.run(seed)
            
            epoch_dict['Epoch'].append(i + 1)
            epoch_dict['Attendance'].append(sum(mod.gv.attendance_history))
            epoch_dict['Contagion'].append(sum(mod.gv.contagious_history))
            epoch_dict['Present contagion'].append(sum(mod.gv.present_contagious_history))
            epoch_dict['A1'].append(sum(mod.gv.a1_is_active_history))
            epoch_dict['A2'].append(sum(mod.gv.a2_is_active_history))
            epoch_dict['A3'].append(sum(mod.gv.a3_is_active_history))
            epoch_dict['Action on random'].append(sum(mod.gv.action_on_random))
            epoch_dict['Action on random zero'].append(sum(mod.gv.action_on_random_zero))
            epoch_dict['Action on max'].append(sum(mod.gv.action_on_max))
            epoch_dict['Actions'].append(sum(mod.gv.action_on_random) + sum(mod.gv.action_on_random_zero) + sum(mod.gv.action_on_max))
            epoch_dict['A1 cost'].append(sum(mod.gv.a1_cost_history))
            epoch_dict['A2 cost'].append(sum(mod.gv.a2_cost_history))
            epoch_dict['A3 cost'].append(sum(mod.gv.a3_cost_history))
            epoch_dict['Action cost'].append(sum(mod.gv.C_a_cost_history))
            epoch_dict['New infections'].append(sum(mod.gv.new_infected_history))
            epoch_dict['New infected cost'].append(sum(mod.gv.C_n_i_cost_history))
            epoch_dict['Total cost'].append(sum(mod.gv.C_cost_history))
            epoch_dict['Total revenues'].append(sum(mod.gv.R_revenues_history))
            
            if i == 0:
                starting_folder = mod.gv.epoch_id

            string_to_print = f' - Run ({mod.gv.epoch_id}) {i + 1} / {str(runs)} excecuted, epsilon {epsilon_RL}, random actions {sum(mod.gv.action_on_random)}, random actions on zero {sum(mod.gv.action_on_random_zero)}, max actions {sum(mod.gv.action_on_max)}'
            epoch_dict['Epoch txt'] += f'\n{string_to_print}'
            
            if i == (runs - 1):
                ending_folder = mod.gv.epoch_id
                mod.cl.save_epoch(mod.par, mod.gv, starting=starting_folder, ending=ending_folder)
                mod.cl.epoch_CSV_data(epoch_dict=epoch_dict, runs=runs)
                mod.cl.epoch_Chart_save(epoch_dict=epoch_dict, runs=runs)
        
            print(string_to_print)
    
        self.end()

    def run_epoch_cost(self, cost):

        runs = self.runs
        epsilon_RL = self.starting_epsilon_RL
        starting_epsilon_RL = self.starting_epsilon_RL
        starting_folder = 0
        ending_folder = 0

        epoch_dict = {
            'Epoch': [],
            'Attendance': [],
            'Contagion': [],
            'Present contagion': [],
            'A1': [],
            'A2': [],
            'A3': [],
            'Action on random': [],
            'Action on random zero': [],
            'Action on max': [],
            'Actions': [],
            'A1 cost': [],
            'A2 cost': [],
            'A3 cost': [],
            'Action cost': [],
            'New infections': [],
            'New infected cost': [],
            'Total cost': [], 
            'Total revenues': [],
            'Epoch txt': f'\n------- Epochs: {200}, Starting Epsilon: {starting_epsilon_RL} -----------------------------------------------------------------------------\n\n'
        }

        for i in range(0, runs):
            
            plt.close('all')

            seed = np.random.randint(1000000)
            mod = model(seed, is_epoch=True)
            mod.par.draw_conclusions = False
            mod.par.save_conclusions = True
            
            # Parameter to edit
            mod.par.a2_cost = cost


            if i == 0:
                mod.par.clear_q_table_memory = True
            else:
                mod.par.clear_q_table_memory = False

            
            if i < int(runs * 0.625): epsilon_RL += (1 - starting_epsilon_RL) / int(runs * 0.625)
            mod.par.epsilon_RL = epsilon_RL

            
            mod.run(seed)
            
            epoch_dict['Epoch'].append(i + 1)
            epoch_dict['Attendance'].append(sum(mod.gv.attendance_history))
            epoch_dict['Contagion'].append(sum(mod.gv.contagious_history))
            epoch_dict['Present contagion'].append(sum(mod.gv.present_contagious_history))
            epoch_dict['A1'].append(sum(mod.gv.a1_is_active_history))
            epoch_dict['A2'].append(sum(mod.gv.a2_is_active_history))
            epoch_dict['A3'].append(sum(mod.gv.a3_is_active_history))
            epoch_dict['Action on random'].append(sum(mod.gv.action_on_random))
            epoch_dict['Action on random zero'].append(sum(mod.gv.action_on_random_zero))
            epoch_dict['Action on max'].append(sum(mod.gv.action_on_max))
            epoch_dict['Actions'].append(sum(mod.gv.action_on_random) + sum(mod.gv.action_on_random_zero) + sum(mod.gv.action_on_max))
            epoch_dict['A1 cost'].append(sum(mod.gv.a1_cost_history))
            epoch_dict['A2 cost'].append(sum(mod.gv.a2_cost_history))
            epoch_dict['A3 cost'].append(sum(mod.gv.a3_cost_history))
            epoch_dict['Action cost'].append(sum(mod.gv.C_a_cost_history))
            epoch_dict['New infections'].append(sum(mod.gv.new_infected_history))
            epoch_dict['New infected cost'].append(sum(mod.gv.C_n_i_cost_history))
            epoch_dict['Total cost'].append(sum(mod.gv.C_cost_history))
            epoch_dict['Total revenues'].append(sum(mod.gv.R_revenues_history))
            
            if i == 0:
                starting_folder = mod.gv.epoch_id

            string_to_print = f' - Run ({mod.gv.epoch_id}) {i + 1} / {str(runs)} excecuted, epsilon {epsilon_RL}, random actions {sum(mod.gv.action_on_random)}, random actions on zero {sum(mod.gv.action_on_random_zero)}, max actions {sum(mod.gv.action_on_max)}'
            epoch_dict['Epoch txt'] += f'\n{string_to_print}'
            
            if i == (runs - 1):
                ending_folder = mod.gv.epoch_id
                mod.cl.save_epoch(mod.par, mod.gv, starting=starting_folder, ending=ending_folder)
                mod.cl.epoch_CSV_data(epoch_dict=epoch_dict, runs=runs)
                mod.cl.epoch_Chart_save(epoch_dict=epoch_dict, runs=runs)
        
            print(string_to_print)
    
        self.end()

    def run_epoch_parameter_to_change(self, cost_1, cost_2):
        for i in range(cost_1, cost_2 + 1):
            self.run_epoch_cost(i)

    def run(self):
        
        seed = np.random.randint(1000000)
        mod = model(seed, is_epoch=False)
        mod.par.draw_conclusions = False
        mod.par.save_conclusions = True

if __name__ == '__main__':
    mt = mt()
    mt.run_epoch_parameter_to_change(2, 5)