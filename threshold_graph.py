import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
from threshold_calculate import go
from threshold_return_path import path as path1

path = path1


def make_file(elements, factor1):
    with open(path+'graph.txt', 'w') as file:
        file.truncate(0)
        file.write("Nth Gene Included"+'\n')

    go(elements, "all", factor1)

def make_graph(elements, type):
    with open(path+'graph.txt', 'r') as file:
        lines = file.readlines()

    x_array = []
    y_array = []
    for line in lines:
        rows = line.strip().split('\t')
        if rows[0] != "Nth Gene Included":
            x_array.append(float(rows[0]))
            if type == "incremental_saturation" and rows[1] != "Incremental Saturation":
                y_array.append(float(rows[1]))
            elif type == "overall_saturation" and rows[2] != "Overall Saturation":
                y_array.append(float(rows[2]))

    x = np.array(x_array)
    y = np.array(y_array)

    fig, ax = plt.subplots()
    ax.plot(x, y, c='#325BA9', linewidth="1")

    ax.yaxis.set_major_locator(MultipleLocator(0.1))
    x_ticks = np.arange(0, elements + round((elements / 10)), round((elements / 10)))
    ax.set_xticks(x_ticks)
    y_ticks = np.arange(0, max(y) + 0.1, 0.1)
    ax.set_yticks(y_ticks)

    plt.show()

