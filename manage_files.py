# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 09:56:37 2024

@author: Nicolas
"""
import nextwheel
import os

# %%


def rename_file(dat_filename: str, new_name: str, path: str, new_path: str):
    """
    Rename and relocate the dat file.

    Parameters
    ----------
    dat_filename : str
        DESCRIPTION.
    new_name : str
        DESCRIPTION.
    path : str
        DESCRIPTION.
    new_path : str
        DESCRIPTION.

    Returns
    -------
    None.

    """
    n_trial = 0
    while os.path.isfile(f"{new_path}{new_name}{n_trial}"):  # not overwriting
        n_trial += 1
    os.rename(path + dat_filename, f"{new_path}{new_name}{n_trial}")


def relocate_file(dat_filename: str, path: str, new_path: str):
    """
    Relocate the dat file.

    Parameters
    ----------
    dat_filename : str
        DESCRIPTION.
    path : str
        DESCRIPTION.
    new_path : str
        DESCRIPTION.

    Returns
    -------
    None.

    """
    os.rename(f"{path}{dat_filename}", f"{new_path}{dat_filename}")


# %%

path = "C:/Users/Nicolas/"
new_path = "C:/Users/Nicolas/Desktop/Test/"

if __name__ == "__main__":
    # nw = nextwheel.NextWheel("192.168.0.86")
    # nw = nextwheel.NextWheel("192.168.0.130")
    nw = nextwheel.NextWheel("192.168.1.167")

    for files in nw.file_list()["files"]:
        dat_filename = files["name"]
        nw.file_download(dat_filename)
        new_name = dat_filename
        try:
            relocate_file(dat_filename, path, new_path)
        except:
            rename_file(dat_filename, new_name, path, new_path)

    for files in nw.file_list()["files"]:
        dat_filename = files["name"]
        nw.file_delete(dat_filename)
