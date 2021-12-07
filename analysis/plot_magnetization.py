# plot_magnetization.py
# Plots magnetization vector directions (x, y, z) generated from mumax3.

# import functions
import pandas as pd
import matplotlib.pyplot as plt

# import functions from parse_output.py
from parse_output import get_result

# get file directory
filepath = get_result()

# read data
data = pd.read_csv(filepath, sep="\t")

# the number of graphs to display in rows and columns
displayRow = 2
displayCol = 1

# plotting the graphs
plt.subplot(displayRow, displayCol, 1)
plt.plot(data["t (s)"], data["mx ()"], "ro")

plt.subplot(displayRow, displayCol, 2)
plt.plot(data["t (s)"], data["my ()"], "go")


plt.show()

