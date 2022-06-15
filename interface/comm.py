"""
NextWheel Interface.

comm.py: Submodule that communicates with the instrumented wheels.
"""

__author__ = "Clémence Starosta, Félix Chénier"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"

import socket
import threading
import json
import constant as c


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
        lists={},
    ):
        self.ip_address = ip_address
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.flag_stream = False
        self.lists = lists

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

    def _receive_streaming_thread(self):
        """
        Receives data from the stream, places it in the corresponding lists.

        Removes items from the list to avoid overloading the display.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Connecting main.py to the right socket
        while self.flag_stream is True:
            # Reception of the frames
            buffer = self.client.recv(c.LENGTH_BUFFER)
            if (buffer.decode() != "stop"):
                trame = json.loads(buffer.decode())

                for i_receiving in range(0, c.nbr_JSON_per_framme):
                    data = dict(trame["data"][i_receiving])

                    # Put data in the corresponding lists
                    self.lists['graph_time'].append(data['time'])
                    self.lists['graph_force0'].append(data['Forces'][0])
                    self.lists['graph_force1'].append(data['Forces'][1])
                    self.lists['graph_force2'].append(data['Forces'][2])
                    self.lists['graph_force3'].append(data['Forces'][3])
                    self.lists['graph_moment0'].append(data['Moments'][0])
                    self.lists['graph_moment1'].append(data['Moments'][1])
                    self.lists['graph_moment2'].append(data['Moments'][2])
                    self.lists['graph_moment3'].append(data['Moments'][3])
                    self.lists['graph_velocity'].append(
                        round(data['Velocity'], 2))
                    self.lists['graph_power'].append(round(data["Power"], 2))

                    # lists length management
                    if (
                            len(self.lists['graph_time']) >
                            3*int(c.nbr_JSON_per_second)
                    ):
                        del self.lists['graph_time'][0:int(
                            c.nbr_JSON_per_second)]
                        del self.lists['graph_force0'][0:int(
                            c.nbr_JSON_per_second)]
                        del self.lists['graph_force1'][0:int(
                            c.nbr_JSON_per_second)]
                        del self.lists['graph_force2'][0:int(
                            c.nbr_JSON_per_second)]
                        del self.lists['graph_force3'][0:int(
                            c.nbr_JSON_per_second)]
                        del self.lists['graph_moment0'][0:int(
                            c.nbr_JSON_per_second)]
                        del self.lists['graph_moment1'][0:int(
                            c.nbr_JSON_per_second)]
                        del self.lists['graph_moment2'][0:int(
                            c.nbr_JSON_per_second)]
                        del self.lists['graph_moment3'][0:int(
                            c.nbr_JSON_per_second)]
                        del self.lists['graph_velocity'][0:int(
                            c.nbr_JSON_per_second)]
                        del self.lists['graph_power'][0:int(
                            c.nbr_JSON_per_second)]
            else:
                print("end")

    def streaming(self):
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
        self.thread_streaming = threading.Thread(
            target=self._receive_streaming_thread
        )
        self.flag_stream = True
        self.thread_streaming.start()

    def end_streaming(self):
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
