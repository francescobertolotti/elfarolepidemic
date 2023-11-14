#import libraries
import matplotlib.pyplot as plt

class conclusions:

    def __init__(self) -> None:
        pass

    def Chart(self, par, gv, max_line: bool = True):
        arr_x = []
        for i in range(1, len(gv.attendance_history) + 1):
            arr_x.append(i)
        plt.plot(arr_x, gv.attendance_history, label=f"People in the bar every week\nAgents treshold: {par.threshold}")
        plt.plot(arr_x, gv.contagious_history, label=f"Contagious people ({par.infection_duration} weeks)\nContagious treshold: {par.infection_threshold}")
        plt.plot(arr_x, gv.present_contagious_history, label=f"Contagious people level in bar\nContagious treshold (not present): {par.infection_thresholdNotPresent}")
        if par.enablePM: pm_treshold_string = f"\nPM a1 treshold: {par.a1_InfectedTreshold}"
        else: pm_treshold_string = ""
        if max_line:
            plt.plot(arr_x, gv.capacityHistory, color="red", label=f"Maximum capacity: {par.capacity}{pm_treshold_string}")
        plt.legend(loc="upper left", bbox_to_anchor=(0.175, -0.1), ncol=1)
        plt.tight_layout()
        plt.show()







