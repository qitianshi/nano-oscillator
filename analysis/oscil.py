"""Analyzes oscillation characteristics."""

import os

import numpy as np

from analysis import paths, write


def load_npy(date: str = None):
    """Returns npy files as dict of numpy arrays with filename as key."""

    date = date if date is not None else paths.top.latest_date()

    fields = {}

    for file in os.listdir(paths.data.raw(date)):

        if os.path.splitext(file)[1].strip('.') == "npy":

            #TODO: raise FileNotFoundError

            filename = os.path.splitext(file)[0]
            write.prep_dir(paths.spatial.geom_dir(filename, date))

            fields[filename] = np.load(os.path.join(paths.data.raw(date), file))

    return fields
