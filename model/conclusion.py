#import libraries
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import json

class conclusions:

    def __init__(self, par) -> None:
        self.base_folder = self.get_base_folder()
        self.folder_number = self.get_folder_n()
        self.folder_location = f'{self.base_folder}/output/{self.folder_number}'
        if par.save_conclusions: os.mkdir(self.folder_location)

    def get_base_folder(self):
        cwd = os.getcwd()
        if cwd.split('/')[-1] != 'model':
            cwd += '/model'
        return cwd

    def get_folder_n(self):
        return (len(os.listdir(f'{self.base_folder}/output')) + 1)


    def Chart(self, par, gv, max_line: bool = True):
        arr_x = []
        for i in range(1, len(gv.attendance_history) + 1):
            arr_x.append(i)
        plt.plot(arr_x, gv.contagious_history, label=f"Infected people ({par.infection_duration} days)\nInfection treshold: {par.infection_threshold}", color="#e69b10")
        plt.plot(arr_x, gv.present_contagious_history, label=f"Infected people level in bar\nInfection treshold (not present): {par.infection_thresholdNotPresent}", color="#06d45c")
        plt.plot(arr_x, gv.new_infected_history, label=f"New infected people per day\nAverage infected people per day {np.mean(gv.new_infected_history)}", color="#05a347")
        if par.enablePM and par.enableA1: pm_treshold_string = f"\nPM a1 treshold: {par.a1_InfectedTreshold}"
        else: pm_treshold_string = ""
        if max_line:
            plt.plot(arr_x, gv.capacityHistory, label=f"Final maximum capacity: {int(gv.actualCapacity)}{pm_treshold_string}", color="#e64d10")
        if par.enablePM and par.enableA2: 
            plt.scatter(gv.a2History_x, gv.a2History_y, s=10, label="Active PM a2 strategy (face masks)", color="#ad10e6")
        if par.enablePM and par.enableA3: 
            plt.scatter(gv.a3History_x, gv.a3History_y, s=10, label="Active PM a3 strategy (entrance test)", color="#bc6fd9")
        plt.plot(arr_x, gv.attendance_history, label=f"People in the bar every day\nAgents treshold: {par.threshold}", color="#09a9e3")
        plt.legend(loc="upper left", bbox_to_anchor=(0.175, -0.1), ncol=1)
        plt.tight_layout()
        if par.save_conclusions: plt.savefig(f'{self.folder_location}/simulation.png')
        if par.draw_conclusions: plt.show()
        


    def Chart_cost(self, par, gv):
        fig, axs = plt.subplots(4, 2, layout='constrained')

        axs[0, 0].plot(gv.R_revenues_history)
        axs[0, 0].set_xlabel('Time (s)')
        axs[0, 0].set_ylabel('Revenues')

        axs[0, 1].plot(gv.C_cost_history)
        axs[0, 1].set_xlabel('Time (s)')
        axs[0, 1].set_ylabel('Total costs')

        axs[1, 0].plot(gv.C_n_i_cost_history)
        axs[1, 0].set_xlabel('Time (s)')
        axs[1, 0].set_ylabel('New infection costs')

        axs[1, 1].plot(gv.C_a_cost_history)
        axs[1, 1].set_xlabel('Time (s)')
        axs[1, 1].set_ylabel('PM Actions costs')
       
        axs[2, 0].plot(gv.a1_cost_history)
        axs[2, 0].set_xlabel('Time (s)')
        axs[2, 0].set_ylabel('PM Action 1 costs')
      
        
        axs[2, 1].plot(gv.a2_cost_history)
        axs[2, 1].set_xlabel('Time (s)')
        axs[2, 1].set_ylabel('PM Action 2 costs')

        axs[3, 0].plot(gv.a3_cost_history)
        axs[3, 0].set_xlabel('Time (s)')
        axs[3, 0].set_ylabel('PM Action 3 costs')

        plt.subplots_adjust(wspace=0.0, hspace=10, right=0.7)
        if par.save_conclusions: plt.savefig(f'{self.folder_location}/costs.png')
        if par.draw_conclusions: plt.show()

    def CSV_data(self, par, gv):
        
        csv_dict = {
            't': gv.t_history,
            'Attendance': gv.attendance_history,
            'Contagion': gv.contagious_history,
            'Present contagion': gv.present_contagious_history,
            'New infections': gv.new_infected_history,
            'New infections cost': gv.C_n_i_cost_history,
            'Recovered': gv.recovered_agents_history,
            'Revenues': gv.R_revenues_history,
        }
        
        if par.enablePM:
            csv_dict['Capacity'] = gv.capacityHistory
            if par.enableA1:
                csv_dict['A1'] = gv.a1_is_active_history
                csv_dict['A1 cost'] = gv.a1_cost_history
            if par.enableA2:
                csv_dict['A2'] = gv.a2_is_active_history
                csv_dict['A2 cost'] = gv.a2_cost_history
            if par.enableA3:
                csv_dict['A3'] = gv.a3_is_active_history
                csv_dict['A3 cost'] = gv.a3_cost_history

            csv_dict['Total A costs'] = gv.C_a_cost_history
            csv_dict['Total costs'] = gv.C_cost_history
        

        with open(f'{self.folder_location}/data.csv', mode='w') as csvfile:
            fieldnames = csv_dict.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            rows = []
            for i in range(0, gv.t):
                row_dict = {}
                for key in csv_dict.keys():
                    row_dict[key] = csv_dict[key][i]
                rows.append(row_dict)
            
            writer.writerows(rows)

    def save_parameters(self, par):
        par_dict = par.__dict__
        with open(f'{self.folder_location}/parameters.json', 'w') as f:
            json.dump(par_dict, f)

    def save_current_q_table(self, gv):
        with open(f'{self.folder_location}/current_q_table.json', 'w') as f:
            json.dump(gv.export_q_table, f)