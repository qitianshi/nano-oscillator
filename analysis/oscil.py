"""Analyzes oscillation characteristics."""

import os

import numpy as np

import analysis as anl

def load_npy(date: str = None):
    """Returns npy files as dict of numpy arrays with filename as key."""

    date = date if date is not None else anl.paths.top.latest_date()

    fields = {}

    for file in os.listdir(anl.paths.data.raw(date)):

        if file.endswith("700.npy"):

            #TODO: raise FileNotFoundError

            filename = os.path.splitext(file)[0]
            anl.write.prep_dir(anl.paths.spatial.geom_dir(filename, date))

            fields[filename] = np.load(os.path.join(anl.paths.data.raw(date), file))

    return fields
