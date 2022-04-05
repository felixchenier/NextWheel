#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NextWheel Interface
===================
comm.py: Submodule that manages the classes and functions
"""

import threading
import time
import sys
from typing import Optional, Dict, Any, Union
import socket
import matplotlib.pyplot as plt
import numpy as np
import csv


__author__ = "Félix Chénier"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"

"""
___________________________________
    CSV Functions
___________________________________
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
    return data_wheel


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


file_data_wheel = 'kinetics.csv'
data = open_add_data(file_data_wheel)
data_wheel = average_data(data, file_data_wheel)

"""
___________________________________
    Class
___________________________________
"""


class Wheel:
    """
    A class that implements the communication with a wheel.

    Attributes
    ----------
    ip_address : str
        IP address (IPv4) of the wheel. Use 127.0.0.1 for the emulator.
    port : int
        Port of the wheel.
    """

    def __init__(
        self,
        ip_address: str = '127.0.0.1',
        port: int = 50000,
    ):
        self.ip_address = ip_address
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_wheel = data_wheel

    def connection(self) -> bool:
        """
        Initialize the connection to the wheel.

        Returns
        -------
        True for success, False otherwise.
        """
        self.client.connect((self.ip_address, self.port))
        if self.client.fileno() != -1:
            return False
        else:
            return True

    def disconnect(self) -> bool:
        """
        Closes the connection to the wheel.

        Returns
        -------
        True for success, False otherwise.
        """
        self.client.close()
        if self.client.fileno() == -1:
            return True
        else:
            return False

    def set_config(
        *,
        ip_address: Optional[str],
        port: Optional[str],
        streaming_sample_rate: Optional[int],
        stream_forces: Optional[bool],
        stream_moments: Optional[bool],
        stream_raw_kinetics: Optional[bool],
        stream_battery: Optional[bool],
        stream_angle: Optional[bool],
        stream_velocity: Optional[bool],
        stream_raw_imu: Optional[bool],
        recording_sample_rate: Optional[int],
        record_forces: Optional[bool],
        record_moments: Optional[bool],
        record_raw_kinetics: Optional[bool],
        record_battery: Optional[bool],
        record_angle: Optional[bool],
        record_velocity: Optional[bool],
        record_raw_imu: Optional[bool],
    ) -> bool:
        """
        Configure the wheel.

        Parameters
        ----------
        TO DO

        Returns
        -------
        True for success, False otherwise.
        """
        raise NotImplementedError()

    def get_config() -> Union[None, Dict[str, Any]]:
        """
        Get the current wheel configuration.

        Returns
        -------
        A dictionary with every configuration as defined in set_config.
        Returns None if the operation did not succeed.
        """
        raise NotImplementedError()

    def start_streaming(self, choice: int, send_client) -> bool:
        """
        Start streaming.

        Returns
        -------
        True for success, False otherwise.
        """
        i = 0
        for elt in data_wheel:
            i += 1
            print(data_wheel[i][0], " ms :", data_wheel[i][choice+1])
            send_client.sendall(
                bytes(str(data_wheel[i][0]), encoding="utf-8"))
            send_client.sendall(bytes(str(data_wheel[i][choice+1]),
                                      encoding="utf-8"))
            time.sleep(2)

    def stop_streaming(self, thread: any) -> bool:
        """
        Stop streaming.

        Returns
        -------
        True for success, False otherwise.
        """
        thread.kill()
        thread.join()
        print("End of the streaming")
        return True

    def start_recording(self, choice: int) -> bool:
        """
        Start recording.

        Returns
        -------
        True for success, False otherwise.
        """
        i = 0
        x = []
        y = []
        for elt in data_wheel:
            i += 1
            print(data_wheel[i][0], " ms :", data_wheel[i][choice+1])
            x.append(data_wheel[i][0])
            y.append(data_wheel[i][choice+1])
            np.linspace(0, data_wheel[i][0])
            plt.title("Analyze")
            plt.xlabel('Time')
            plt.plot(x, y)
            plt.savefig("graph.png")
            plt.show()
            time.sleep(2)

    def stop_recording(self, thread: any) -> bool:
        """
        Stop recording.

        Returns
        -------
        True for success, False otherwise.
        """
        thread.kill()
        thread.join()
        print("End of the reccording")


