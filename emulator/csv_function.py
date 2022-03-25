#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NextWheel Interface
===================
csv_functions.py: Submodule that manages the csv functions
"""

import numpy as np
import csv

__author__ = "Clémence Starosta"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"


file_data_wheel = 'kinetics.csv'
timer = True


def csv_count_line(filename: any) -> int:
    """
    count line number in a csv file

    Parameters
    ----------
    filename : file with csv file

    Returns
    -------
    Return number of line
    """
    with open(filename, 'r') as f:
        i = 0
        for line in f:
            i += 1
    return i


def open_add_data(filename: any) -> float:
    """
    Open the csv file and put data into a tab

    Parameters
    ----------
    filename : file with csv file

    Returns
    -------
    Return tab of data
    """
    with open(filename, newline='') as csvfile:
        data_wheel1 = np.zeros((csv_count_line(filename), 16))
        read = csv.reader(csvfile, delimiter=',')
        data_wheel1 = list(read)
        data_wheel = list(np.float_(data_wheel1))
    return data_wheel


def print_data_wheel(data: float):
    """
    Displaying the data table

    Parameters
    ----------
    data : tab of data

    """
    for elt in data:
        np.set_printoptions(precision=6, suppress=True)
        print(str(elt), ", ")


def average_data(data: float, filename: any) -> float:
    """
    Averages ten data and rounds up to the nearest ms

    Parameters
    ----------
    data : tab of data
    filename : file with csv file

    Returns
    -------
    Return tab of data
    """
    average_data = np.zeros((csv_count_line(filename), 15))
    for i in range(0, csv_count_line(file_data_wheel)-10, 10):
        for j in range(0, 14):
            elt = (data[i][j]+data[i+1][j]+data[i+2][j]+data[i+3][j]
                   + data[i+4][j] + data[i+5][j]+data[i+6][j]+data[i+7][j]
                   + data[i+8][j] + data[i+9][j])/10
            k = int(i/10)
            average_data[k][j] = elt
    for i in range(0, int(csv_count_line(file_data_wheel)/10)):
        average_data[i][0] = round(average_data[i][0], 3)
    return average_data
