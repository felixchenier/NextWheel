"""
NextWheel Interface
===================
wheel_serveur.py: Emulator that simulates the operation of the wheel.
"""
import csv
import numpy as np
import socket
import time
import pickle

__author__ = "Clémence Starosta"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"

"""
_______________________________________________________________________________
                                CSV Functions
_______________________________________________________________________________
"""


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
        for i in range(0, csv_count_line(file_data_wheel)):
            for j in range(0, 15):
                data_wheel[i][j] = round(data_wheel[i][j], 5)
    return data_wheel


"""
_______________________________________________________________________________
                     Emulator which has the role of the server
_______________________________________________________________________________
"""


class emulator(object):
    """
    A class that simulates the action of the incremental wheel
    """

    def __init__(self, file_data_wheel: float):
        """
        initialization of the emulator

        Parameters
        ----------
        filename : csv file with the data wheel

        Returns
        -------
        Return number of line
        """

        # extraction of the data
        print("Extraction of the data wheel")
        self.data_wheel = open_add_data(file_data_wheel)
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
            client_choice = self.client.recv(255).decode("utf-8")

            if client_choice == "1":
                print("etat stream")
                for j in range(0, 42000, tramme_JSON):
                    trame = self.tramme_json(j)
                    s = pickle.dumps(trame)
                    self.client.send(s)
                    time.sleep(0.1)
                self.client.send("stop")

            elif client_choice == "2":
                print("etat non stream")

            elif client_choice == "stop":
                print("Closed connection with " + self.adress_client)
                print("---------------------------------------------------")
                self.client.close()

    def tramme_json(self, nbr_framme: int) -> dict:
        """
        Creation of frames consisting of j tables in JSON format

        Parameters
        ----------
        nbr_framme : number of json table in the frames

        Returns
        -------
        Return frames
        """
        obj = []
        for i in range(0+(nbr_framme), (tramme_JSON)+(nbr_framme)):
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
        trame["nombre"] = tramme_JSON
        trame["data"] = obj
        return trame


if __name__ == "__main__":
    file_data_wheel = 'kinetics.csv'
    tramme_JSON = 300
    emul = emulator(file_data_wheel)
