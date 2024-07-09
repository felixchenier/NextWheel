# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:51:52 2024

@author: Nicolas
"""

import kineticstoolkit as ktk
from nextwheel import read_dat
import pandas as pd
import numpy as np
import nextwheel
import matplotlib.pyplot as plt

Left_IP = "192.168.0.130"
Right_IP = "192.168.0.86"
encoder_variation = 0.08789255623292504  # degree by click
wheel_diameter = 0.6096  # m

dat_filename = "log_2000-12-31_19-00-32.dat"
csv_filename = "4th_floor_Right_data.csv"

if __name__ == "__main__":
    nw = nextwheel.NextWheel(Right_IP)
    A = nw.CALIBRATION_MATRIX
    b = nw.CALIBRATION_OFFSET
    nw.file_download(dat_filename)


data = read_dat(dat_filename)
FMs = np.dot(A, data["Analog"]["Force"].T).T - b
# FMs = data["Analog"]["Force"]

wheel_angle_position = data["Encoder"]["Angle"] * encoder_variation
# wheel_angle_position = data["Encoder"]["Angle"]

ts = ktk.TimeSeries()
ts.time = data["Encoder"]["Time"]
ts.data["WheelPosition"] = wheel_angle_position

ts = ts.resample(round(np.mean(1 / (ts.time[1:] - ts.time[:-1]))))

ts2 = ktk.filters.savgol(ts, window_length=3, poly_order=2, deriv=1)

force_dict = {
    "Time Force (s)": data["Analog"]["Time"],
    "Force X (N)": FMs[:, 0],
    "Force Y (N)": FMs[:, 1],
    "Force Z (N)": FMs[:, 2],
    "Moment X (Nm)": FMs[:, 3],
    "Moment Y (Nm)": FMs[:, 4],
    "Moment Z (Nm)": FMs[:, 5],
}

speed_dict = {
    "Time Speed (s)": data["Encoder"]["Time"],
    "Orientation (deg)": wheel_angle_position - wheel_angle_position[0],
    "Displacement (m)": np.pi
    / 180
    * wheel_diameter
    / 2
    * (wheel_angle_position - wheel_angle_position[0]),
    "Angular Speed (deg/s)": np.append(0, ts2.data["WheelPosition"]),
}

force_df = pd.DataFrame(force_dict)
speed_df = pd.DataFrame(speed_dict)

df = pd.concat([force_df, speed_df], axis=1)


df.to_csv(csv_filename, index=False)
