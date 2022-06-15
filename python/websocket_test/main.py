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


def on_message(ws, message):
    if type(message) is bytes:
        # Let's decode the header
        # uint8 type, uint64 timestamp, uint8 datasize (little endian)
        # print('message', len(message), message[0:10].hex(), message[10:].hex())
        (frame_type, timestamp, data_size) = struct.unpack_from('<BQB', message[0:10])
        data = message[10:]
        # print('header: ', frame_type, timestamp, data_size, len(data))
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
    ws = websocket.WebSocketApp("ws://192.168.1.137/ws",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()  # Set dispatcher to automatic reconnection