# fr.acervolima.com/python-differentes-facons-de-tuer-un-fil/


class thread_with_trace(threading.Thread):
    """
    A class that helps manage threads

    Attributes
    ----------
    thread
    """

    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        """
        Launch of the thread
       """
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        """
        Create a thread trace
       """
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame: any, event: any, arg: any) -> any:
        """
        Find the local thread trace

        Parameters
        ----------
        frame, event, arg : parameter of the trace thread

        Returns
        -------
        Return the trace or None.
       """
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame: any, event: any, arg: any) -> any:
        """
        Stop execution of the local trace

        Parameters
        ----------
        frame, event, arg : parameter of the trace thread

        Returns
        -------
        Return the local trace
       """
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        """
        Killed the thread
       """
        self.killed = True


"""
__________________________________________
    Client (communication client/server)
_________________________________________
"""


def client():
    """
    Client that manages the client/server communication to the wheel
    """
    connexion = True

    wheel = Wheel()
    wheel.__init__()

    connect = wheel.connection()
    if connect is False:
        print("Server connection error")
    else:
        print("Connected to the server")
        print("---------------------------------------------------")

    client = wheel.client

    connexion = True

    while connexion is True:
        print("Welcome to the NextWheel interface")
        print("---------------------------------------------------")
        print("What do you want to do?")
        print("   -Start the streaming : tape 1")
        print("   -Stop the streaming:   tape 2")
        print("   -Start the recording:  tape 3")
        print("   -Stop the recording:   tape 4")
        print("   -Exit:                 tape stop")
        print("   -Close the server:     tape close")
        print("Your choice : ")
        option = input()

        if option == '1':
            client.sendall(bytes(option, encoding="utf-8"))
            print("What data do you want to analyse?")
            print("| 0  : Channel[0] |")
            print("| 1  : Channel[1] |")
            print("| 2  : Channel[2] |")
            print("| 3  : Channel[3] |")
            print("| 4  : Channel[4] |")
            print("| 5  : Channel[5] |")
            print("| 6  : Battery    |")
            print("| 7  : Forces[0]  |")
            print("| 8  : Forces[1]  |")
            print("| 9  : Forces[2]  |")
            print("| 10 : Forces[3]  |")
            print("| 11 : Moment[0]  |")
            print("| 12 : Forces[1]  |")
            print("| 13 : Forces[2]  |")
            print("| 14 : Forces[3]  |")
            print("---------------------------------------------------")
            choice = input()
            client.sendall(bytes(choice, encoding="utf-8"))
            print("")

            if option == '2':
                client.sendall(bytes(option, encoding="utf-8"))
                print("")

            if option == '3':
                client.sendall(bytes(option, encoding="utf-8"))
                print("What data do you want to analyse?")
                print("| 0  : Channel[0] |")
                print("| 1  : Channel[1] |")
                print("| 2  : Channel[2] |")
                print("| 3  : Channel[3] |")
                print("| 4  : Channel[4] |")
                print("| 5  : Channel[5] |")
                print("| 6  : Battery    |")
                print("| 7  : Forces[0]  |")
                print("| 8  : Forces[1]  |")
                print("| 9  : Forces[2]  |")
                print("| 10 : Forces[3]  |")
                print("| 11 : Moment[0]  |")
                print("| 12 : Forces[1]  |")
                print("| 13 : Forces[2]  |")
                print("| 14 : Forces[3]  |")
                print("---------------------------------------------------")
                choice = input()
                client.sendall(bytes(choice, encoding="utf-8"))
                print("")

        if option == '4':
            client.sendall(bytes(option, encoding="utf-8"))
            print("")

        elif option == "stop":
            client.sendall(bytes(option, encoding="utf-8"))
            disconnect = wheel.disconnect()
            if disconnect is False:
                print("Server disconnection error")
            else:
                print("Deconnected from the server")
                print("-------------------------------------------------")
                connexion = False
