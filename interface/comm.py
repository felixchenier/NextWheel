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


from typing import Optional, Dict, Any, Union


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
        port: int = 6666,
    ):
        self.ip_address = ip_address
        self.port = port

    def connect() -> bool:
        """
        Initialize the connection to the wheel.

        Returns
        -------
        True for success, False otherwise.
        """
        raise NotImplementedError()

    def disconnect() -> bool:
        """
        Closes the connection to the wheel.

        Returns
        -------
        True for success, False otherwise.
        """
        raise NotImplementedError()

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
        TODO

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

    def start_streaming() -> bool:
        """
        Start streaming.

        Returns
        -------
        True for success, False otherwise.
        """
        raise NotImplementedError()

    def stop_streaming() -> bool:
        """
        Stop streaming.

        Returns
        -------
        True for success, False otherwise.
        """
        raise NotImplementedError()

    def start_recording() -> bool:
        """
        Start recording.

        Returns
        -------
        True for success, False otherwise.
        """
        raise NotImplementedError()

    def stop_recording() -> bool:
        """
        Stop recording.

        Returns
        -------
        True for success, False otherwise.
        """
        raise NotImplementedError()

