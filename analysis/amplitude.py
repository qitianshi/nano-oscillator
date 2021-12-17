"""Find amplitude from dataset"""

from os.path import join

import pandas as pd
import numpy as np
from readresults import amplitude_dir, read_data

import readresults


def calc_amp(
        date: str = None,
        phi: str = None,
        fRF: float = None,
        var: str = None
) -> float:
    """Finds the amplitudes for one variable"""

    timeskip = 1.5e-9

    waveform = readresults.read_data(readresults.data_path(date,
        {"phi": f"{phi:03}deg",
        "f_RF": f"{fRF / 1e9}GHz"}
    ))

    #TODO: Find a better way of calculating amplitude of the graphs
    amplitude = (waveform.loc[waveform["t"] > timeskip, var].max() -         #pylint: disable=E1136
        waveform.loc[waveform["t"] > timeskip, var].min()) / 2         #pylint: disable=E1101,E1136

    return amplitude

def col_names(date: str = None, skip: bool = False) -> list[str]:
    """Returns an array of column names.

    Args:
        skip (bool): if True, it skips the first column name (the frequency column) and
            just returns the array of the amplitude columns
    """

    data = readresults.read_data(readresults.data_path(date))
    if skip:
        names = []
    else:
        names = ["frequency"]

    for phi in data["phi"].unique():
        names.append(f"{phi}deg")

    return names

def amp_phi_fRF(date: str = None, var: str = None):
    """Finds the ampltiude for all the split datasets, for one given var."""

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
            row = np.array([calc_amp(date, phi, fRF, var)])
            col = np.append(col, [row], axis=0)

        amplitudes = np.column_stack((amplitudes, col))

    #converts the numpy array into a dataframe
    amplitude_data = pd.DataFrame(amplitudes, columns=col_names(date))
    amplitude_data.to_csv(join(
        readresults.result_dir(date), 'calculated_values', 'amplitudes.tsv'), sep='\t', index=False
    )

def max_amp_phi(date: str = None):
    """Finds the maximum amplitudes for each phi value"""

    data = read_data(join(amplitude_dir(date), "amplitudes.tsv"))
    freq = np.empty((0, 1), float)
    max = np.empty((0, 1), float)

    #create numpy arrays with max amp and phi values
    for val in (data.columns):
        if "deg" in val:
            phi = np.array([val.strip("deg")])
            freq = np.append(freq, [phi], axis=0)

            max_amp = np.array([data[val].max()])
            max = np.append(max, [max_amp], axis=0)

    output = np.column_stack((freq, max))

    #output to panda dataframe and a tsv file
    output_data = pd.DataFrame(output, columns=["phi", "max amplitudes"])
    output_data.to_csv(join(
        readresults.result_dir(date), 'calculated_values', 'max_amplitudes.tsv'),
        sep='\t', index=False
    )
