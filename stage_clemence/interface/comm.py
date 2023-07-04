"""
NextWheel Interface.

comm.py: Submodule that communicates with the instrumented wheels.
"""

__author__ = "Clémence Starosta, Félix Chénier, Dominic Létourneau"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"

import threading
import struct
import datetime
import websocket
import requests


class Wheel:
    """
    A class that implements the communication with a wheel.

    Attributes
    ----------
    ip_address : str
        IP address (IPv4) of the wheel. Use 127.0.0.1 for the emulator.
    lists : lists that bring together the data
    """

    def __init__(
        self,
        lists={},
    ):
        self.lists = lists
        self.adc_values = []
        self.imu_values = []
        self.power_values = []

    def parse_power_frame(self, message: bytes) -> tuple:
        """
        Analysis of power frames.

        Performs conversions between Python values and C structures
        represented as Python bytes objects.

        Parameters
        ----------
        self
        message: framme (bytes)

        Returns
        -------
        vals (tuple)
        """
        if len(message) != 13:
            return []
        else:
            vals = struct.unpack_from('<3fB', message)
            return vals

    def parse_imu_frame(self, message: bytes) -> tuple:
        """
        Analysis of IMU frames.

        Performs conversions between Python values and C structures
        represented as Python bytes objects.

        Parameters
        ----------
        self
        message: framme (bytes)

        Returns
        -------
        vals (tuple)
        """
        if len(message) != 36:
            return []
        else:
            vals = struct.unpack_from('<9f', message)
            return vals

    def parse_adc_frame(self, message: bytes) -> tuple:
        """
        Analysis of ADC frames.

        Performs conversions between Python values and C structures
        represented as Python bytes objects.

        Parameters
        ----------
        self
        message: framme (bytes)

        Returns
        -------
        vals (tuple)
        """
        if len(message) != 32:
            return []
        else:
            vals = struct.unpack_from('<8f', message)
            return vals

    def parse_superframe(self, message: bytes, count: int):
        """
        Adding the frames to the corresponding lists.

        Frame conversion.

        Parameters
        ----------
        self
        message: framme (bytes)
        count: Message size

        Returns
        -------
        None
        """
        offset = 0
        header_size = 10

        for sub_count in range(count):
            (frame_type, timestamp, data_size) = struct.unpack_from(
                '<BQB', message[offset:offset+header_size])

        # Convert to real time
            timestamp = datetime.datetime.fromtimestamp(timestamp / 1e6)

            if frame_type == 2:
                self.lists["adc_values"].append(
                    (timestamp, self.parse_adc_frame(
                        message[
                            offset+header_size:offset+header_size+data_size])))
                if len(self.lists["adc_values"]) > 5000:
                    self.lists["adc_values"].pop(0)

            elif frame_type == 3:
                self.lists["imu_values"].append(
                    (timestamp, self.parse_imu_frame(
                        message[
                            offset+header_size:offset+header_size+data_size])))
                if len(self.lists["imu_values"]) > 500:
                    self.lists["imu_values"].pop(0)

            elif frame_type == 4:
                self.lists["power_values"].append(
                    (timestamp, self.parse_power_frame(
                        message[
                            offset+header_size:offset+header_size+data_size])))
                if len(self.lists["power_values"]) > 5:
                    self.lists["power_values"].pop(0)

            offset = offset + data_size + header_size

    def on_message(self, ws, message):
        """
        Read the message on the websocket.

        Parameters
        ----------
        self
        message: framme (bytes)
        ws: websocket

        Returns
        -------
        None
        """
        if type(message) is bytes:
            # Let's decode the header
            # uint8 type, uint64 timestamp, uint8 datasize (little endian)
            (frame_type, timestamp, data_size) = struct.unpack_from(
                '<BQB', message[0:10])
            # data = message[10:]

            if frame_type == 255:
                # data_size contains the number of frames
                self.parse_superframe(message[10:], data_size)

    def on_error(self, ws, error):
        """
        Display the errors of the websockets.

        Parameters
        ----------
        self
        ws: websocket
        error: websocket error

        Returns
        -------
        None
        """
        print(ws, error)

    def on_close(self, ws, close_status_code, close_msg):
        """
        Close the websocket.

        Parameters
        ----------
        self
        ws: websocket
        close_status_code
        close_msg

        Returns
        -------
        None
        """
        print("### closed ###", ws, close_status_code, close_msg)

    def on_open(self, ws):
        """
        Open the websocket.

        Parameters
        ----------
        self
        ws: websocket

        Returns
        -------
        None
        """
        print("Opened connection", ws)

    def connect(self, IP_adress):
        """
        Connect to the wheel websocket.

        Parameters
        ----------
        self

        Returns
        -------
        None.
        """
        # websocket.enableTrace(True)
        web_socket_ip_wheel = 'ws://' + IP_adress + '/ws'
        self.ws = websocket.WebSocketApp(web_socket_ip_wheel,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        t = threading.Thread(target=self.ws.run_forever)
        t.start()

    def disconnect(self):
        """
        Disconnect to the wheel websocket.

        Parameters
        ----------
        self

        Returns
        -------
        None.
        """
        self.ws.close()

    def reccord(self, IP_adress):
        """
        Launch the reccord on SD card.

        Using HTTP protocole

        Parameters
        ----------
        self

        Returns
        -------
        None.
        """
        URL = 'http://' + IP_adress + '/recording'
        requests.get(URL,
                     params={"recording": "start_recording"})

    def stop_reccord(self, IP_adress):
        """
        Stop the reccord on SD card.

        Using HTTP protocole

        Parameters
        ----------
        self

        Returns
        -------
        None.
        """
        URL = 'http://' + IP_adress + '/recording'
        requests.get(URL,
                     params={"recording": "stop_recording"})
