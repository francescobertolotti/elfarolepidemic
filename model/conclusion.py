#import libraries
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import json
import shutil

class conclusions:

    def __init__(self, par, gv) -> None:
        self.base_folder = self.get_base_folder()
        self.folder_number = self.get_folder_n(gv)
        self.folder_location = f'{self.base_folder}/output/{self.folder_number}'

        self.output_location = f'{self.base_folder}/output'
        self.epoch_name = par.epoch_name
        self.folder_number_epoch = self.get_epoch_folder_n()
        self.folder_location_epoch = f'{self.base_folder}/output/{self.epoch_name}_{self.folder_number_epoch}'
        
        if par.save_conclusions: os.mkdir(self.folder_location)

    def get_base_folder(self):
        cwd = os.getcwd()
        if cwd.split('/')[-1] != 'model':
            cwd += '/model'
        return cwd

    def get_folder_n(self, gv):
        ls = os.listdir(f'{self.base_folder}/output')
        dir_arr = []
        for el in ls:
            try:
                int(el)
                dir_arr.append(int(str(el)))
            except:
                pass
                
        if len(dir_arr) > 0:
            n = max(dir_arr) + 1
        else:
            n = 1
        gv.epoch_id = n
        return n
    
    def get_epoch_folder_n(self):
        cont = 0
        for el in os.listdir(f'{self.base_folder}/output'):
            if self.epoch_name in el:
                cont += 1
        return (cont + 1)


    def Chart(self, par, gv, max_line: bool = True):
        arr_x = []
        for i in range(1, len(gv.attendance_history) + 1):
            arr_x.append(i)

        fig = plt.figure()
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
        plt.plot(arr_x, gv.recovered_agents_history, label=f"Recovered people every day", color="#00e5f2")
        plt.legend(loc="upper left", bbox_to_anchor=(0.175, -0.1), ncol=1)
        plt.tight_layout()
        if par.save_conclusions and par.save_chart: fig.savefig(f'{self.folder_location}/simulation.png')
        if par.draw_conclusions: plt.show()
        
        plt.clf()


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
        if par.save_conclusions and par.save_chart: fig.savefig(f'{self.folder_location}/costs.png')
        if par.draw_conclusions: plt.show()

        plt.clf()

    def CSV_data(self, par, gv):
        
        csv_dict = {}
        

        
        if gv.is_epoch:
            arr_epoch = [gv.epoch_id for i in range(0, par.max_days)]
            csv_dict['Epoch id'] = arr_epoch

        csv_dict['t'] = gv.t_history
        csv_dict['Attendance'] = gv.attendance_history
        csv_dict['Contagion'] = gv.contagious_history
        csv_dict['Present contagion'] = gv.present_contagious_history
        csv_dict['New infections'] = gv.new_infected_history
        csv_dict['New infections cost'] = gv.C_n_i_cost_history
        csv_dict['Recovered'] = gv.recovered_agents_history
        csv_dict['Revenues'] = gv.R_revenues_history


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

            if par.enableRL:
                csv_dict['Random action'] = gv.action_on_random
                csv_dict['Random action on zero'] = gv.action_on_random_zero
                csv_dict['Random on max'] = gv.action_on_max

            csv_dict['Total A costs'] = gv.C_a_cost_history
            csv_dict['Total costs'] = gv.C_cost_history

        self.csv_dict = csv_dict
        

        with open(f'{self.folder_location}/data.csv', mode='w') as csvfile:
            fieldnames = csv_dict.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not gv.is_epoch: writer.writeheader()
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
            json.dump(par_dict, f, indent=4)

    def save_txt_output(self, gv):
        with open(f'{self.folder_location}/txt_output.txt', 'w') as f:
            f.write(gv.txt_output)
        

    def save_current_q_table(self, gv):
        with open(f'{self.folder_location}/current_q_table.json', 'w') as f:
            json.dump(gv.export_q_table, f, indent=4)


    # Epoch export
    def epoch_condition_save(self, par, gv):
        par.save_conclusions = True
        self.base_folder = self.get_base_folder()
        self.folder_number = self.get_folder_n()
        self.folder_location = f'{self.base_folder}/output/{self.folder_number}'
        if par.save_conclusions: os.mkdir(self.folder_location)
        if par.save_conclusions and par.save_q_table: self.save_current_q_table(gv)
        if par.save_conclusions and not gv.is_epoch: self.save_parameters(par)
        self.CSV_data(par, gv)
        self.Chart(par, gv)
        self.Chart_cost(par, gv)

    def save_epoch(self, par, gv, starting, ending):
        
        os.mkdir(self.folder_location_epoch)
        os.mkdir(f'{self.folder_location_epoch}/simulation_data')
        
        for i in range(starting, ending + 1):
            shutil.move(f'{self.output_location}/{i}', f'{self.folder_location_epoch}/simulation_data')

        completed_data = []
        for i in range(starting, ending + 1):
            with open(f'{self.folder_location_epoch}/simulation_data/{i}/data.csv', newline='') as csv_file:
                reader = csv.reader(csv_file)
                completed_data.extend(reader)

        with open(f'{self.folder_location_epoch}/simulation_data.csv', 'w', newline='') as csv_output:
            writer = csv.writer(csv_output)
            writer.writerow(self.csv_dict.keys())
            writer.writerows(completed_data)

    def epoch_CSV_data(self, epoch_dict: dict, runs: int) -> None:
        with open(f'{self.folder_location_epoch}/epoch_data.csv', mode='w') as csvfile:
            fieldnames = epoch_dict.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            rows = []
            for i in range(0, runs):
                row_dict = {}
                for key in epoch_dict.keys():
                    row_dict[key] = str(epoch_dict[key][i]).replace('.', ',')
                rows.append(row_dict)
            writer.writerows(rows)

        with open(f'{self.folder_location_epoch}/epoch_txt_output.txt', mode='w') as f:
            f.write(epoch_dict['Epoch txt'])

    def epoch_Chart_save(self, epoch_dict: dict, runs: int) -> None:
    
        arr_x = []
        for i in range(1, runs + 1):
            arr_x.append(i)

        fig, axs = plt.subplots(8, 2, layout='constrained')

        fig.set_size_inches(10, 10)

        axs[0, 0].plot(epoch_dict['Total revenues'])
        axs[0, 0].set_xlabel('Epoch')
        axs[0, 0].set_ylabel('Total revenues')

        axs[0, 1].plot(epoch_dict['Total cost'])
        axs[0, 1].set_xlabel('Epoch')
        axs[0, 1].set_ylabel('Total cost')

        axs[1, 0].plot(epoch_dict['New infected cost'])
        axs[1, 0].set_xlabel('Epoch')
        axs[1, 0].set_ylabel('New infected cost')

        axs[1, 1].plot(epoch_dict['Action cost'])
        axs[1, 1].set_xlabel('Epoch')
        axs[1, 1].set_ylabel('PM Actions costs')
       
        axs[2, 0].plot(epoch_dict['A1 cost'])
        axs[2, 0].set_xlabel('Epoch')
        axs[2, 0].set_ylabel('PM A1 costs')
        
        axs[2, 1].plot(epoch_dict['A2 cost'])
        axs[2, 1].set_xlabel('Epoch')
        axs[2, 1].set_ylabel('PM A2 costs')

        axs[3, 0].plot(epoch_dict['A3 cost'])
        axs[3, 0].set_xlabel('Epoch')
        axs[3, 0].set_ylabel('PM A3 costs')

        axs[3, 1].plot(epoch_dict['Actions'])
        axs[3, 1].set_xlabel('Epoch')
        axs[3, 1].set_ylabel('PM A')

        axs[4, 0].plot(epoch_dict['Action on max'])
        axs[4, 0].set_xlabel('Epoch')
        axs[4, 0].set_ylabel('A on max')

        axs[4, 1].plot(epoch_dict['Action on random zero'])
        axs[4, 1].set_xlabel('Epoch')
        axs[4, 1].set_ylabel('A on random zero')

        axs[5, 0].plot(epoch_dict['Action on random'])
        axs[5, 0].set_xlabel('Epoch')
        axs[5, 0].set_ylabel('A on random')

        axs[5, 1].plot(epoch_dict['A1'])
        axs[5, 1].set_xlabel('Epoch')
        axs[5, 1].set_ylabel('PM A1 days')

        axs[6, 0].plot(epoch_dict['A2'])
        axs[6, 0].set_xlabel('Epoch')
        axs[6, 0].set_ylabel('PM A2 days')

        axs[6, 1].plot(epoch_dict['A3'])
        axs[6, 1].set_xlabel('Epoch')
        axs[6, 1].set_ylabel('PM A3 days')

        axs[7, 0].plot(epoch_dict['Present contagion'])
        axs[7, 0].set_xlabel('Epoch')
        axs[7, 0].set_ylabel('Present contagion')

        plt.subplots_adjust(wspace=0.0, hspace=10, right=0.7)
        fig.savefig(f'{self.folder_location_epoch}/epoch_plots.png')
        
        plt.clf()
        fig = plt.figure()
        plt.plot(arr_x, epoch_dict['Contagion'], label=f"Infected people in epochs", color="#e69b10")
        fig.savefig(f'{self.folder_location_epoch}/epoch_contagion.png')


        plt.clf()
        fig = plt.figure()
        plt.plot(arr_x, epoch_dict['Attendance'], label=f"Bar attendance in epochs", color="#09a9e3")
        fig.savefig(f'{self.folder_location_epoch}/epoch_attendance.png')