"""
NextWheel Interface.

wheel_serveur.py: Emulator that simulates the operation of the wheel.
"""

import csv
import numpy as np
import socket
import time
import json
import constant as c
from typing import List

__author__ = "Clémence Starosta"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"


"""
_______________________________________________________________________________
                                CSV Functions
_______________________________________________________________________________
"""


def csv_count_line(filename: str) -> int:
    """
    Count line number in a csv file.

    Parameters
    ----------
    filename : file with csv file

    Returns
    -------
    Return number of line
    """
    with open(filename, 'r') as f:
        n = 0
        for line in f:
            n += 1
    return n


def read_file(filename: str) -> List[List[float]]:
    """
    Open the csv file and put data into a list of list.

    Parameters
    ----------
    filename : file with csv file
    i : line = time
    j : column = associated data (force or moment or channel)

    Returns
    -------
    Return list of list
    """
    with open(filename, newline='') as csvfile:
        data_wheel = np.zeros((csv_count_line(filename), 16))
        read = csv.reader(csvfile, delimiter=',')
        data_wheel = list(read)
        data_wheel_empty = list(np.float_(data_wheel))
        for i in range(0, csv_count_line(c.data_wheel_file)):
            for j in range(0, 15):
                data_wheel_empty[i][j] = round(data_wheel_empty[i][j], 5)
    return data_wheel_empty


"""
_______________________________________________________________________________
                     Emulator which has the role of the server
_______________________________________________________________________________
"""


class Emulator(object):
    """
    A class that simulates the action of the incremental wheel.

    Parameters
    ----------
    filename : file with csv file corresponding of the wheel data

    Returns
    -------
    Object of the class that corresponds to the emulator
    """

    def __init__(self, data_wheel_file: float):
        """
        Initialise of the emulator.

        Parameters
        ----------
        filename : csv file with the data wheel

        Returns
        -------
        None
        """
        # extraction of the data, adding data to a table
        print("Extraction of the data wheel")
        self.data_wheel = read_file(data_wheel_file)
        print("Sucessful extraction")

        # creation of the wheel server
        print("---------------------------------------------------")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Successful creation of the wheel emulator")
        self.server.bind(('', 50000))
        self.server.listen(5)
        print("---------------------------------------------------")
        self.client, self.adress_client = self.server.accept()
        print("Client :", self.adress_client)
        self.buffer = []

        self.flag = True

        while self.flag is True:
            # reception of the wheel status
            client_choice = self.client.recv(255).decode("utf-8")

            # streaming status
            if client_choice == "1":
                infinity = 0
                while (infinity < 1000):
                    print(infinity)
                    for i in range(0, c.nbr_JSON_total-75,
                                   c.nbr_JSON_per_framme):
                        frame = self.create_framme_json(i)
                        send = json.dumps(frame)
                        # print(send)
                        self.client.send(send.encode())
                        time.sleep(c.real)
                    infinity += 1

            # stop streaming status
            elif client_choice == "2":
                print("stop stream status")

            # end of the client connexion
            elif client_choice == "stop":
                print("Closed connection with " + self.adress_client)
                print("---------------------------------------------------")
                self.client.close()

    def create_framme_json(self, index: int) -> dict:
        """
        Create a frame of nbr_framme JSON data.

        Parameters
        ----------
        index : Index of the table

        Returns
        -------
        Return frames
        """
        obj = []
        for i in range(0+(index), (c.nbr_JSON_per_framme)+(index)):
            obj.append({"time": self.data_wheel[i][0],
                        "channel": [self.data_wheel[i][1],
                                    self.data_wheel[i][2],
                                    self.data_wheel[i][3],
                                    self.data_wheel[i][4],
                                    self.data_wheel[i][5],
                                    self.data_wheel[i][6]],

                        "battery": self.data_wheel[i][7],

                        "forces": [self.data_wheel[i][8],
                                   self.data_wheel[i][9],
                                   self.data_wheel[i][10],
                                   self.data_wheel[i][11]],

                        "moment": [self.data_wheel[i][12],
                                   self.data_wheel[i][13],
                                   self.data_wheel[i][14],
                                   self.data_wheel[i][15]]})

        trame = dict()
        trame["format"] = "json"
        trame["nombre"] = c.nbr_JSON_per_framme
        trame["data"] = obj
        return trame


if __name__ == "__main__":
    emul = Emulator(c.data_wheel_file)
