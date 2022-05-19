#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NextWheel Interface
===================
comm.py: Submodule that communicates with the instrumented wheels.
"""

__author__ = "Félix Chénier"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"

import socket
import threading
import main as m


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

    def connect(self) -> bool:
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

    def disconnect(self, client) -> bool:
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

    def _streaming(self):
        """
        Start streaming.

        """
        # asks the wheel to go into stream mode
        self.client.send(bytes("1", encoding="utf-8"))
        # Launching the thread for receiving data from the wheel
        self.t_streaming = threading.Thread(target=m.receive_streaming)
        self.t_streaming.start()

    def _end_streaming(self):
        """
        Stop streaming.

        """
        # asks the wheel to go stop stream mode
        self.client.send(bytes("2", encoding="utf-8"))

    def client_name(self) -> any:
        """
        Returns the socket address

        Returns
        -------
        Return socket
        """
        return self.client


wheel = Wheel()
wheel.connect()

# management of gui threads


def streaming():
    wheel. _streaming()


def end_streaming():
    wheel._end_streaming()
