"""testbed"""

import json
import paths

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from analysis import *

xticks_num = 10

xindex = 250
yindex = None
component = "mz"
filename = "geom000000"
cell_index = "x"

#creates a Pandas dataframe with the B_ext data as a column
if yindex is None:
    #vertical line
    plot_data = pd.DataFrame(
        read.read_data(paths.spatial_path(0, filename, component)).iloc[:, xindex]
    )

elif xindex is None:
    #horizontal line
    plot_data = pd.DataFrame(
        read.read_data(paths.spatial_path(0, filename, component)).iloc[yindex, :]
    )

else:
    raise NotImplementedError("Data needs to be either a row or a column")

#create the list of x coordinates and puts it in the Pandas dataframe
with open(paths.header_path(), 'r', encoding='utf-8') as file:
        headers = json.load(file)
        xvar = np.arange(
            float(headers[f"{cell_index}min"]),
            float(headers[f"{cell_index}max"]),
            float(headers[f"{cell_index}stepsize"])
        )

        xlabel = f"{cell_index} (" + headers["meshunit"] + ")"
        plot_data.insert(0, xlabel, xvar)
