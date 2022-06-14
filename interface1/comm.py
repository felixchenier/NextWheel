"""
NextWheel Interface.

comm.py: Submodule that communicates with the instrumented wheels.
"""

__author__ = "Félix Chénier"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"

import socket
import threading
import _init_ as m


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
        self.flag_stream = False

    def connect(self) -> bool:
        """
        Initialize the connection to the wheel.

        When the gui starts, wheel will automatically connect to the server

        Parameters
        ----------
        self

        Returns
        -------
        True for success, False otherwise.
        """
        self.client.connect((self.ip_address, self.port))
        if self.client.fileno() != -1:
            return False
        else:
            return True

    def disconnect(self, client: object) -> bool:
        """
        Close the connection to the wheel.

        Parameters
        ----------
        self

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
        Send the streaming status to the emulator.

        Launching the reception management thread in main.py.

        Parameters
        ----------
        self

        Returns
        -------
        None
        """
        # asks the wheel to go into stream mode
        self.client.send(bytes("1", encoding="utf-8"))
        # Launching the thread for receiving data from the wheel
        self.thread_streaming = threading.Thread(target=m.receive_streaming)
        self.flag_stream = True
        self.thread_streaming.start()

    def _end_streaming(self):
        """
        Send the end streaming status to the emulator.

        Parameters
        ----------
        self

        Returns
        -------
        None
        """
        # asks the wheel to go stop stream mode
        self.flag_stream = False

    def client_name(self) -> any:
        """
        Return the socket address.

        Parameters
        ----------
        self

        Returns
        -------
        Return socket
        """
        return self.client


# creation of the wheel object
wheel = Wheel()

# connexion to the emulator
wheel.connect()

# management of gui threads


def streaming():
    """
    Manage streaming threads of the Wheel class.

    The _streaming function of the Wheel class will constantly listen and
    check if we want to go to the streaming state.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    wheel._streaming()


def end_streaming():
    """
    Manage end streaming threads of the Wheel class.

    The _end_streaming function of the Wheel class will constantly listen and
    check if we want to quite the streaming state.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    wheel._end_streaming()
