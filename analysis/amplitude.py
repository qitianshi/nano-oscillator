"""Find amplitude from dataset"""

import numpy as np
import pandas as pd

from analysis import paths, read, write


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

    for mag_var in ("mx", "my", "mz"):

        amplitudes = np.reshape(np.array(data["f_RF"].unique()), newshape=(-1, 1))

        # Appends the amplitude data for each phi value.
        for phi in data["phi"].unique():
            col = np.array([__calc_amp(date, phi, fRF, mag_var) for fRF in data["f_RF"].unique()])
            amplitudes = np.append(amplitudes, np.reshape(col, newshape=(-1, 1)), axis=1)

        write.prep_dir(paths.calcvals_dir(date), clear=False)

        # Outputs amplitude data.
        pd.DataFrame(amplitudes, columns=["f_RF", *[f"{i}deg" for i in data["phi"].unique()]]) \
            .to_csv(paths.amp_path(mag_var, date), sep='\t', index=False)


def max_amp_phi(date: str = None):
    """Finds the maximum amplitudes for each phi value."""

    date = date if date is not None else paths.latest_date()

    # .T transposes the ndarray to a column vector.
    result = np.reshape(
        np.array( ( read.read_data(paths.data_path(date))["phi"] ).unique() ),
        newshape=(-1, 1)
    )

    mag_vars = ("mx", "my", "mz")
    for var in mag_vars:

        # Reads the greatest amp for each value of phi.
        data = read.read_data(paths.amp_path(var, date))
        max_col = np.array([data[val].max() for val in data.columns[1:]])

        result = np.append(result, np.reshape(max_col, newshape=(-1, 1)), axis=1)

    # Outputs to data file.
    pd.DataFrame(result, columns=(["phi"] + list(f"MaxAmp_{i}" for i in mag_vars))) \
        .to_csv(paths.maxamp_path(date), sep='\t', index=False)
