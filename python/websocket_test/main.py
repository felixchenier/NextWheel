import websocket
import _thread
import time


def on_message(ws, message):
    print(ws, message)


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

