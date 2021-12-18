"""Find amplitude from dataset"""

from os.path import join

import pandas as pd
import numpy as np

import readresults


def calc_amp(date: str, phi: str, fRF: float, mag_var: str) -> float:
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

    operable_data = data.loc[data["t"] > skip_duration][mag_var]             #pylint: disable=E1136

    #TODO: Find a better way of calculating amplitude of the graphs
    amplitude = (operable_data.max() - operable_data.min()) / 2

    return amplitude


def amp_phi_fRF(mag_var: str, date: str = None):
    """Finds the amplitude for all the split datasets, for one given var."""

    date = date if date is not None else readresults.latest_date()
    data = readresults.read_data(readresults.data_path(date))

    amplitudes = np.empty((data["f_RF"].nunique(), 0), float)
    freq_col = np.empty((0, 1), float)

    #creates a numpy array of all the frequency values
    for fRF in data["f_RF"].unique():
        row = np.array([fRF])
        freq_col = np.append(freq_col, [row], axis=0)

    amplitudes = np.column_stack((amplitudes, freq_col))

    #creates a numpy array of all the amplitude data for each phi value
    for phi in data["phi"].unique():

        col = np.empty((0, 1), float)

        for fRF in data["f_RF"].unique():
            row = np.array([calc_amp(date, phi, fRF, mag_var)])
            col = np.append(col, [row], axis=0)

        amplitudes = np.column_stack((amplitudes, col))

    #converts the numpy array into a dataframe
    amplitude_data = pd.DataFrame(
        amplitudes, columns=["f_RF", *[f"{i}deg" for i in data["phi"].unique()]])
    amplitude_data.to_csv(readresults.amplitude_path(mag_var, date), sep='\t', index=False)

def max_amp_phi(date: str = None, mag_vars: list[str] = ["mx", "my", "mz"]):
    """Finds the maximum amplitudes for each phi value"""

    date = date if date is not None else readresults.latest_date()
    data = readresults.read_data(readresults.data_path(date))

    phi_col = np.empty((0, 1), int)
    for phi in data["phi"].unique():
        phi = np.array([phi])
        phi_col = np.append(phi_col, [phi], axis=0)

    for var in mag_vars:
        data = readresults.read_data(readresults.amplitude_path(var, date))
        max_col = np.empty((0, 1), float)

        #create numpy arrays with max amp and phi values
        for val in (data.columns):
            if "deg" in val:
                max_amp = np.array([data[val].max()])
                max_col = np.append(max_col, [max_amp], axis=0)

        phi_col = np.column_stack((phi_col, max_col))

    #output to panda dataframe and a tsv file
    output_data = pd.DataFrame(phi_col, columns=["phi"] + mag_vars)
    output_data.to_csv(join(
        readresults.result_dir(date), 'calculated_values', 'max_amp.tsv'),
        sep='\t', index=False
    )

max_amp_phi("2021-12-06_0610")