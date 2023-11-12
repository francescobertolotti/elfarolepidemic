import matplotlib.pyplot as plt 
import numpy as np

arr_x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])


arr_y = np.array([1.3, 1.2, 1.5, 2.1, 2.4, 2.1, 2.2, 2.5, 2.6])



def regLine(arr_y, next_val = "", arr_x = ""):
    if arr_x == "":
        arr_x = np.arange(1, len(arr_y) + 1)
    if next_val == "":
        arr_x_n = np.arange(1, len(arr_y) + 2)
    else:
        arr_x_n = np.arange(1, next_val + 1)
        
    n = np.size(arr_x)

    x_mean = np.mean(arr_x)
    y_mean = np.mean(arr_y)

    slope_xy = np.sum(arr_x * arr_y) - n * x_mean * y_mean 
    slope_xx = np.sum(arr_x * arr_x) - n * x_mean * x_mean

    # slope_xy = np.sum((arr_x - x_mean) * (arr_y - y_mean))
    # slope_xx = np.sum((arr_x - x_mean) ** 2)

    slope = slope_xy / slope_xx
    intercept = y_mean - slope * x_mean

    regression_line = slope * arr_x_n + intercept

    return regression_line, arr_x_n

regression_line, arr_x_n = regLine(arr_y)

