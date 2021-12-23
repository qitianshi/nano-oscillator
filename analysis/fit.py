"""Curve-fits amplitude data."""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from analysis import paths, read


def __cauchy_distribution(x, x0, gamma, I):                           #pylint: disable=invalid-name
    """Cauchy distribution curve-fitting function.

    Args:
        x: Independent variable.
        x_0: Fitting parameter: the x-value of the peak.
        gamma: Fitting parameter: half-width at half-maximum.
        I: Fitting parameter: the height of the peak.
    """

    return I * ( np.square(gamma) / ( np.square(x - x0) + np.square(gamma) ) )


def fit_cauchy(
    mag_var: str,
    xlim: tuple[float],
    p0: tuple[float] = None,                                          #pylint: disable=invalid-name
    date: str = None
):
    """Curve-fits magnetization amplitudes to a Cauchy distribution.

    Args:
        mag_var (str): The magnetization vector variable to calculate.
          Acceptable values: "mx", "my", "mz".
        xlim (tuple[float]): A tuple of two values. The zeroth value is the
          lower limit and the first value is the upper limit.
        p0 (tuple[float]): Initial guesses of fitting parameters for the Cauchy
          distribution: (x_0, gamma, I).
    """

    p0 = p0 if p0 is not None else [4.5e9, 0.5e9, 0.004]
    date = date if date is not None else paths.latest_date()

    amp_data = read.read_data(paths.amp_path(mag_var, date))
    extracted_data = amp_data.loc[
        (amp_data["f_RF"] <= xlim[1]) & (amp_data["f_RF"] >= xlim[0])]       #pylint: disable=E1136
    amp_cols = list(amp_data.columns)                                    #pylint: disable=no-member
    amp_cols.remove("f_RF")

    results = np.empty(shape=(0, 4))

    for phi in amp_cols:
        results = np.append(
            arr=results,
            values=np.reshape(
                [
                    phi,
                    *curve_fit(
                        f=__cauchy_distribution,
                        xdata=extracted_data["f_RF"],
                        ydata=extracted_data[phi],
                        p0=p0
                    )[0]
                ],
                newshape=(-1, 4)
            ),
            axis=0
        )

    pd.DataFrame(results, columns=["f_RF", "x_0", "gamma", "I"]) \
        .to_csv(
            paths.fitted_amp_path(mag_var, date),
            sep='\t',
            index=False
        )
