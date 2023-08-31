import websocket
import _thread
import time
import struct
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import time
import datetime

HEADER_LENGTH = 10
HISTORY = 100  # Number of ADC and IMU sample to keep in memory

ADC_LOG_FILENAME = "log_adc.csv"
IMU_LOG_FILENAME = "log_imu.csv"

LOG_TO_FILE = False

# Thread mutex
mutex = threading.Lock()

adc_values = []
imu_values = []
power_values = []
encoder_values = []

if LOG_TO_FILE:
    fid_adc = open(ADC_LOG_FILENAME, "w")
    fid_adc.write(
        "Y,M,D,h,m,s,us,ch[0],ch[1],ch[2],ch[3],ch[4],ch[5]\n"
    )
    fid_imu = open(IMU_LOG_FILENAME, "w")
    fid_imu.write(
        "Y,M,D,h,m,s,us,"
        "acc[0],acc[1],acc[2],"
        "gyro[0],gyro[1],gyro[2],"
        "mag[0],mag[1],mag[2]\n"
    )
else:
    fid_adc = None
    fid_imu = None


mpl.rcParams["axes.prop_cycle"] = mpl.cycler(
    color=["r", "g", "b", "c", "m", "y", "k", "tab:orange"]
)
mpl.rcParams["figure.figsize"] = [10, 5]
mpl.rcParams["figure.dpi"] = 75
mpl.rcParams["lines.linewidth"] = 1

# define and adjust figure
fig = plt.figure(figsize=(12, 8))

adc_plot = plt.subplot(1, 1, 1)  # row, col, index
adc_plot.set_title("ADC")

# imu_plot = plt.subplot(4, 1, 2)  # row, col, index
# imu_plot.set_title("IMU")
#
# power_plot = plt.subplot(4, 1, 3)  # row, col, index
# power_plot.set_title("POWER")
#
# encoder_plot = plt.subplot(4, 1, 4)  # row, col, index
# encoder_plot.set_title("ENCODER")
plt.tight_layout()


class GlobalConfig:
    def __init__(self):
        self.adc_v_ref = 4.096
        self.adc_in_max = 1.25 * self.adc_v_ref
        self.adc_in_min = -1.25 * self.adc_v_ref

    def convert_adc_value(self, value: int) -> float:
        # This is according to the 86888 datasheet
        return float(value) * (self.adc_in_max-self.adc_in_min) / 65535. + self.adc_in_min


# This will hold all the configuration information
config = GlobalConfig()


def parse_power_frame(message: bytes):
    if len(message) != 13:
        return []
    else:
        vals = struct.unpack_from("<3fB", message)
        return vals


def parse_imu_frame(message: bytes):
    if len(message) != 36:
        return []
    else:
        vals = struct.unpack_from("<9f", message)
        return vals


def parse_adc_frame(message: bytes):
    # Now streaming only 6 channels
    # Need to do conversion to voltage
    if len(message) != 12:
        return []
    else:
        vals = struct.unpack_from("<6H", message)
        converted_vals = [config.convert_adc_value(v) for v in vals]
        return converted_vals


def parse_config_frame(message: bytes):
    if len(message) != 20:
        return []
    else:
        vals = struct.unpack_from("<5I", message)
        print(
            f"Config accel_range:{vals[0]}, gyro_range:{vals[1]}, "
            f"mag_range:{vals[2]}, imu_sample_rate:{vals[3]}, adc_sample_rate:{vals[4]}"
        )
        return vals


def parse_encoder_frame(message: bytes):
    if len(message) != 8:
        return []
    else:
        vals = struct.unpack_from("<q", message)
        return vals


