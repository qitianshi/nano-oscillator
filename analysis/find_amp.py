"""Find amplitude from dataset"""

from os.path import join
import pandas as pd
import numpy as np
import readresults


def find_amp(
        date : str = None,
        phi : str = None,
        fRF : float = None,
        var : str = None
):
    """Finds the amplitudes for one variable"""

    timeskip = 1.5e-9

    waveform = readresults.read_data(readresults.data_path(date,
        {"phi": f"{phi:03}deg",
        "f_RF": f"{fRF / 10**9}GHz"}
    ))

    # Super rudimentary way of determining amplitude
    amplitude = (waveform.loc[waveform["t"] > timeskip, var].max() -
        waveform.loc[waveform["t"] > timeskip, var].min())/2

    return amplitude


def amp_phi_fRF(date : str = None, var : str = None):
    """Finds the ampltiude for all the split datasets, for one given var"""

    data = readresults.read_data(readresults.data_path(date))

    for phi in data["phi"].unique():

        # Creates an empty numpy array
        amplitude = np.empty((0, 2), float)

        # Appends the amplitude and frequency values into the numpy 2D array
        for fRF in data["f_RF"].unique():
            row = np.array([fRF, find_amp(date, phi, fRF, var)])
            amplitude = np.append(amplitude, [row], axis=0)

        # Converts the 2D array into a dataframe and csv file
        output = pd.DataFrame(amplitude, columns=["f_RF", "amplitude"])
        output.to_csv(join(
            readresults.result_dir(date), 'amplitudes', f"{phi}deg.tsv"), sep='\t', index=False
        )
