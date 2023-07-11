# -*- coding: utf-8 -*-

import websocket
import struct
import threading
import numpy as np


class NextWheel:
    def __init__(self, ip: str, HEADER_LENGTH: int = 10):
        self.ip = ip
        self.HEADER_LENGTH = HEADER_LENGTH
        self.is_connect = False

        self.TIME_ZERO = 0

        self.adc_TIME = np.ndarray((0, 1))
        self.adc_value = np.ndarray((0, 9))

        self.imu_TIME = np.ndarray((0, 1))
        self.imu_value = np.ndarray((0, 9))

        self.power_TIME = np.ndarray((0, 1))
        self.power_values = np.ndarray((0, 3))

        self.encoder_TIME = np.ndarray((0, 1))
        self.encoder_values = np.ndarray((0, 1))

    def __parse_config_frame__(self, message: bytes):
        if len(message) != 20:
            return []
        else:
            vals = struct.unpack_from("<5I", message)
            print(
                f"Config accel_range:{vals[0]}, gyro_range:{vals[1]}, "
                f"mag_range:{vals[2]}, imu_sample_rate:{vals[3]}, adc_sample_rate:{vals[4]}"
            )
            return vals

    def __fetch_values__(self, frame_type: int, message: bytes, TIME: float):
        if frame_type == 2:  # frame type of the ADC values
            if len(message) == 32:
                self.adc_TIME = np.append(self.adc_TIME, TIME)
                vals = struct.unpack_from("<8f", message)

        elif frame_type == 3:  # frame type of the IMU
            if len(message) == 36:
                self.imu_TIME = np.append(self.imu_TIME, TIME)
                vals = struct.unpack_from("<9f", message)

        elif frame_type == 4:  # frame type of the POWER
            if len(message) == 13:
                self.power_TIME = np.append(self.power_TIME, TIME)
                vals = struct.unpack_from("<3fB", message)

        elif frame_type == 7:  # frame type of the ENCODER
            if len(message) == 8:
                self.encoder_TIME = np.append(self.encoder_TIME, TIME)
                vals = struct.unpack_from("<q", message)

    def __parse_superframe__(self, message: bytes, count: int):
        offset = 0

        for sub_count in range(count):
            (frame_type, timestamp, data_size) = struct.unpack_from(
                "<BQB", message[offset : offset + self.HEADER_LENGTH]
            )

            self.__fetch_values__(
                frame_type,
                message[
                    offset
                    + self.HEADER_LENGTH : offset
                    + self.HEADER_LENGTH
                    + data_size
                ],
                timestamp / 1e6,
            )

            offset = offset + data_size + self.HEADER_LENGTH

    def __on_message__(self, ws, message):
        if type(message) is bytes:
            # Let's decode the header
            # uint8 type, uint64 timestamp, uint8 datasize (little endian)
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
                self.TIME = timestamp / 1e6
                self.__parse_config_frame__(message[10:])

            if frame_type == 255:
                # print(frame_type, timestamp, data_size, len(message[10:]))
                # data_size contains the number of frames
                self.__parse_superframe__(message[10:], data_size)

    def __on_open__(self, ws):
        self.is_connect = True
        print("Opened connection", self.ws)

    def __on_error__(self, ws, error):
        self.close()
        print(self.ws, error)

    def __on_close__(self, ws, close_status_code, close_msg):
        self.is_connect = False
        print("### closed ###", ws, close_status_code, close_msg)

    def connect(
        self,
        max_imu_samples: int = 1000,
        max_analog_samples: int = 1000,
        max_encoder_samples: int = 100,
        max_power_samples: int = 10,
    ):
        self.max_imu_samples = max_imu_samples
        self.max_analog_samples = max_analog_samples
        self.max_encoder_samples = max_encoder_samples
        self.max_power_samples = max_power_samples

        self.ws = websocket.WebSocketApp(
            f"ws://{self.ip}/ws",
            on_open=self.__on_open__,
            on_message=self.__on_message__,
            on_error=self.__on_error__,
            on_close=self.__on_close__,
        )

        t = threading.Thread(target=self.ws.run_forever)
        t.start()

    def close(self):
        self.ws.close()


nw = NextWheel("192.168.1.254")
nw.connect()
# nw.close()
