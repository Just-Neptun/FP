import ast
import numpy as np
import pandas as pd

def read_metadata(loc):
    '''Safely reads first line of file as a python dict containing metadata for the data in the .txt'''
    with open(loc, "r") as file:
        return ast.literal_eval(file.readline())


def read_exp_file(loc, skip_data_rows=0):
    '''Reads a .txt file at given location. Returns tuple of (tuple of columns) and the metadata dict.'''
    freq, A, A_err, phi, phi_err = np.loadtxt(
        loc,
        delimiter=",",
        skiprows=2+skip_data_rows,
        unpack=True
    )
    metadata = read_metadata(loc)
    return (freq, A, A_err, phi, phi_err), metadata

def pd_read_exp_file(loc, skip_data_rows=0):
    '''Reads a .txt file at given location. Returns tuple of pd.DataFrame and the metadata dict.'''
    df = pd.read_csv(
        loc,
        skiprows=1
    )
    df = df[skip_data_rows:]
    metadata = read_metadata(loc)
    return df, metadata