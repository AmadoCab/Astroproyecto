#!/usr/bin/env python3

import argparse
import numpy as np
import pandas as pd

column_types = {
    "Date(UTC)":'str',
    "Julian Date":'str',
    "MET":'float64',
    "TS":'float64',
    "Photon Flux [0.1-100 GeV](photons cm-2 s-1)":'str',
    "Photon Flux Error(photons cm-2 s-1)":'str',
    "Photon Index":'str',
    "Photon Index Error":'str',
    "Sun Distance":'str',
    "Fit Tolerance":'str',
    "MINUIT Return Code":'str',
    "Analysis Log":'str'
}

def parse_arguments():
    """
    Parse command-line arguments to get the CSV file path.

    Returns:
        argparse.Namespace: Contains the path to the CSV file specified by the user.
    """
    parser = argparse.ArgumentParser(description="Variability.")
    parser.add_argument('csv_path', type=str, help="Path to the CSV file.")
    return parser.parse_args()

def data_cleaning(file_path):
    """
    Cleans the data by removing unnecessary columns from the DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: A DataFrame with specific columns removed, containing only relevant data.
    """
    df = pd.read_csv(file_path, dtype=column_types)
    df = df.drop(columns=[
        "Date(UTC)", "Julian Date", "Analysis Log",
        "Sun Distance", "Fit Tolerance","MINUIT Return Code"
    ])
    return df


def variabilities(df):
    """
    Calculates the fractional variability and the variability index based on the data.

    Args:
        df (pandas.DataFrame): A DataFrame with cleaned data, containing flux and error values.

    Returns:
        tuple: A tuple containing:
            - mod_idx (float): The modulation index.
            - frac_var (float): The fractional variability.
            - Dfrac_var (float): The error in fractional variability.
            - var_idx (float): The variability index.
    """
    # Get flux and error columns
    values = df.iloc[:, [2, 3]].values

    # Separate values into real and upper limit values
    vls_v, err_v = [], []
    vls_c = []
    for flx, err in values:
        if flx.startswith("<"):
            # Manejar los límites superiores
            vls_c.append(float(flx[2:]))
        else:
            vls_v.append(float(flx))
            err_v.append(float(err))

    ## Convert lists to NumPy arrays for efficient calculations
    vls_v = np.array(vls_v)
    err_v = np.array(err_v)

    ## Modulation index
    mean_v = np.mean(vls_v)
    std_v = np.std(vls_v)
    mod_idx = std_v/mean_v

    ## Fraccional variability
    var_v = np.var(vls_v, ddof=1)
    sigma = np.mean(err_v ** 2)
    frac_var = np.sqrt((var_v - sigma) / mean_v ** 2)

    ## Fractional variability error
    N = vls_v.size
    auxvar = np.sqrt(2/N * (sigma/mean_v**2)**2 + sigma/N * (2*frac_var/mean_v)**2)
    Dfrac_var = np.sqrt(frac_var**2 + auxvar) - frac_var

    ## Variability index
    var_idx = (np.max(vls_v)-np.min(vls_v) - (np.max(err_v)+np.min(err_v))) /\
              (np.max(vls_v)+np.min(vls_v) - (np.max(err_v)-np.min(err_v)))

    return mod_idx, frac_var, Dfrac_var#, var_idx


def main():
    """
    Main function to parse arguments, clean data, calculate indices, and print the results.
    """
    args = parse_arguments()
    data = data_cleaning(args.csv_path)
    vars = variabilities(data)
    print(*vars, sep=',')


if __name__ == '__main__':
    main()
