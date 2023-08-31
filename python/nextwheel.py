# -*- coding: utf-8 -*-
"""
The module has a NextWheel class that fetch data from the instrumented wheel.

It contain the Nextwheel class that communicate with the instrumented wheel.
"""

import websocket
import struct
import threading
import numpy as np
from typing import Tuple


class GlobalConfig:
    """
    Global configuration of the instrumented wheel. This will be used to store data current configuration
    and calculate conversions from raw data.
    """
    def __init__(self):
        self.adc_v_ref = 4.096
        self.adc_in_max = 1.25 * self.adc_v_ref
        self.adc_in_min = -1.25 * self.adc_v_ref

    def convert_adc_values(self, values: Tuple[int]) -> Tuple[float]:
        return tuple(self.convert_adc_value(value) for value in values)

    def convert_adc_value(self, value: int) -> float:
        # This is according to the 86888 datasheet
        return float(value) * (self.adc_in_max - self.adc_in_min) / 65535. + self.adc_in_min


class NextWheel:
    """
    Communicate with the instrumented wheel.

    The class permit to communicate with the instrumented wheel with 3 methods:
        - NextWheel.connect() allows to start a connection with the server via
        the WebSocketApp.
        - NextWheel.fetch() return the streamed data in a nested dictionary
        with all the usefull informations. Also clear the buffer.
        - NextWheel.close() close the connection with the instrumented wheel.
    It needs an IP address like in the example below.

    Exemple
    -------
    >>> from nextwheel import NextWheel
    >>> nw = NextWheel("196.168.1.254")
    >>> nw.connect()

    >>> print(nw.fetch())

    >>> nw.close()

    """

    def __init__(self, IP: str, HEADER_LENGTH: int = 10):
        self.IP = IP
        self.HEADER_LENGTH = HEADER_LENGTH
        self.TIME_ZERO = 0
        self.max_imu_samples = 0
        self.max_analog_samples = 0
        self.max_encoder_samples = 0
        self.max_power_samples = 0
        self.ws = None
        self._adc_values = []
        self._imu_values = []
        self._power_values = []
        self._encoder_values = []
        self._mutex = threading.Lock()
        self._config = GlobalConfig()

    def __extract_values(self, frame_type: int, message: bytes, time: float):
        """
        Extract functional values from the message.

        Utilize the WebSocket Binary Message Format to extract values from
        the message depending on the frame_type:
            2 - Frame type of the ADC
            3 - Frame type of the IMU
            4 - Frame type of the Power
            7 - Frame type of the Encoder

        Parameters
        ----------
        frame_type : int
            Frame type that determine the information in the message.
        message : bytes
            Message received from the instrumented wheel without header.
        time : float
            Time when the message has been received.

        Returns
        -------
        None.

        """
        if frame_type == 2:  # frame type of the ADC values
            if len(message) == 16:
                self._adc_values.append(
                    (time, self._config.convert_adc_values(struct.unpack_from("<8H", message)))
                )

                if len(self._adc_values) > self.max_analog_samples:
                    self._adc_values.pop(0)

        elif frame_type == 3:  # frame type of the IMU
            if len(message) == 18:
                self._imu_values.append(
                    (time, struct.unpack_from("<9h", message))
                )

                if len(self._imu_values) > self.max_imu_samples:
                    self._imu_values.pop(0)

        elif frame_type == 4:  # frame type of the POWER
            if len(message) == 13:
                self._power_values.append(
                    (time, struct.unpack_from("<3fB", message))
                )

                if len(self._power_values) > self.max_power_samples:
                    self._power_values.pop(0)

        elif frame_type == 7:  # frame type of the ENCODER
            if len(message) == 8:
                self._encoder_values.append(
                    (time, struct.unpack_from("<q", message))
                )

                if len(self._encoder_values) > self.max_encoder_samples:
                    self._encoder_values.pop(0)

    def __parse_superframe(self, message: bytes, count: int):
        """
        Unpack superframe and scan the message.

        The function loop over the message and call the function
        __extract_values to convert the bytes messages to other type more
        functional.

        Parameters
        ----------
        message : bytes
            Message received from the instrumented wheel without the first
            header.
        count : int
            Number of data present in the message.

        Returns
        -------
        None.

        """
        offset = 0

        for sub_count in range(count):
            (frame_type, timestamp, data_size) = struct.unpack_from(
                "<BQB", message[offset : offset + self.HEADER_LENGTH]
            )

            self.__extract_values(
                frame_type,
                message[
                    offset
                    + self.HEADER_LENGTH : offset
                    + self.HEADER_LENGTH
                    + data_size
                ],
                timestamp / 1e6 - self.TIME_ZERO,
            )

            offset = offset + data_size + self.HEADER_LENGTH

    def __on_message(self, ws, message):
        """
        Reaction of the WebSocketApp when receiving a message.

        The function analyse if the frame type is 1 or 255:
            - If frame_type = 1, this is the configuration frame. The function
            simply save the data.
            - If frame_type = 255, this is the superframe type. It calls the
            __parse_superframe function to read and scan the message.

        Parameters
        ----------
        ws : _app.WebSocketApp
            DESCRIPTION.
        message : bytes
            Information containing data in bytes.

        Returns
        -------
        None.

        """

        self._mutex.acquire()

        if type(message) is bytes:
            (frame_type, timestamp, data_size) = struct.unpack_from(
                "<BQB", message[0:10]
            )

            # Config frame (should always be first)
            if frame_type == 1:
                print("ConfigFrame detected")
                print(
                    "header: ",
                    frame_type,
                    timestamp,
                    data_size,
                    len(message[10:]),
                )
                self.TIME_ZERO = timestamp / 1e6

                if len(message[10:]) == 20:
                    self._config_values = struct.unpack_from(
                        "<5I", message[10:]
                    )

            if frame_type == 255:
                self.__parse_superframe(message[10:], data_size)

        self._mutex.release()

    def __on_open(self, ws):
        """Reaction of the WebSocketApp when the connection is open."""
        print("Opened connection", self.ws)

    def __on_error(self, ws, error):
        """Reaction of the WebSocketApp when there is an error."""
        self.close()
        print(self.ws, error)

    def __on_close(self, ws, close_status_code, close_msg):
        """Reaction of the WebSocketApp when the connection is close."""
        print("### closed ###", self.ws, close_status_code, close_msg)

    def connect(
        self,
        max_imu_samples: int = 1000,
        max_analog_samples: int = 1000,
        max_encoder_samples: int = 100,
        max_power_samples: int = 10,
    ):
        """
        Connect to the instrumented wheel via the WebSocketApp.

        Parameters
        ----------
        max_imu_samples : int, optional
            Maximum IMU data to keep in memory. The default is 1000.
        max_analog_samples : int, optional
            Maximum ADC data to keep in memory. The default is 1000.
        max_encoder_samples : int, optional
            Maximum encoder data to keep in memory. The default is 100.
        max_power_samples : int, optional
            Maximum Power data to keep in memory. The default is 10.

        Returns
        -------
        None.

        """
        self.max_imu_samples = max_imu_samples
        self.max_analog_samples = max_analog_samples
        self.max_encoder_samples = max_encoder_samples
        self.max_power_samples = max_power_samples

        self.ws = websocket.WebSocketApp(
            f"ws://{self.IP}/ws",
            on_open=self.__on_open,
            on_message=self.__on_message,
            on_error=self.__on_error,
            on_close=self.__on_close,
        )

        t = threading.Thread(target=self.ws.run_forever)
        t.start()

    def fetch(self) -> dict[str, dict[str, np.ndarray]]:
        """
        Fetch data and return a nested dictionary. Clear the buffer.

        Returns
        -------
        data : dict[str, dict[str, np.ndarray]]
            A dictionary of multiple dictionaries that contain latest
            informations on:
                - IMU values
                - ADC values
                - Encoder values
                - Power values
        """

        self._mutex.acquire()

        n_adc_values = len(self._adc_values)
        local_adc_values = [
            self._adc_values.pop(0) for _ in range(n_adc_values)
        ]

        n_imu_values = len(self._imu_values)
        local_imu_values = [
            self._imu_values.pop(0) for _ in range(n_imu_values)
        ]

        n_encoder_values = len(self._encoder_values)
        local_encoder_values = [
            self._encoder_values.pop(0) for _ in range(n_encoder_values)
        ]

        n_power_values = len(self._power_values)
        local_power_values = [
            self._power_values.pop(0) for _ in range(n_power_values)
        ]

        self._mutex.release()

        data = {
            "IMU": {
                "Time": np.array([t[0] for t in local_imu_values]),
                "Acc": np.array([i[1][:3] for i in local_imu_values]),
                "Gyro": np.array([i[1][3:6] for i in local_imu_values]),
                "Mag": np.array([i[1][6:] for i in local_imu_values]),
            },
            "Analog": {
                "Time": np.array([t[0] for t in local_adc_values]),
                "Force": np.array([i[1][:6] for i in local_adc_values]),
                "Spare": np.array([i[1][6:] for i in local_adc_values]),
            },
            "Encoder": {
                "Time": np.array([t[0] for t in local_encoder_values]),
                "Angle": np.array([i[1][0] for i in local_encoder_values]),
            },
            "Power": {
                "Time": np.array([t[0] for t in local_power_values]),
                "Voltage": np.array([i[1][0] for i in local_power_values]),
                "Current": np.array([i[1][1] for i in local_power_values]),
                "Power": np.array([i[1][2] for i in local_power_values]),
            },
        }

        return data

    def close(self):
        """
        Close the connection with the instrumented wheel.

        Returns
        -------
        None.

        """
        self.ws.close()
