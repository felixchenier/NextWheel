"""The module contain the NextWheel class."""

import websocket
import struct
import threading
import numpy as np


class NextWheel:
    """The class permit communication with the SmartWheel."""

    def __init__(self, IP: str, HEADER_LENGTH: int = 10):
        self.IP = IP
        self.HEADER_LENGTH = HEADER_LENGTH
        self.TIME_ZERO = 0

        self.adc_values = []
        self.imu_values = []
        self.power_values = []
        self.encoder_values = []

    def __parse_config_frame(self, message: bytes):
        """Unpack data from the configurtion frame."""
        if len(message) == 20:
            unpacked_values = struct.unpack_from("<5I", message)
            print(
                f"Config accel_range:{unpacked_values[0]}, "
                f"gyro_range:{unpacked_values[1]}, "
                f"mag_range:{unpacked_values[2]}, "
                f"imu_sample_rate:{unpacked_values[3]}, "
                f"adc_sample_rate:{unpacked_values[4]}"
            )

    def __extract_value(self, frame_type: int, message: bytes, time: float):
        """Unpack data and save them in the appropriate variables."""
        if frame_type == 2:  # frame type of the ADC values
            if len(message) == 32:
                self.adc_values.append(
                    (time, struct.unpack_from("<8f", message))
                )

                if len(self.adc_values) > self.max_analog_samples:
                    self.adc_values.pop(0)

        elif frame_type == 3:  # frame type of the IMU
            if len(message) == 36:
                self.imu_values.append(
                    (time, struct.unpack_from("<9f", message))
                )

                if len(self.imu_values) > self.max_imu_samples:
                    self.imu_values.pop(0)

        elif frame_type == 4:  # frame type of the POWER
            if len(message) == 13:
                self.power_values.append(
                    (time, struct.unpack_from("<3fB", message))
                )

                if len(self.power_values) > self.max_power_samples:
                    self.power_values.pop(0)

        elif frame_type == 7:  # frame type of the ENCODER
            if len(message) == 8:
                self.encoder_values.append(
                    (time, struct.unpack_from("<q", message))
                )

                if len(self.encoder_values) > self.max_encoder_samples:
                    self.encoder_values.pop(0)

    def __parse_superframe(self, message: bytes, count: int):
        """Unpack superframe data and loop to scan the message."""
        offset = 0

        for sub_count in range(count):
            (frame_type, timestamp, data_size) = struct.unpack_from(
                "<BQB", message[offset : offset + self.HEADER_LENGTH]
            )

            self.__extract_value(
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
        """React on receiving a message from the SmartWheel."""
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
                self.__parse_config_frame(message[10:])

            if frame_type == 255:
                self.__parse_superframe(message[10:], data_size)

    def __on_open(self, ws):
        """React on opening a connection with the SmartWheel."""
        print("Opened connection", self.ws)

    def __on_error(self, ws, error):
        """React on an error with the SmartWheel."""
        self.close()
        print(self.ws, error)

    def __on_close(self, ws, close_status_code, close_msg):
        """React on closing a connection with the SmartWheel."""
        print("### closed ###", ws, close_status_code, close_msg)

    def connect(
        self,
        max_imu_samples: int = 1000,
        max_analog_samples: int = 1000,
        max_encoder_samples: int = 100,
        max_power_samples: int = 10,
    ):
        """Connect the SmartWheel with the WebSocketApp."""
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

    def fetch(self):
        """Fetch data and return a nested dictionary."""
        data = {
            "IMU": {
                "Time": np.array([t[0] for t in self.imu_values]),
                "Acc": np.array([i[1][:3] for i in self.imu_values]),
                "Gyro": np.array([i[1][3:6] for i in self.imu_values]),
                "Mag": np.array([i[1][6:] for i in self.imu_values]),
            },
            "Analog": {
                "Time": np.array([t[0] for t in self.adc_values]),
                "Force": np.array([i[1][:6] for i in self.adc_values]),
                "Spare": np.array([i[1][6:] for i in self.adc_values]),
            },
            "Encoder": {
                "Time": np.array([t[0] for t in self.encoder_values]),
                "Angle": np.array([i[1][0] for i in self.encoder_values]),
            },
            "Power": {
                "Time": np.array([t[0] for t in self.power_values]),
                "Voltage": np.array([i[1][0] for i in self.power_values]),
                "Current": np.array([i[1][1] for i in self.power_values]),
                "Power": np.array([i[1][2] for i in self.power_values]),
            },
        }

        self.adc_values = []
        self.imu_values = []
        self.power_values = []
        self.encoder_values = []

        return data

    def close(self):
        """Close the connection with the SmartWheel."""
        self.ws.close()
