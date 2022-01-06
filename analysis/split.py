"""Splits data by variables."""

import pandas as pd

from analysis import paths, read, write


def __split_variable(
    data: pd.DataFrame,
    var: str,
    reset_t: bool = True
) -> dict[float, pd.DataFrame]:
    """"Splits data by a variable."""

    #FIXME: This code will group all rows with the same value of var together;
    #       expected behavior is that different groups should be separated.

    unique_values = data[var].unique()
    extracted_data = {}

    for phi in unique_values:

        extract = data[data[var] == phi].reset_index(drop=True)

        if reset_t:
            initial_t = extract.at[0, "t"]
            extract["t"] -= initial_t

        extracted_data[phi] = extract

    return extracted_data


def split_phi(date: str = None, reset_t: bool = True):
    """"Splits data by phi."""

    split_data = __split_variable(read.read_data(paths.data.data_path(date)), "phi", reset_t)
    destination = paths.data.dataset_dir(date, vals={"phi": None})

    write.prep_dir(destination)

    for phi, data in split_data.items():
        data.to_csv(
            paths.data.data_path(date, {"phi": f"{phi:03}deg"}),
            sep='\t',
            index=False
        )


def split_phi_fRF(date: str = None, reset_t: bool = True):
    """Splits data by phi, then f_RF."""

    split_data_phi = __split_variable(
        read.read_data(paths.data.data_path(date)), "phi", reset_t)

    write.prep_dir(paths.data.dataset_dir(date, vals={"phi": None, "f_RF": None}))

    for phi, data in split_data_phi.items():

        split_data_phi_fRF = __split_variable(data, "f_RF", reset_t)

        write.prep_dir(paths.data.dataset_dir(date, vals={"phi": f"{phi:03}deg", "f_RF": None}))

        for fRF, split_data in split_data_phi_fRF.items():
            split_data.to_csv(
                paths.data.data_path(
                    date,
                    vals={"phi": f"{phi:03}deg", "f_RF": f"{fRF / 10**9}GHz"}
                ),
                sep='\t',
                index=False
            )
