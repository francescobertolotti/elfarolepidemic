#import libraries
import matplotlib.pyplot as plt
import numpy as np

class conclusions:

    def __init__(self) -> None:
        pass

    def Chart(self, par, gv, max_line: bool = True):
        arr_x = []
        for i in range(1, len(gv.attendance_history) + 1):
            arr_x.append(i)
        plt.plot(arr_x, gv.contagious_history, label=f"Infected people ({par.infection_duration} days)\nInfection treshold: {par.infection_threshold}", color="#e69b10")
        plt.plot(arr_x, gv.present_contagious_history, label=f"Infected people level in bar\nInfection treshold (not present): {par.infection_thresholdNotPresent}", color="#06d45c")
        plt.plot(arr_x, gv.new_infected_history, label=f"New infected people per day\nAverage infected people per day {np.mean(gv.new_infected_history)}", color="#05a347")
        if par.enablePM: pm_treshold_string = f"\nPM a1 treshold: {par.a1_InfectedTreshold}"
        else: pm_treshold_string = ""
        if max_line:
            plt.plot(arr_x, gv.capacityHistory, label=f"Final maximum capacity: {int(gv.actualCapacity)}{pm_treshold_string}", color="#e64d10")
        plt.plot(arr_x, gv.attendance_history, label=f"People in the bar every day\nAgents treshold: {par.threshold}", color="#09a9e3")
        plt.legend(loc="upper left", bbox_to_anchor=(0.175, -0.1), ncol=1)
        plt.tight_layout()
        plt.show()







