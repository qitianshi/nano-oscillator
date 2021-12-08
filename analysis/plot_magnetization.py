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


def plot_angle():
    start_angle = 0
    end_angle = 360
    angle_step = 5

    for i in range(start_angle, end_angle + angle_step, angle_step):
        folder_dir = get_folder_dir()
        filepath = get_angle(i)
        filename = 'mx, my and mz against time for ' + str(i) + '°'
        graph_path = os.path.join(folder_dir, 'plots/split_plots/by_angle/', filename + '.png')

        data = pd.read_csv(filepath, sep=",")

        plt.figure()
        graph = plt.plot(data['# t (s)'], data["mx ()"]) #the header for time has a weird # in front of it
        graph = plt.plot(data['# t (s)'], data["my ()"])
        graph = plt.plot(data['# t (s)'], data["mz ()"])
        plt.setp(graph, linewidth=0.5)

        plt.xlabel("t (s)")
        plt.ylabel("mx, my and mz")
        plt.title(filename)

        plt.savefig(graph_path)
        # plt.show()

plot_angle()

