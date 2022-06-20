import websocket
import _thread
import time
import struct

HEADER_LENGTH = 10

count = 0


def parse_adc_frame(message: bytes):
    if len(message) != 32:
        return []
    else:
        vals = struct.unpack_from('<8f', message)
        return vals


def parse_superframe(message: bytes, count: int):
    offset = 0
    header_size = 10
    print('Should have subs', count)
    sub_count = 0

    result = dict()
    adc_values = []
    while offset < len(message):
        sub_count += 1
        (frame_type, timestamp, data_size) = struct.unpack_from('<BQB', message[offset:offset+header_size])
        # print(f'sub header: {sub_count}/{count}', frame_type, timestamp, data_size)

        if frame_type == 2:
            adc_values.append((timestamp, parse_adc_frame(message[offset+header_size:offset+header_size+data_size])))

        offset = offset + data_size + header_size

    result['adc'] = adc_values

    return result


def on_message(ws, message):
    if type(message) is bytes:
        # Let's decode the header
        # uint8 type, uint64 timestamp, uint8 datasize (little endian)
        print('message', len(message), message[0:10].hex())
        (frame_type, timestamp, data_size) = struct.unpack_from('<BQB', message[0:10])
        data = message[10:]
        print('header: ', frame_type, timestamp, data_size, len(data))

        if frame_type == 255:
            # data_size contains the number of frames
            parse_superframe(message[10:], data_size)

        if frame_type == 2:
            values = parse_adc_frame(data)
            # print(values)
            global count
            count = count + 1
            print('Total count: ', count)





def on_error(ws, error):
    print(ws, error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###", ws, close_status_code, close_msg)


def on_open(ws):
    print("Opened connection", ws)


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://10.0.1.23/ws",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()  # Set dispatcher to automatic reconnection