def parse_superframe(message: bytes, count: int):
    offset = 0
    header_size = 10

    mutex.acquire()

    for sub_count in range(count):
        (frame_type, timestamp, data_size) = struct.unpack_from(
            "<BQB", message[offset : offset + header_size]
        )
        # print(f'sub header: {sub_count}/{count}', frame_type, timestamp, data_size)

        # Convert to real time
        timestamp = datetime.datetime.fromtimestamp(timestamp / 1e6)

        if frame_type == 2:
            new_values = parse_adc_frame(
                message[
                    offset + header_size : offset + header_size + data_size
                ]
            )
            adc_values.append(
                (
                    timestamp,
                    new_values,
                )
            )
            if len(adc_values) > HISTORY:
                adc_values.pop(0)

            if LOG_TO_FILE:
                # Log
                fid_adc.write(
                    f"{timestamp.year},"
                    f"{timestamp.month},"
                    f"{timestamp.day},"
                    f"{timestamp.hour},"
                    f"{timestamp.minute},"
                    f"{timestamp.second},"
                    f"{timestamp.microsecond}"
                )
                for i in range(len(new_values)):
                    fid_adc.write(f",{new_values[i]}")
                fid_adc.write("\n")

        elif frame_type == 3:
            new_values = parse_imu_frame(
                message[
                    offset + header_size : offset + header_size + data_size
                ]
            )
            imu_values.append(
                (
                    timestamp,
                    new_values,
                )
            )
            if len(imu_values) > 10:
                imu_values.pop(0)

            # Log
            if LOG_TO_FILE:
                fid_imu.write(
                    f"{timestamp.year},"
                    f"{timestamp.month},"
                    f"{timestamp.day},"
                    f"{timestamp.hour},"
                    f"{timestamp.minute},"
                    f"{timestamp.second},"
                    f"{timestamp.microsecond}"
                )
                for i in range(9):
                    fid_imu.write(f",{new_values[i]}")
                fid_imu.write("\n")

        elif frame_type == 4:
            power_values.append(
                (
                    timestamp,
                    parse_power_frame(
                        message[
                            offset
                            + header_size : offset
                            + header_size
                            + data_size
                        ]
                    ),
                )
            )
            if len(power_values) > 10:
                power_values.pop(0)

        elif frame_type == 7:
            encoder_values.append(
                (
                    timestamp,
                    parse_encoder_frame(
                        message[
                            offset
                            + header_size : offset
                            + header_size
                            + data_size
                        ]
                    ),
                )
            )
            if len(encoder_values) > HISTORY:
                encoder_values.pop(0)

        offset = offset + data_size + header_size

    mutex.release()

def on_message(ws, message):
    if type(message) is bytes:
        # Let's decode the header
        # uint8 type, uint64 timestamp, uint8 datasize (little endian)
        # print('message', len(message), message[0:10].hex())
        (frame_type, timestamp, data_size) = struct.unpack_from(
            "<BQB", message[0:10]
        )
        data = message[10:]
        # print('header: ', frame_type, timestamp, data_size, len(data))

        # Config frame (should always be first)
        if frame_type == 1:
            print("ConfigFrame detected")
            print("header: ", frame_type, timestamp, data_size, len(data))
            parse_config_frame(data)

        if frame_type == 255:
            # data_size contains the number of frames
            parse_superframe(message[10:], data_size)


def on_error(ws, error):
    print(ws, error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###", ws, close_status_code, close_msg)


def on_open(ws):
    print("Opened connection", ws)


# funct to update the data
def update_plots(i):
    """
    Update the plots.

    This function updates the plots using global variables adc_values,
    imu_values, power_values and encoder_values. It is normally called by
    Matplotlib's FunctAnimation class.
    """
    mutex.acquire()

    # ADC
    adc_plot.cla()
    adc_plot.set_title(f"[{i}] - Force Channels (ADC)")
    x_vals = [x[0] for x in adc_values]
    y_vals = [x[1] for x in adc_values]
    adc_plot.plot(x_vals, y_vals)

    # # IMU
    # imu_plot.cla()
    # imu_plot.set_title("IMU")
    # x_vals = [x[0] for x in imu_values]
    # y_vals = [x[1] for x in imu_values]
    # imu_plot.plot(x_vals, y_vals)
    #
    # # POWER
    # power_plot.cla()
    # power_plot.set_title("Battery level")
    # x_vals = [x[0] for x in power_values]
    # y_vals = [x[1][0:3] for x in power_values]
    # power_plot.plot(x_vals, y_vals)
    #
    # # ENCODER
    # encoder_plot.cla()
    # encoder_plot.set_title("Encoder")
    # x_vals = [x[0] for x in encoder_values]
    # y_vals = [x[1] for x in encoder_values]
    # encoder_plot.plot(x_vals, y_vals)

    mutex.release()


if __name__ == "__main__":
    # websocket.enableTrace(True)  # Uncomment to print all received data
    ws = websocket.WebSocketApp(
        "ws://10.0.1.2/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    t = threading.Thread(target=ws.run_forever)
    t.start()

    ani = FuncAnimation(fig, update_plots, interval=100)
    plt.show()
