"""Find amplitude from dataset"""

from os.path import join

import pandas as pd
import numpy as np

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
        names.append("amp for " f"{phi}deg")

    return names

def amp_phi_fRF(date: str = None, var: str = None):
    """Finds the ampltiude for all the split datasets, for one given var."""

    data = readresults.read_data(readresults.data_path(date))

    amplitudes = np.empty((data["f_RF"].nunique(), 0), float)
    freq_col = np.empty((0, 1), float)

    for f_RF in data["f_RF"].unique():
        row = np.array([f_RF])
        freq_col = np.append(freq_col, [row], axis=0)

    amplitudes = np.column_stack((amplitudes, freq_col))

    for phi in data["phi"].unique():

        col = np.empty((0, 1), float)

        for f_RF in data["f_RF"].unique():
            row = np.array([calc_amp(date, phi, f_RF, var)])
            col = np.append(col, [row], axis=0)

        amplitudes = np.column_stack((amplitudes, col))

    df = pd.DataFrame(amplitudes, columns=col_names(date))
    df.to_csv(join(
            readresults.result_dir(date), 'amplitudes', 'amplitudes.tsv'), sep='\t', index=False
    )
