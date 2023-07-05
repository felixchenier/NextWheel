# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 13:41:37 2023

@author: Nicolas
"""

import websocket
import struct
import threading


class NextWheel:
    def __init__(self, ip: str, max_length: int = 10):
        self.ip = ip
        self.max_length = max_length

    def __str__(self):
        return f"NextWheel Object Created. IP address : {self.ip}"

    def __on_open__(self, ws):
        print("Opened connection", ws)

    def __on_message__(self, ws, message):
        if type(message) is bytes:
            # Let's decode the header
            # uint8 type, uint64 timestamp, uint8 datasize (little endian)
            # print("message", len(message), message[0:10].hex())
            (frame_type, timestamp, data_size) = struct.unpack_from(
                "<BQB", message[0:10]
            )
            data = message[10:]
            # print("header: ", frame_type, timestamp, data_size, len(data))

    def __on_error__(self, ws, error):
        print(ws, error)

    def __on_close__(self, ws, close_status_code, close_msg):
        print("### closed ###", ws, close_status_code, close_msg)

    def connect(self):
        # websocket.enableTrace(True)  # Uncomment to print all received data
        self.ws = websocket.WebSocketApp(
            f"ws://{self.ip}/ws",
            on_open=self.__on_open__,
            on_message=self.__on_message__,
            on_error=self.__on_error__,
            on_close=self.__on_close__,
        )

        t = threading.Thread(target=self.ws.run_forever)
        t.start()


nw = NextWheel("192.168.1.254")
nw.connect()
