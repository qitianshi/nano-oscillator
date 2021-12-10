"""Parses output data from mumax3 in the results directory."""

from os.path import join
import pandas as pd

import readresults


def __split_variable(
    dataset: pd.DataFrame,
    var: str,
    reset_t: bool = True
) -> dict[float, pd.DataFrame]:
    """"Splits a dataframe by a variable."""

    #FIXME: This code will group all rows with the same value of var together;
    #       expected behavior is that different groups should be separated.

    unique_values = dataset[var].unique()
    extracted_datasets = {}

    for phi in unique_values:

        extract = dataset[dataset[var] == phi].reset_index(drop=True)

        if reset_t:
            initial_t = extract.at[0, "t"]
            extract["t"] -= initial_t

        extracted_datasets[phi] = extract

    return extracted_datasets


def split_phi(date: str = None, reset_t: bool = True):
    """"Splits data by phi."""

    split_datasets = __split_variable(
        readresults.read_table(readresults.find_data(date)), "phi", reset_t)
    destination = join(readresults.find_result(date), "split", "phi")

    readresults.prep_dir(destination)

    for phi, data in split_datasets.items():
        data.to_csv(join(destination, f"{phi:03}deg.tsv"), sep='\t', index=False)


def split_phi_fRF(date: str = None, reset_t: bool = True):
    """Splits data by phi, then f_RF."""

    split_datasets_phi = __split_variable(
        readresults.read_table(readresults.find_data(date)), "phi", reset_t)
    base_destination = join(readresults.find_result(date), "split", "phi, f_RF")

    readresults.prep_dir(base_destination)

    for phi, data in split_datasets_phi.items():

        split_datasets_phi_fRF = __split_variable(data, "f_RF", reset_t)
        destination = join(base_destination, f"{phi:03}" + "deg")

        readresults.prep_dir(destination)

        for fRF, split_data in split_datasets_phi_fRF.items():
            split_data.to_csv(
                join(destination, f"{phi:03}deg, {fRF / 10**9}GHz.tsv"),
                sep='\t', index=False)