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

path = r"C:\Users\MOSA\Documents\NextWheel\python/"
new_path = r"C:\Users\MOSA\Desktop\Pilot test2\Biofeedback\Right/"

if __name__ == "__main__":
    nw = nextwheel.NextWheel("192.168.0.86")
    # nw = nextwheel.NextWheel("192.168.0.130")

    nw.file_download("calibration.json")

    if not os.path.exists(new_path):
        os.makedirs(new_path)

        try:
            relocate_file("calibration.json", path, new_path)
        except:
            print("Calibration file already in folder")

    for files in nw.file_list()["files"]:
        dat_filename = files["name"]
        nw.file_download(dat_filename)
        new_name = dat_filename
        try:
            relocate_file(dat_filename, path, new_path)
        except:
            # rename_file(dat_filename, new_name, path, new_path)
            print("File already in folder")

if __name__ == "__main__":
    for files in nw.file_list()["files"]:
        dat_filename = files["name"]
        nw.file_delete(dat_filename)
