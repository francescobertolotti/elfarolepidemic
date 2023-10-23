#import libraries
import matplotlib.pyplot as plt

class conclusions:

    def __init__(self) -> None:
        pass

    def Chart(self, par, gv, max_line: bool = True, threshold_line: bool = True, cont_threshold_line: bool = True, contNotPres_threshold_line: bool = True):
        arr_x = []
        for i in range(1, len(gv.attendance_history) + 1):
            arr_x.append(i)
        plt.plot(arr_x, gv.attendance_history, label="People in the bar every week")
        plt.plot(arr_x, gv.contagious_history, label="Contagious people (%d weeks)" % par.contagious_duration)
        plt.plot(arr_x, gv.present_contagious_history, label="Contagious people level in bar")
        if max_line:
            line_max = plt.Line2D((0, arr_x[len(arr_x) - 1]), (par.capacity, par.capacity), color="red", label=f"Maximum capacity: {par.capacity}")
            plt.gca().add_line(line_max)
        if threshold_line:
            line_threshold = plt.Line2D((0, arr_x[len(arr_x) - 1]), (par.threshold * par.n_persons, par.threshold * par.n_persons), color="green", label=f"Agents treshold: {par.threshold * par.n_persons}")
            plt.gca().add_line(line_threshold)
        if cont_threshold_line:
            line_threshold = plt.Line2D((0, arr_x[len(arr_x) - 1]), (par.contagious_threshold * par.n_persons, par.contagious_threshold * par.n_persons), color="blue", label=f"Contagious treshold: {par.contagious_threshold * par.n_persons}")
            plt.gca().add_line(line_threshold)
        if contNotPres_threshold_line:
            line_threshold = plt.Line2D((0, arr_x[len(arr_x) - 1]), (par.contagious_thresholdNotPresent * par.n_persons, par.contagious_thresholdNotPresent * par.n_persons), color="lightblue", label=f"Contagious treshold (not present): {par.contagious_thresholdNotPresent * par.n_persons}")
            plt.gca().add_line(line_threshold)
        plt.legend(loc="upper left", bbox_to_anchor=(-0.15,1.25), ncol=2)
        plt.tight_layout()
        plt.show()







