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

path = r"C:/Users/Nicolas/Desktop/Test2/"
dat_filename = r"log_2000-12-31_19-02-12.dat"
csv_filename = r"sample_data.csv"


with open(f"{path}calibration.json", "r") as json_file:
    CALIBRATION = json.load(json_file)

A = np.array(CALIBRATION["Matrix"])
b = np.array(CALIBRATION["Offset"])

data = read_dat(f"{path}{dat_filename}")
time = data["Analog"]["Time"]
new_time = np.linspace(time[0], time[-1], len(time))

FMs = np.dot(A, data["Analog"]["Force"].T).T - b

wheel_angle_position = data["Encoder"]["Angle"] * encoder_variation
wheel_angle_position = np.interp(
    time, data["Encoder"]["Time"], wheel_angle_position
)

ts = ktk.TimeSeries()
ts.time = 1 * new_time
ts.data["WheelPosition"] = 1 * wheel_angle_position

ts2 = ktk.filters.savgol(ts, window_length=3, poly_order=2, deriv=1)

df = {
    "Time Force (s)": data["Analog"]["Time"],
    "Force X (N)": FMs[:, 0],
    "Force Y (N)": FMs[:, 1],
    "Force Z (N)": FMs[:, 2],
    "Moment X (Nm)": FMs[:, 3],
    "Moment Y (Nm)": FMs[:, 4],
    "Moment Z (Nm)": FMs[:, 5],
    "Orientation (deg)": wheel_angle_position - wheel_angle_position[0],
    "Displacement (m)": np.pi
    / 180
    * wheel_diameter
    / 2
    * (wheel_angle_position - wheel_angle_position[0]),
    "Angular Speed (deg/s)": ts2.data["WheelPosition"],
}

# speed_dict = {

# }

df = pd.DataFrame(df)
# speed_df = pd.DataFrame(speed_dict)

# df = pd.concat([force_df, speed_df], axis=1)


df.to_csv(f"{path}{csv_filename}", index=False)
