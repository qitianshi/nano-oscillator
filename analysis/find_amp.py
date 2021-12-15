"""Find amplitude from dataset"""

import pandas as pd
import numpy as np
import readresults
import matplotlib.pyplot as plt
import plot
from os.path import join

def amp(
        date : str = None,
        phi : str = None,
        f_RF : float = None,
        var : str = None
):
    """Finds the amplitudes for one variable"""

    timeskip = 1.5e-9

    waveform = readresults.read_data(readresults.data_path(date,
        {"phi": f"{phi:03}deg",
        "f_RF": f"{f_RF / 10**9}GHz"}
    ))

    amp = (waveform.loc[waveform["t"] > timeskip, var].max() -
        waveform.loc[waveform["t"] > timeskip, var].min())/2
    #super rudimentary way of determining amplitude

    return amp

def amp_phi_fRF(date : str = None, var : str = None):
    """Finds the ampltiude for all the split datasets, for one given var"""

    data = readresults.read_data(readresults.data_path(date))

    for phi in data["phi"].unique():

        amplitude = np.empty((0, 2), float) #creates an empty numpy array

        for f_RF in data["f_RF"].unique():
            row = np.array([f_RF, amp(date, phi, f_RF, var)])
            amplitude = np.append(amplitude, [row], axis=0)
        #appends the amplitude and frequency values into the numpy 2D array

        df = pd.DataFrame(amplitude, columns=["f_RF", "amplitude"])
        df.to_csv(join(
            readresults.result_dir(date), 'amplitudes', f"{phi}deg.tsv"), sep='\t', index=False
        )
        #converts the 2D array into a dataframe and csv file



