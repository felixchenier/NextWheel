"""
NextWheel Interface.

wheel_serveur.py: Emulator that simulates the operation of the wheel.
"""


import socket
import time
import json
import constant as c

import kineticstoolkit.lab as ktk


__author__ = "Clémence Starosta"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"


"""
_______________________________________________________________________________
                     Emulator which has the role of the server
_______________________________________________________________________________
"""


class Emulator(object):
    """A class that simulates the action of the instrumented wheel."""

    def __init__(self, kinetics: float):
        """
        Initialize the emulator.

        Parameters
        ----------
        filename : csv file with sample data

        Returns
        -------
        None
        """
        # extraction of the data, adding data to a table
        print("Extraction of the data wheel")
        self.kinetics = ktk.pushrimkinetics.read_file(
            c.filename, file_format='smartwheel')
        print("Sucessful extraction")

        # data processing
        self.kinetics = ktk.pushrimkinetics.calculate_velocity(self.kinetics)
        self.kinetics = ktk.pushrimkinetics.calculate_power(self.kinetics)

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

        # reception of the wheel status
        start = self.client.recv(255).decode("utf-8")

        # streaming status
        if start == "1":
            infinity = 0
            while (infinity < 1):
                for i in range(0, c.nbr_JSON_total, c.nbr_JSON_per_framme):
                    frame = self.create_json_frame(i)
                    send = json.dumps(frame)
                    self.client.send(send.encode())
                    time.sleep(c.real)
                    infinity += 1

        self.client.send("stop".encode())
        self.server.close()

    def create_json_frame(self, index: int) -> dict:
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
            obj.append({
                "time": float(self.kinetics.time[i]),

                "Forces": [float(self.kinetics.data["Forces"][i][0]),
                           float(self.kinetics.data["Forces"][i][1]),
                           float(self.kinetics.data["Forces"][i][2]),
                           float(self.kinetics.data["Forces"][i][3])],

                "Moments": [float(self.kinetics.data["Moments"][i][0]),
                            float(self.kinetics.data["Moments"][i][1]),
                            float(self.kinetics.data["Moments"][i][2]),
                            float(self.kinetics.data["Moments"][i][3])],

                "Velocity": float(self.kinetics.data["Velocity"][i]),

                "Power": float(self.kinetics.data["Power"][i])
            })

        trame = dict()
        trame["format"] = "json"
        trame["nombre"] = c.nbr_JSON_per_framme
        trame["data"] = obj
        return trame


if __name__ == "__main__":
    emul = Emulator(c.kinetics)
