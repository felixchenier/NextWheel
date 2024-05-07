# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 14:11:43 2024

@author: Nicolas
"""

import numpy as np
import matplotlib.pyplot as plt
import kineticstoolkit as ktk
import nextwheel
import wheelcalibration as wc
import limitedinteraction as li
import time
import os

if __name__ == "__main__":
    nw = nextwheel.NextWheel("192.168.1.155")

    path = "C:/Users/Nicolas/Documents/NextWheel/calibration/"
    trials_dir = "Trials/"

# %% Part 1 - Z-axis calculated from gyroscope

if __name__ == "__main__":
    ########################## INTERFACE #########################################
    li.button_dialog(
        "Make sure the wheel is not moving and click Ok",
        choices=["OK"],
        title="z-axis calibration - Static trial",
        icon="light",
    )

    li.message(
        "Please wait a few moments.", title="Measuring...", icon="clock"
    )
    ##############################################################################
    ########################## MEASURE ###########################################
    nw.start_streaming()

    nw.fetch()

    time.sleep(5)

    static_trial = nw.fetch()
    nw.stop_streaming()
    ##############################################################################

    n_trial = 0
    while os.path.isfile(f"{path}{trials_dir}GyroBiasMeasure{n_trial}"):
        n_trial += 1
    ktk.save(f"{path}{trials_dir}GyroBiasMeasure{n_trial}", static_trial)

    omega_static = static_trial["IMU"]["Gyro"]

    gyro_bias = wc.estimate_gyro_bias(omega_static)  # gyro bias calculation

    li.message("")

    ########################## INTERFACE #########################################
    li.button_dialog(
        "Spin the wheel anticlockwise around the desired z-axis and click OK",
        choices=["OK"],
        title="z-axis calibration - Dynamic trial",
        icon="light",
    )

    li.message(
        "Please wait a few moments.", title="Measuring...", icon="clock"
    )
    ##############################################################################
    ########################## MEASURE ###########################################
    nw.start_streaming()
    nw.fetch()

    time.sleep(5)

    dynamic_trial = nw.fetch()
    nw.stop_streaming()
    ##############################################################################

    while os.path.isfile(f"{path}{trials_dir}GyroMeasureForZAxis{n_trial}"):
        n_trial += 1
    ktk.save(f"{path}{trials_dir}GyroMeasureForZAxis{n_trial}", dynamic_trial)

    omega_dynamic = dynamic_trial["IMU"]["Gyro"]

    z_axis = wc.get_z_axis(gyro_bias, omega_dynamic)  # z-axis calculation

    li.message("")

# %% Part 2 - XZ-Plane determined from acc + base change matrix completion

if __name__ == "__main__":
    ########################## INTERFACE #########################################
    li.button_dialog(
        "Make sure the wheel is not moving and that the x-axis point to the lower part",
        choices=["OK"],
        title="xz-axis calibration - Static trial 1",
        icon="light",
    )

    li.message(
        "Please wait a few moments.", title="Measuring...", icon="clock"
    )
    ##############################################################################
    ########################## MEASURE ###########################################
    nw.start_streaming()
    nw.fetch()

    time.sleep(5)

    static_trial_1 = nw.fetch()
    nw.stop_streaming()
    ##############################################################################

    n_trial = 0
    while os.path.isfile(f"{path}{trials_dir}AccGravMeasure{n_trial}"):
        n_trial += 1

    ktk.save(f"{path}{trials_dir}AccGravMeasure{n_trial}", static_trial_1)

    acc_static1 = -static_trial_1["IMU"]["Acc"]

    li.message("")

    ########################## INTERFACE #########################################
    li.button_dialog(
        "Same indication that before, but with an other orientation around y-axis",
        choices=["OK"],
        title="z-axis calibration - Static trial 2",
        icon="light",
    )

    li.message(
        "Please wait a few moments.", title="Measuring...", icon="clock"
    )
    ##############################################################################
    ########################## MEASURE ###########################################
    nw.start_streaming()
    nw.fetch()

    time.sleep(5)

    static_trial_2 = nw.fetch()
    nw.stop_streaming()
    ##############################################################################

    n_trial = 0
    while os.path.isfile(f"{path}{trials_dir}AccGravMeasure{n_trial}"):
        n_trial += 1
    ktk.save(f"{path}{trials_dir}AccGravMeasure{n_trial}", static_trial_2)

    acc_static2 = -static_trial_2["IMU"]["Acc"]

    base = wc.get_delsys_reference(
        acc_static1, acc_static2, z_axis
    )  # base change calculation

    li.message("")

# %% Part 3 - More static Force mesures for calibration matrix

if __name__ == "__main__":
    ########################## INTERFACE #########################################
    li.button_dialog(
        "Measure the offset of the channel",
        choices=["OK"],
        title="Offset",
        icon="light",
    )

    li.message(
        "Please wait a few moments.", title="Measuring...", icon="clock"
    )
    ##############################################################################
    ########################## MEASURE ###########################################
    nw.start_streaming()
    nw.fetch()

    time.sleep(5)

    offset_trial = nw.fetch()
    nw.stop_streaming()
    ##############################################################################

    offset = np.mean(offset_trial["Analog"]["Force"], axis=0)

    mass = float(
        li.input_dialog("What is the mass you add on rim?", icon="question")
    )
    degree = float(
        li.input_dialog("At witch degree on the rim?", icon="question")
    )

    li.button_dialog(
        "Measure the gravity and forces on rim",
        choices=["OK"],
        title="Calibration - Matrix",
        icon="light",
    )

    li.message(
        "Please wait a few moments.", title="Measuring...", icon="clock"
    )
    ##############################################################################
    ########################## MEASURE ###########################################
    nw.start_streaming()
    nw.fetch()

    time.sleep(5)

    static_trial_3 = nw.fetch()
    nw.stop_streaming()
    ##############################################################################
    static_trial_3["Mass"] = mass
    static_trial_3["Degree"] = degree

    static_trial_3["Analog"]["Force"] -= np.tile(
        offset, (np.shape(static_trial_3["Analog"]["Force"])[0], 1)
    )

    n_trial = 0
    while os.path.isfile(f"{path}{trials_dir}ForcesMomentsMeasure{n_trial}"):
        n_trial += 1

    ktk.save(
        f"{path}{trials_dir}ForcesMomentsMeasure{n_trial}", static_trial_3
    )

    li.message("")

# %% Part 4 - Calibration matrix calculation

Trials = {}
grav_measures = np.ndarray((1, 3))
forces_channels = np.ndarray((1, 6))
count = 0

for file_name in os.listdir(f"{path}{trials_dir}"):
    if file_name.startswith("Forces"):
        Trials[file_name] = ktk.load(f"{path}{trials_dir}{file_name}")
        grav = -np.mean(Trials[file_name]["IMU"]["Acc"], axis=0)
        grav_measures = np.vstack(
            (
                grav_measures,
                grav,
            )
        )

        forces = np.mean(Trials[file_name]["Analog"]["Force"], axis=0)
        forces_channels = np.vstack(
            (
                forces_channels,
                forces,
            )
        )

    if file_name.startswith("GyroBias"):
        Trials[file_name] = ktk.load(f"{path}{trials_dir}{file_name}")

        Trials["GyroBias"] = np.mean(Trials[file_name]["IMU"]["Gyro"], axis=0)

    if file_name.startswith("GyroMeasure"):
        Trials[file_name] = ktk.load(f"{path}{trials_dir}{file_name}")

    if file_name.startswith("AccGrav"):
        Trials[file_name] = ktk.load(f"{path}{trials_dir}{file_name}")
        count += 1

Trials["Z-Axis"] = np.array(
    [-0.0007454810123062489, 0.0009531282008410795, -0.9999992679020785]
)
# Trials["Z-Axis"] = wc.get_z_axis(
#     Trials["GyroBias"], Trials["GyroMeasureForZAxis"]["IMU"]["Gyro"]
# ) # uncomment if the trial GyroMeasureForZAxis exist

Trials["AccBias"] = wc.estimate_acc_bias(
    grav_measures
)  # estimate accelerometer bias

Trials["Base"] = wc.get_wheel_reference(
    -Trials[f"AccGravMeasure{count-2}"]["IMU"]["Acc"],
    -Trials[f"AccGravMeasure{count-1}"]["IMU"]["Acc"],
    Trials["Z-Axis"],
)  # estimate the base change matrix

FMs = np.ndarray((1, 6))
for trial in Trials:
    if trial.startswith("Forces"):
        F, M = wc.make_an_estimation_of_forces_moments(
            Trials[trial],
            Trials["AccBias"],
            Trials["Base"],
        )

        FM = np.hstack((F, M))
        FMs = np.vstack((FMs, FM))

A = wc.calculate_calibration_matrix(
    FMs.T, forces_channels.T
)  # estimate the calibration matrix in A*forces_channels.T = FMs.T
