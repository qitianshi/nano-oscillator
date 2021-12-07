# plot_magnetization.py
# Plots magnetization vector directions (x, y, z) generated from mumax3.

# import functions
import pandas as pd
import matplotlib.pyplot as plt
import os

# import functions from parse_output.py
from parse_output import get_folder_dir
from parse_output import get_angle
from parse_output import get_freq


def plot_angle(x, y):
    start_angle = 0
    end_angle = 0
    angle_step = 30

    for i in range(start_angle, end_angle + angle_step, angle_step):
        folder_dir = get_folder_dir()
        filepath = get_angle(i)
        graph_path = os.path.join(folder_dir, 'plots/split_plots/by_angle/', str(i) + '.png')

        data = pd.read_csv(filepath, sep=",")

        plt.subplot(1, 1, 1)
        graph = plt.plot(data['# ' + x], data[y]) #the header for time has a weird # in front of it
        plt.setp(graph, linewidth=0.5)

        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(str(y) + ' against ' + str(x) + ' for ' + str(i) + ' degrees' )

        plt.savefig(graph_path)
        plt.show()

plot_angle("t (s)", "my ()")

