# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:51:52 2024

@author: Nicolas
"""

import kineticstoolkit as ktk
from nextwheel import read_dat
import pandas as pd
import numpy as np
import json

encoder_variation = 0.087890625  # degree by click
wheel_diameter = 0.6096  # m

path = r"C:\Users\MOSA\Desktop\Pilot test2\L-path\OG\Right"
dat_filename = "log_2000-12-31_19-02-34.dat"
csv_filename = "L-path-2nd_right.csv"


with open(f"{path}/calibration.json", "r") as json_file:
    CALIBRATION = json.load(json_file)

A = np.array(CALIBRATION["Matrix"])
b = np.array(CALIBRATION["Offset"])

data = read_dat(f"{path}/{dat_filename}")
FMs = np.dot(A, data["Analog"]["Force"].T).T - b

wheel_angle_position = data["Encoder"]["Angle"] * encoder_variation

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


df.to_csv(f"{path}\{csv_filename}", index=False)
