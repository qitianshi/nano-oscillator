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


def amp_phi_fRF(date: str = None, var: str = None):
    """Finds the ampltiude for all the split datasets, for one given var."""

    data = readresults.read_data(readresults.data_path(date))

    freq_col = np.empty((0, 1), float)

    for fRF in data["f_RF"].unique():
        col = np.array([fRF])
        freq_col = np.append(freq_col, [col], axis=0)

    for phi in data["phi"].unique():
        for fRF in data["f_RF"].unique():
            amp_col = np.empty((0, 1), float)
            col = np.array([calc_amp(date, phi, fRF, var)])
            amp_col = np.append(amp_col, [col], axis=0)


    # for phi in data["phi"].unique():

    #     # Creates an empty numpy array
    #     amplitude = np.empty((0, 2), float)

    #     # Appends the amplitude and frequency values into the numpy 2D array
    #     for fRF in data["f_RF"].unique():
    #         row = np.array([fRF, calc_amp(date, phi, fRF, var)])
    #         amplitude = np.append(amplitude, [row], axis=0)

    #     # Converts the 2D array into a dataframe and csv file
    #     output = pd.DataFrame(amplitude, columns=["f_RF", "amplitude"])
    #     output.to_csv(join(
    #         readresults.result_dir(date), 'amplitudes', "all amplitudes.tsv"), sep='\t', index=False
    #     )

amp_phi_fRF("2021-12-06_0610", "my")
