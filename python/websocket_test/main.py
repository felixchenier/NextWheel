import websocket
import _thread
import time
import struct
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import time
import datetime

HEADER_LENGTH = 10

adc_values = []
imu_values = []
power_values = []

# define and adjust figure
fig = plt.figure(figsize=(12, 6), facecolor='#DEDEDE')

adc_plot = plt.subplot(3, 1, 1)  # row, col, index
adc_plot.set_facecolor('#DEDEDE')

imu_plot = plt.subplot(3, 1, 2)  # row, col, index
imu_plot.set_facecolor('#DEDEDE')

power_plot = plt.subplot(3, 1, 3)  # row, col, index
power_plot.set_facecolor('#DEDEDE')


def parse_power_frame(message: bytes):
    if len(message) != 13:
        return []
    else:
        vals = struct.unpack_from('<3fB', message)
        return vals


def parse_imu_frame(message: bytes):
    if len(message) != 36:
        return []
    else:
        vals = struct.unpack_from('<9f', message)
        return vals


def parse_adc_frame(message: bytes):
    if len(message) != 32:
        return []
    else:
        vals = struct.unpack_from('<8f', message)
        return vals


def parse_superframe(message: bytes, count: int):
    offset = 0
    header_size = 10

    for sub_count in range(count):
        (frame_type, timestamp, data_size) = struct.unpack_from('<BQB', message[offset:offset+header_size])
        # print(f'sub header: {sub_count}/{count}', frame_type, timestamp, data_size)

        # Convert to real time
        timestamp = datetime.datetime.fromtimestamp(timestamp / 1e6)

        if frame_type == 2:
            adc_values.append((timestamp, parse_adc_frame(message[offset+header_size:offset+header_size+data_size])))
            if len(adc_values) > 10000:
                adc_values.pop(0)

        elif frame_type == 3:
            imu_values.append((timestamp, parse_imu_frame(message[offset+header_size:offset+header_size+data_size])))
            if len(imu_values) > 1000:
                imu_values.pop(0)

        elif frame_type == 4:
            power_values.append((timestamp, parse_power_frame(message[offset+header_size:offset+header_size+data_size])))
            if len(power_values) > 10:
                power_values.pop(0)

        offset = offset + data_size + header_size

    # result['adc'] = adc_values
    # result['imu'] = imu_values
    # result['power'] = power_values
    # return result


def on_message(ws, message):
    if type(message) is bytes:
        # Let's decode the header
        # uint8 type, uint64 timestamp, uint8 datasize (little endian)
        # print('message', len(message), message[0:10].hex())
        (frame_type, timestamp, data_size) = struct.unpack_from('<BQB', message[0:10])
        data = message[10:]
        # print('header: ', frame_type, timestamp, data_size, len(data))

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
def my_function(i):
    # ADC
    adc_plot.cla()
    x_vals = [x[0] for x in adc_values]
    y_vals = [x[1] for x in adc_values]
    adc_plot.plot(x_vals, y_vals)

    # IMU
    imu_plot.cla()
    x_vals = [x[0] for x in imu_values]
    y_vals = [x[1] for x in imu_values]
    imu_plot.plot(x_vals, y_vals)

    # POWER
    power_plot.cla()
    x_vals = [x[0] for x in power_values]
    y_vals = [x[1][0:3] for x in power_values]
    power_plot.plot(x_vals, y_vals)


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://10.0.1.23/ws",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    t = threading.Thread(target=ws.run_forever)
    t.start()

    ani = FuncAnimation(fig, my_function, interval=1000)
    plt.show()







