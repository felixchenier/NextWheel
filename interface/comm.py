#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NextWheel Interface
===================
comm.py: Submodule that communicates with the instrumented wheels.
"""

__author__ = "Félix Chénier"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"

import time
from typing import Optional, Dict, Any, Union
import socket
import json


class Wheel:
    """
    A class that implements the communication with a wheel.

    Attributes
    ----------
    ip_address : str
        IP address (IPv4) of the wheel. Use 127.0.0.1 for the emulator.
    port : int
        Port of the wheel.
    """

    def __init__(
        self,
        ip_address: str = '127.0.0.1',
        port: int = 50000,
    ):
        self.ip_address = ip_address
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connection(self) -> bool:  # changer en connect
        """
        Initialize the connection to the wheel.

        Returns
        -------
        True for success, False otherwise.
        """
        self.client.connect((self.ip_address, self.port))
        if self.client.fileno() != -1:
            return False
        else:
            return True

    def disconnect(self) -> bool:
        """
        Closes the connection to the wheel.

        Returns
        -------
        True for success, False otherwise.
        """
        self.client.close()
        if self.client.fileno() == -1:
            return True
        else:
            return False

    def set_config(
        *,
        ip_address: Optional[str],
        port: Optional[str],
        streaming_sample_rate: Optional[int],
        stream_forces: Optional[bool],
        stream_moments: Optional[bool],
        stream_raw_kinetics: Optional[bool],
        stream_battery: Optional[bool],
        stream_angle: Optional[bool],
        stream_velocity: Optional[bool],
        stream_raw_imu: Optional[bool],
        recording_sample_rate: Optional[int],
        record_forces: Optional[bool],
        record_moments: Optional[bool],
        record_raw_kinetics: Optional[bool],
        record_battery: Optional[bool],
        record_angle: Optional[bool],
        record_velocity: Optional[bool],
        record_raw_imu: Optional[bool],
    ) -> bool:
        """
        Configure the wheel.

        Parameters
        ----------
        TO DO

        Returns
        -------
        True for success, False otherwise.
        """
        raise NotImplementedError()

    def get_config() -> Union[None, Dict[str, Any]]:
        """
        Get the current wheel configuration.

        Returns
        -------
        A dictionary with every configuration as defined in set_config.
        Returns None if the operation did not succeed.
        """
        raise NotImplementedError()

    def start_streaming(self, choice: int, send_client, data_wheel) -> bool:
        """
        Start streaming.
        Returns
        -------
        True for success, False otherwise.
        """
        i = 0
        for elt in data_wheel:
            i += 1
            dict_obj = {'time': data_wheel[i][0],

                        'channel': [data_wheel[i][1], data_wheel[i][2],
                                    data_wheel[i][3], data_wheel[i][4],
                                    data_wheel[i][5], data_wheel[i][6]],

                        'battery': data_wheel[i][7],

                        'forces': [data_wheel[i][8], data_wheel[i][9],
                                   data_wheel[i][10], data_wheel[i][11]],

                        'moment': [data_wheel[i][12], data_wheel[i][13],
                                   data_wheel[i][14], data_wheel[i][15]]}
            dict_obj_json = json.dumps(dict_obj)
            send_client.sendall(bytes(dict_obj_json, encoding="utf-8"))
            time.sleep(0.05)

    def stop_streaming(self, thread: any) -> bool:
        """
        Stop streaming.

        Returns
        -------
        True for success, False otherwise.
        """
        thread.kill()
        thread.join()
        print("End of the streaming")
        return True

    def start_recording(self, choice: int) -> bool:
        """
        Start recording.

        Returns
        -------
        True for success, False otherwise.
        """
        return True

    def stop_recording(self, thread: any) -> bool:
        """
        Stop recording.

        Returns
        -------
        True for success, False otherwise.
        """
        thread.kill()
        thread.join()
        print("End of the reccording")
