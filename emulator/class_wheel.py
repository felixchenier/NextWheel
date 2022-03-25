#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NextWheel Interface
===================
class_wheel.py: Submodule that manages the classes
"""

import threading
import time
import sys
from typing import Optional, Dict, Any, Union
import socket
import csv_function as csvf
import matplotlib.pyplot as plt
import numpy as np

__author__ = "Félix Chénier"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"


file_data_wheel = 'kinetics.csv'
data = csvf.open_add_data(file_data_wheel)
data_wheel = csvf.average_data(data, file_data_wheel)


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
            return True
        else:
            return False

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

    def start_streaming(self, choice: int) -> bool:
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
