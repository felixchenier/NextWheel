# -*- coding: utf-8 -*-
#
# Copyright 2023 NextWheel Developers

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This Python module provides the NextWheel class that fetches data from an
intrumented wheel.
"""

import websocket
import struct
import threading
import numpy as np
from enum import IntEnum
import requests
import os

# Constants

GRAVITY = 9.80665


class FrameType(IntEnum):
    """Identify frame type from websocket message."""

    CONFIG = 1
    ADC = 2
    IMU = 3
    POWER = 4
    ENCODER = 7
    SUPERFRAME = 255


class GlobalConfig:
    """
    Global configuration of the instrumented wheel.

    This is be used to store the current configuration and calculate
    conversions from raw data.

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

    def convert_adc_values(self, values: np.ndarray) -> np.ndarray:
        """
        Convert ADC values from ADC integers to volts.

        Parameters
        ----------
        values
            ADC outputs (integer).

        Returns
        -------
        np.ndarray
            ADC inputs in volts.

        """
        # This is according to the 86888 datasheet
        return (
            values * (self._adc_in_max - self._adc_in_min) / 65535
            + self._adc_in_min
        )

    def convert_accel_values(self, values: np.ndarray) -> np.ndarray:
        """
        Convert acceleration values from integers to m/s2.

        Parameters
        ----------
        values
            Integers as reported by the sensor.

        Returns
        -------
        np.ndarray
            Acceleration in m/s2.

        """
        factor = {
            2: self._accel_mg_lsb_2g * GRAVITY,
            4: self._accel_mg_lsb_4g * GRAVITY,
            8: self._accel_mg_lsb_8g * GRAVITY,
            16: self._accel_mg_lsb_16g * GRAVITY,
        }

        try:
            return values * factor[self.accel_range]
        except KeyError:
            raise ValueError("Invalid accel range")

    def convert_gyro_values(self, values: np.ndarray) -> np.ndarray:
        """
        Convert gyro values from integers to deg/s.

        Parameters
        ----------
        values
            Integers as reported by the sensor.

        Returns
        -------
        np.ndarray
            Angular velocity in m/s2.

        """
        factor = {
            125: self._gyro_sensitivity_125dps,
            250: self._gyro_sensitivity_250dps,
            500: self._gyro_sensitivity_500dps,
            1000: self._gyro_sensitivity_1000dps,
            2000: self._gyro_sensitivity_2000dps,
        }

        try:
            return values * factor[self.gyro_range]
        except KeyError:
            raise ValueError("Invalid gyro range")

    def convert_mag_values(self, values: np.ndarray) -> np.ndarray:
        """
        Convert magnetometer integers to ??.

        Parameters
        ----------
        values
            Integers as reported by the sensor.

        Returns
        -------
        np.ndarray
            To be determined.

        """
        # FIXME what is the output unit?
        if self.mag_range == 2500:
            return values * self._mag_ut_lsb
        else:
            raise ValueError("Invalid mag range")


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

    def __init__(self, IP: str, *, debug: bool = False):
        # General configuration
        self.IP = IP
        self.HEADER_LENGTH = 10
        self.TIME_ZERO = 0
        self.max_imu_samples = 0
        self.max_analog_samples = 0
        self.max_encoder_samples = 0
        self.max_power_samples = 0
        self._config = GlobalConfig()
        self._debug = debug

        # Communication stuff
        self.ws = None
        self._mutex = threading.Lock()

        # Data buffers. In these arrays, column 0 is the time
        self._adc_values = []  # type: list[np.ndarray]
        self._imu_values = []  # type: list[np.ndarray]
        self._power_values = []  # type: list[np.ndarray]
        self._encoder_values = []  # type: list[np.ndarray]

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
        if frame_type == FrameType.ADC:  # frame type of the ADC values
            if len(message) != 16:
                print(f"Unexpected message length of {len(message)} (ADC)")
                return

            self._adc_values.append(
                np.hstack([[time], struct.unpack_from("<8H", message)])
            )

            if len(self._adc_values) > self.max_analog_samples:
                self._adc_values.pop(0)

        elif frame_type == FrameType.IMU:  # frame type of the IMU
            if len(message) != 18:
                print(f"Unexpected message length of {len(message)} (IMU)")
                return

            self._imu_values.append(
                np.hstack(
                    [
                        [time],
                        self._config.convert_accel_values(
                            np.array(struct.unpack_from("<3h", message[:6]))
                        ),
                        self._config.convert_gyro_values(
                            np.array(struct.unpack_from("<3h", message[6:12]))
                        ),
                        self._config.convert_mag_values(
                            np.array(struct.unpack_from("<3h", message[12:18]))
                        ),
                    ]
                )
            )

            if len(self._imu_values) > self.max_imu_samples:
                self._imu_values.pop(0)

        elif frame_type == FrameType.POWER:  # frame type of the POWER
            if len(message) != 13:
                print(f"Unexpected message length of {len(message)} (POWER)")
                return

            self._power_values.append(
                np.hstack([[time], struct.unpack_from("<3fB", message)])
            )

            if len(self._power_values) > self.max_power_samples:
                self._power_values.pop(0)

        elif frame_type == FrameType.ENCODER:  # frame type of the ENCODER
            if len(message) != 8:
                print(f"Unexpected message length of {len(message)} (ENCODER)")
                return

            self._encoder_values.append(
                np.hstack([[time], struct.unpack_from("<q", message)])
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
        React to WebSocketApp message received.

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
            if frame_type == FrameType.CONFIG:
                if self._debug:
                    print("Configuration frame received.")
                self.TIME_ZERO = timestamp / 1e6

                if len(message[10:]) == 20:
                    (
                        accel_range,
                        gyro_range,
                        mag_range,
                        imu_sampling_rate,
                        adc_sampling_rate,
                    ) = struct.unpack_from("<5I", message[10:])

                    # Update configuration
                    self._config.accel_range = accel_range
                    self._config.gyro_range = gyro_range
                    self._config.mag_range = mag_range
                    self._config.imu_sampling_rate = imu_sampling_rate
                    self._config.adc_sampling_rate = adc_sampling_rate

            elif frame_type == FrameType.SUPERFRAME:
                self.__parse_superframe(message[10:], data_size)

        self._mutex.release()

    def __on_open(self, ws):
        """Reaction of the WebSocketApp when the connection is open."""
        if self._debug:
            print("Connected: ", self.ws)

    def __on_error(self, ws, error):
        """Reaction of the WebSocketApp when there is an error."""
        print(self.ws, error)
        self.close()

    def __on_close(self, ws, close_status_code, close_msg):
        """Reaction of the WebSocketApp when the connection is close."""
        if self._debug:
            print("Closed: ", self.ws, close_status_code, close_msg)

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
            f"ws://{self.IP}:81/",
            on_open=self.__on_open,
            on_message=self.__on_message,
            on_error=self.__on_error,
            on_close=self.__on_close,
        )

        t = threading.Thread(target=self.ws.run_forever)  # type: ignore
        t.start()

    def monitor(self) -> None:
        """
        Blocking function that monitors the sensors measurements.

        This function shows the current sensor states in a simple GUI for
        testing and monitoring. To log data, use NextWheel.fetch() instead.

        """
        # Don't import until needed.
        import nextwheel.monitor as nwm  # noqa

        nwm.monitor(self)

    def fetch(self) -> dict[str, dict[str, np.ndarray]]:
        """
        Fetch data and return a nested dictionary. Clear the buffer.

        Returns
        -------
        data : dict[str, dict[str, np.ndarray]]
            A dictionary of multiple dictionaries that contain latest
            informations on:
                - IMU values
                - Analog values
                - Encoder values
                - Power values
        """
        self._mutex.acquire()

        # Concatenate all samples in big numpy arrays
        adc_values = np.array(self._adc_values)
        imu_values = np.array(self._imu_values)
        encoder_values = np.array(self._encoder_values)
        power_values = np.array(self._power_values)

        # Reset the buffers
        self._adc_values = []
        self._imu_values = []
        self._encoder_values = []
        self._power_values = []

        self._mutex.release()

        has_imu = len(imu_values) > 0
        has_adc = len(adc_values) > 0
        has_enc = len(encoder_values) > 0
        has_pow = len(power_values) > 0

        # Output
        data = {
            "IMU": {
                "Time": imu_values[:, 0] if has_imu > 0 else np.array([]),
                "Acc": imu_values[:, 1:4] if has_imu > 0 else np.array([]),
                "Gyro": imu_values[:, 4:7] if has_imu > 0 else np.array([]),
                "Mag": imu_values[:, 7:] if has_imu > 0 else np.array([]),
            },
            "Analog": {
                "Time": adc_values[:, 0] if has_adc > 0 else np.array([]),
                "Force": adc_values[:, 1:7] if has_adc > 0 else np.array([]),
                "Spare": adc_values[:, 7:] if has_adc > 0 else np.array([]),
            },
            "Encoder": {
                "Time": encoder_values[:, 0] if has_enc > 0 else np.array([]),
                "Angle": encoder_values[:, 1] if has_enc > 0 else np.array([]),
            },
            "Power": {
                "Time": power_values[:, 0] if has_pow > 0 else np.array([]),
                "Voltage": power_values[:, 1] if has_pow > 0 else np.array([]),
                "Current": power_values[:, 2] if has_pow > 0 else np.array([]),
                "Power": power_values[:, 3] if has_pow > 0 else np.array([]),
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
        try:
            # If something has crashed somewhere, release the mutex for the
            # next connection.
            self._mutex.release()
        except RuntimeError:
            # No mutex was locked. That's fine.
            pass

    def set_time(self, unix_time: int) -> requests.Response:
        """
        Set the time of the instrumented wheel.

        Parameters
        ----------
        unix_time : int
            Unix time in seconds.

        Returns
        -------
        requests.Response

        """
        response = requests.post(
            f"http://{self.IP}/config_set_time", params={"time": unix_time}
        )
        return response

    def set_sensors_params(
        self,
        adc_sampling_rate: int,
        imu_sampling_rate: int,
        accelerometer_precision: int,
        gyrometer_precision: int,
    ) -> requests.Response:
        """
        Set the parameters of the instrumented wheel.

        Parameters
        ----------
        adc_sampling_rate
            Sampling rate for the forces in Hz. Valid values are 120, 240,
            480, 960, 1000, 2000
        imu_sampling_rate
            Sampling rate for the IMU, in Hz. Valid values are 60, 120, 240.
        accelerometer_precision
            Accelerometer range, in g. Value values are 2, 4, 8, 16.
        gyrometer_precision
            Gyrometer range, in degrees per second. Valid values are 250, 500,
            1000, 2000.

        Returns
        -------
        requests.Response

        """
        # TODO Validate params? We assume it is verified in the ESP32 firmware

        response = requests.post(
            f"http://{self.IP}/config_update",
            params={
                "adc_sampling_rate": adc_sampling_rate,
                "imu_sampling_rate": imu_sampling_rate,
                "accelerometer_precision": accelerometer_precision,
                "gyrometer_precision": gyrometer_precision,
            },
        )
        return response

    def get_sensors_params(self) -> requests.Response:
        """
        Get the parameters of the instrumented wheel sensors.

        Returns
        -------
        requests.Response

        """
        response = requests.get(f"http://{self.IP}/config")
        return response

    def get_system_state(self) -> requests.Response:
        """
        Get the system state of the instrumented wheel.

        Returns
        -------
        requests.Response

        """
        response = requests.get(f"http://{self.IP}/system_state")
        return response

    def start_recording(self) -> requests.Response:
        """
        Start recording data on the instrumented wheel.

        Returns
        -------
        requests.Response

        """
        response = requests.get(f"http://{self.IP}/start_recording")
        return response

    def stop_recording(self) -> requests.Response:
        """
        Stop recording data on the instrumented wheel.

        Returns
        -------
        requests.Response

        """
        response = requests.get(f"http://{self.IP}/stop_recording")
        return response

    def file_list(self) -> requests.Response:
        """
        Get the list of files on the instrumented wheel.

        Returns
        -------
        requests.Response

        """
        response = requests.get(f"http://{self.IP}/file_list")
        return response

    def file_download(self, filename: str, save_path: str = ".") -> int:
        """
        Download a file from the instrumented wheel.

        Parameters
        ----------
        filename
            The name of the file to download
        save_folder
            Optional. Where to save the file. The default is the current
            folder.

        Returns
        -------
        int
            The size of the file

        """
        param = {"file": filename}
        response = requests.get(
            f"http://{self.IP}/file_download", params=param, stream=True
        )
        if response.status_code == 200:
            with open(os.path.join(save_path, filename), "wb") as f:
                f.write(response.content)
                # Return size...
                return f.tell()

        # filed download
        return 0

    def file_delete(self, filename: str) -> requests.Response:
        """
        Delete a file from the instrumented wheel.

        Parameters
        ----------
        filename
            The name of the file to delete

        Returns
        -------
        requests.Response

        """
        response = requests.get(
            f"http://{self.IP}/file_delete", params={"file": filename}
        )
        return response
