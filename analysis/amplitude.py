"""Find amplitude from dataset"""

from os.path import join

import pandas as pd
import numpy as np

from analysis import read, paths


def __calc_amp(date: str, phi: str, fRF: float, mag_var: str) -> float:
    """
    Finds the amplitudes for one variable.

    Args:
        mag_var (str): The magnetization vector variable to calculate.
          Acceptable values: "mx", "my", "mz".
    """

    skip_duration = 1.5e-9

    data = read.read_data(paths.data_path(date,
        {"phi": f"{phi:03}deg",
        "f_RF": f"{fRF / 1e9}GHz"}
    ))

    operable_data = data.loc[data["t"] > skip_duration][mag_var]             #pylint: disable=E1136

    #TODO: Find a better way of calculating amplitude of the graphs
    amplitude = (operable_data.max() - operable_data.min()) / 2

    return amplitude


def amp_phi_fRF(date: str = None):
    """Finds the amplitude for all the split datasets, for all magnetization
    components.
    """

    date = date if date is not None else paths.latest_date()
    data = read.read_data(paths.data_path(date))

    for mag_var in ["mx", "my", "mz"]:

        amplitudes = np.empty((data["f_RF"].nunique(), 0), float)
        freq_col = np.empty((0, 1), float)

        #creates a numpy array of all the frequency values
        for fRF in data["f_RF"].unique():
            row = np.array([fRF])
            freq_col = np.append(freq_col, [row], axis=0)

        amplitudes = np.column_stack((amplitudes, freq_col))

        # Creates a numpy array of all the amplitude data for each phi value.
        for phi in data["phi"].unique():

            col = np.empty((0, 1), float)

            for fRF in data["f_RF"].unique():
                row = np.array([__calc_amp(date, phi, fRF, mag_var)])
                col = np.append(col, [row], axis=0)

            amplitudes = np.column_stack((amplitudes, col))

        read.prep_dir(join(paths.result_dir(date), "calculated_values"), clear=False)

        # Outputs amplitude data.
        pd.DataFrame(amplitudes, columns=["f_RF", *[f"{i}deg" for i in data["phi"].unique()]]) \
            .to_csv(paths.amp_path(mag_var, date), sep='\t', index=False)


def max_amp_phi(date: str = None):
    """Finds the maximum amplitudes for each phi value"""

    mag_vars = ["mx", "my", "mz"]
    date = date if date is not None else paths.latest_date()
    data = read.read_data(paths.data_path(date))

    phi_col = np.empty((0, 1), int)
    for phi in data["phi"].unique():
        phi = np.array([phi])
        phi_col = np.append(phi_col, [phi], axis=0)

    for var in mag_vars:

        data = read.read_data(paths.amp_path(var, date))
        max_col = np.empty((0, 1), float)

        # Creates numpy arrays with MaxAmp and phi values.
        for val in (data.columns):
            if "deg" in val:
                max_amp = np.array([data[val].max()])
                max_col = np.append(max_col, [max_amp], axis=0)

        phi_col = np.column_stack((phi_col, max_col))

    # Outputs to data file.
    pd.DataFrame(phi_col, columns=(["phi"] + (f"MaxAmp_{i}" for i in mag_vars))) \
        .to_csv(
            join(paths.result_dir(date), 'calculated_values', 'MaxAmp.tsv'),
            sep='\t',
            index=False
        )
