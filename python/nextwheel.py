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
import requests


class GlobalConfig:
    """
    Global configuration of the instrumented wheel. This will be used to store current configuration
    and calculate conversions from raw data.
    """
    def __init__(self):
        # IMU CONFIG
        self.accel_range = 16
        self.gyro_range = 2000
        self.mag_range = 2500
        self.imu_rate = 1000

        # ADC CONFIG
        self.adc_rate = 1000

        # ACCORDING TO ADS8688 DATASHEET
        self._adc_v_ref = 4.096
        # ADC RANGING from [-5,5] V according to PCB design
        self._adc_in_max = 1.25 * self._adc_v_ref
        self._adc_in_min = -1.25 * self._adc_v_ref

        # ACCORDING TO BMX160 DATASHEET
        self._gravity_earth = 9.80665
        self._accel_mg_lsb_2g = 0.000061035
        self._accel_mg_lsb_4g = 0.000122070
        self._accel_mg_lsb_8g = 0.000244141
        self._accel_mg_lsb_16g = 0.000488281
        self._gyro_sensitivity_125dps = 0.0038110
        self._gyro_sensitivity_250dps = 0.0076220
        self._gyro_sensitivity_500dps = 0.0152439
        self._gyro_sensitivity_1000dps = 0.0304878
        self._gyro_sensitivity_2000dps = 0.0609756
        self._mag_ut_lsb = 0.3

    def update_config(self, accel_range: int, gyro_range: int, mag_range: int,  imu_rate: int, adc_rate: int):
        self.accel_range = accel_range
        self.gyro_range = gyro_range
        self.mag_range = mag_range
        self.imu_rate = imu_rate
        self.adc_rate = adc_rate

    def convert_adc_values(self, values: Tuple[int]) -> Tuple[float]:
        return tuple(self.convert_adc_value(value) for value in values)

    def convert_adc_value(self, value: int) -> float:
        # This is according to the 86888 datasheet
        return float(value) * (self._adc_in_max - self._adc_in_min) / 65535. + self._adc_in_min

    def convert_accel_values(self, values: Tuple[int]) -> Tuple[float]:
        return tuple(self.convert_accel_value(value) for value in values)

    def convert_accel_value(self, values: int) -> float:
        if self.accel_range == 2:
            return float(values) * self._accel_mg_lsb_2g * self._gravity_earth
        elif self.accel_range == 4:
            return float(values) * self._accel_mg_lsb_4g * self._gravity_earth
        elif self.accel_range == 8:
            return float(values) * self._accel_mg_lsb_8g * self._gravity_earth
        elif self.accel_range == 16:
            return float(values) * self._accel_mg_lsb_16g * self._gravity_earth
        else:
            print('Invalid accel range')
            return 0

    def convert_gyro_values(self, values: Tuple[int]) -> Tuple[float]:
        return tuple(self.convert_gyro_value(value) for value in values)

    def convert_gyro_value(self, values: int) -> float:
        if self.gyro_range == 125:
            return float(values) * self._gyro_sensitivity_125dps
        elif self.gyro_range == 250:
            return float(values) * self._gyro_sensitivity_250dps
        elif self.gyro_range == 500:
            return float(values) * self._gyro_sensitivity_500dps
        elif self.gyro_range == 1000:
            return float(values) * self._gyro_sensitivity_1000dps
        elif self.gyro_range == 2000:
            return float(values) * self._gyro_sensitivity_2000dps
        else:
            print('Invalid gyro range')
            return 0

    def convert_mag_values(self, values: Tuple[int]) -> Tuple[float]:
        return tuple(self.convert_mag_value(value) for value in values)

    def convert_mag_value(self, values: int) -> float:
        if self.mag_range == 2500:
            return float(values) * self._mag_ut_lsb
        else:
            print('Invalid mag range')
            return 0


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
                # Converting to m/s^2, deg/s and uT
                acc_values = self._config.convert_accel_values(struct.unpack_from("<3h", message[:6]))
                gyro_values = self._config.convert_gyro_values(struct.unpack_from("<3h", message[6:12]))
                mag_values = self._config.convert_mag_values(struct.unpack_from("<3h", message[12:18]))

                # NOTE + will concat the tuples
                self._imu_values.append(
                    (time, acc_values + gyro_values + mag_values)
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
                    (accel_range, gyro_range, mag_range, imu_sampling_rate, adc_sampling_rate) = \
                        struct.unpack_from("<5I", message[10:])

                    self._config.update_config(accel_range, gyro_range, mag_range, imu_sampling_rate, adc_sampling_rate)

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

    def set_time(self, unix_time: int) -> requests.Response:
        """
        Set the time of the instrumented wheel.

        Parameters
        ----------
        unix_time : int
            Unix time in seconds.

        Returns
        -------
        response : requests.Response

        """
        response = requests.post(f"http://{self.IP}/config_set_time", params={"time": unix_time})
        return response

    def set_sensors_params(self, adc_sampling_rate: int, imu_sampling_rate: int,
                          accelerometer_precision: int, gyrometer_precision: int) -> requests.Response:
        """
        Set the parameters of the instrumented wheel.
        :param adc_sampling_rate: valid values are : [120, 240, 480, 960, 1000, 2000] in Hz
        :param imu_sampling_rate: valid values are: [60, 120, 240] in Hz
        :param accelerometer_precision: valid values are: [2,4,8,16] in g
        :param gyrometer_precision: valid values are [250, 500, 1000, 2000] dps (degrees per second)
        :return:
        response: requests.Response
        """
        # TODO Validate params? We assume it is verified in the ESP32 firmware

        response = requests.post(f"http://{self.IP}/config_update",
                                 params={"adc_sampling_rate": adc_sampling_rate,
                                         "imu_sampling_rate": imu_sampling_rate,
                                         "accelerometer_precision": accelerometer_precision,
                                         "gyrometer_precision": gyrometer_precision})
        return response

    def get_sensors_params(self) -> requests.Response:
        """
        Get the parameters of the instrumented wheel sensors.
        :return:
        response: requests.Response
        """
        response = requests.get(f"http://{self.IP}/config")
        return response
