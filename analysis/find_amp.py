"""Find amplitude from dataset"""

import readresults
import plot
import pandas as pd
from os.path import join
import numpy as np

def amp(
        date : str = None,
        phi : str = None,
        f_RF : float = None,
        var : str = None
):
    """Finds the amplitudes for one variable

    Args:
        phi (str): the phi value ("Xdeg")
    """

    timeskip = 1.5e-9

    waveform = readresults.read_data(readresults.data_path(date,
        {"phi": "00" + phi,
        "f_RF": f"{f_RF / 10**9}GHz"}
    ))

    amp = (waveform.loc[waveform["t"] > timeskip, var].max() -
        waveform.loc[waveform["t"] > timeskip, var].min())/2
    #super rudimentary way of determining amplitude

    return amp

def amp_phi(
    date : str = None,
    phi : str = None,
    var : str = None
):
    """Finds the ampltiude for all the datasets in a given phi value, for one given var"""

    data = readresults.read_data(readresults.data_path(date))
    amplitude = np.empty((0, 2), float) #creates an empty numpy array

    for f_RF in data["f_RF"].unique():
        row = np.array([f_RF, amp(date, phi, f_RF, var)])
        amplitude = np.append(amplitude, [row], axis=0)
    #appends the amplitude and frequency values into the numpy 2D array

    df = pd.DataFrame(amplitude, columns=["f_RF", "amplitude"])
    df.to_csv(join(
        readresults.result_dir(date), 'amplitudes', f"{phi}.tsv"), sep='\t', index=False
    )
    #converts the 2D array into a dataframe and csv file



