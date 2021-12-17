"""Find amplitude from dataset"""

from os.path import join

import pandas as pd
import numpy as np

import readresults


def calc_amp(date: str, phi: str, fRF: float, var: str) -> float:
    """
    Finds the amplitudes for one variable.

    Args:
        var (str): The magnetization vector variable to calculate. Acceptable
          values: "mx", "my", "mz".
    """

    skip_duration = 1.5e-9

    data = readresults.read_data(readresults.data_path(date,
        {"phi": f"{phi:03}deg",
        "f_RF": f"{fRF / 1e9}GHz"}
    ))

    operable_data = data.loc[data["t"] > skip_duration][var]                 #pylint: disable=E1136

    #TODO: Find a better way of calculating amplitude of the graphs
    amplitude = (operable_data.max() - operable_data.min()) / 2

    return amplitude


def amp_phi_fRF(var: str, date: str = None):
    """Finds the amplitude for all the split datasets, for one given var."""

    data = readresults.read_data(readresults.data_path(date))

    amplitudes = np.empty((data["f_RF"].nunique(), 0), float)
    freq_col = np.empty((0, 1), float)

    for fRF in data["f_RF"].unique():
        row = np.array([fRF])
        freq_col = np.append(freq_col, [row], axis=0)

    amplitudes = np.column_stack((amplitudes, freq_col))

    for phi in data["phi"].unique():

        col = np.empty((0, 1), float)

        for fRF in data["f_RF"].unique():
            row = np.array([calc_amp(date, phi, fRF, var)])
            col = np.append(col, [row], axis=0)

        amplitudes = np.column_stack((amplitudes, col))

    amplitude_data = pd.DataFrame(
        amplitudes, columns=["f_RF", *[f"{i}deg" for i in data["phi"].unique()]])
    amplitude_data.to_csv(join(
        readresults.result_dir(date), 'calculated_values', 'amplitudes.tsv'), sep='\t', index=False
    )
