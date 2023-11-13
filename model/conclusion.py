#import libraries
import matplotlib.pyplot as plt

class conclusions:

    def __init__(self) -> None:
        pass

    def Chart(self, par, gv, max_line: bool = True):
        arr_x = []
        for i in range(1, len(gv.attendance_history) + 1):
            arr_x.append(i)
        plt.plot(arr_x, gv.attendance_history, label=f"People in the bar every week\nAgents treshold: {par.threshold * par.n_persons}")
        plt.plot(arr_x, gv.contagious_history, label=f"Contagious people ({par.infection_duration} weeks)\nContagious treshold: {par.infection_threshold * par.n_persons}")
        plt.plot(arr_x, gv.present_contagious_history, label=f"Contagious people level in bar\nContagious treshold (not present): {par.infection_thresholdNotPresent * par.n_persons}")
        if max_line:
            plt.plot(arr_x, gv.capacityHistory, color="red", label=f"Maximum capacity: {par.capacity}")
        plt.legend(loc="upper left", bbox_to_anchor=(0.175, -0.1), ncol=1)
        plt.tight_layout()
        plt.show()







