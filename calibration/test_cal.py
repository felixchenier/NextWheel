# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 14:11:43 2024

@author: Nicolas
"""

import numpy as np
import matplotlib.pyplot as plt
import nextwheel
import wheelcalibration as wc
import limitedinteraction as li
import time
import os
import pickle
import csv

if __name__ == "__main__":
    nw = nextwheel.NextWheel("192.168.1.155")

    path = "C:/Users/Nicolas/Documents/NextWheel/calibration/"

    if not os.path.isfile(f"{path}DelsysRef.csv"):
        with open(
            f"{path}DelsysRef.csv",
            "w",
        ) as my_file:
            my_file.write("Trial, x, y, z")

    if not os.path.isfile(f"{path}Calibration.csv"):
        with open(
            f"{path}Calibration.csv",
            "w",
        ) as my_file:
            my_file.write(
                "Trial number, Acceleration x, Acceleration y, Acceleration z,"
            )
            my_file.write(
                "Channel 1, Channel 2, Channel 3, Channel 4, Channel 5, Channel 6,"
            )
            my_file.write("Mass, Degree")

# %% Partie 1 - Mesure du gyro pour l'axe z

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

    time.sleep(3)

    static_trial = nw.fetch()
    ##############################################################################
    static_trial["Mass"] = 0.0
    static_trial["Degree"] = 0.0

    n_trial = 0
    while os.path.isfile(f"Trials/StaticTrial{n_trial}.pkl"):
        n_trial += 1

    with open(f"{path}Trials/StaticTrial{n_trial}.pkl", "wb") as file:
        pickle.dump(static_trial, file)

    omega_static = static_trial["IMU"]["Gyro"]

    gyro_bias = wc.estimate_gyro_bias(omega_static)

    with open(f"{path}DelsysRef.csv", "a") as file:
        file.write("\nGyro Bias")
        for bias in gyro_bias:
            file.write(f",{bias}")

    li.message("")

    ########################## INTERFACE #########################################
    li.button_dialog(
        "Spin the wheel fast anticlockwise around the desired z-axis and click OK",
        choices=["OK"],
        title="z-axis calibration - Dynamic trial",
        icon="light",
    )

    li.message(
        "Please wait a few moments.", title="Measuring...", icon="clock"
    )
    ##############################################################################
    ########################## MEASURE ###########################################
    nw.fetch()

    time.sleep(3)

    dynamic_trial = nw.fetch()
    ##############################################################################
    n_trial = 0
    while os.path.isfile(f"Trials/DynamicTrial{n_trial}.pkl"):
        n_trial += 1

    with open(f"{path}Trials/DynamicTrial{n_trial}.pkl", "wb") as file:
        pickle.dump(dynamic_trial, file)

    omega_dynamic = dynamic_trial["IMU"]["Gyro"]

    z_axis = wc.get_z_axis_delsys_on_wheel(gyro_bias, omega_dynamic)

    with open(f"{path}DelsysRef.csv", "a") as file:
        file.write("\nZ-Axis")
        for z in z_axis:
            file.write(f",{z}")

    li.message("")

    nw.stop_streaming()

# %% Partie 2 - Mesure du plan xz and finalise the base_change_matrix

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

    time.sleep(3)

    static_trial_1 = nw.fetch()
    ##############################################################################
    static_trial_1["Mass"] = 0.0
    static_trial_1["Degree"] = 0.0

    n_trial = 0
    while os.path.isfile(f"Trials/XStaticTrial{n_trial}.pkl"):
        n_trial += 1

    with open(f"{path}Trials/XStaticTrial{n_trial}.pkl", "wb") as file:
        pickle.dump(static_trial_1, file)

    acc_static1 = -static_trial_1["IMU"]["Acc"]

    with open("{path}DelsysRef.csv", "a") as file:
        file.write("\nStatic Acceleration 1")
        for acc in np.median(acc_static1, axis=0):
            file.write(f",{acc}")

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
    nw.fetch()

    time.sleep(3)

    static_trial_2 = nw.fetch()
    ##############################################################################
    static_trial_2["Mass"] = 0.0
    static_trial_2["Degree"] = 0.0

    n_trial = 0
    while os.path.isfile(f"Trials/XStaticTrial{n_trial}.pkl"):
        n_trial += 1

    with open(f"{path}Trials/XStaticTrial{n_trial}.pkl", "wb") as file:
        pickle.dump(static_trial_2, file)

    acc_static2 = -static_trial_2["IMU"]["Acc"]

    with open("{path}DelsysRef.csv", "a") as file:
        file.write("\nStatic Acceleration 2")
        for acc in np.median(acc_static2, axis=0):
            file.write(f",{acc}")

    base = wc.get_delsys_reference(acc_static1, acc_static2, z_axis)

    li.message("")

    nw.stop_streaming()

# %% Partie 3 - More static trials for calibration matrix

if __name__ == "__main__":
    ########################## INTERFACE #########################################

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

    time.sleep(3)

    static_trial_3 = nw.fetch()
    ##############################################################################
    static_trial_3["Mass"] = mass
    static_trial_3["Degree"] = degree

    n_trial = 0
    while os.path.isfile(f"Trials/StaticTrial{n_trial}.pkl"):
        n_trial += 1

    with open(f"{path}Trials/StaticTrial{n_trial}.pkl", "wb") as file:
        pickle.dump(static_trial_3, file)

    li.message("")

    nw.stop_streaming()

# %% Partie 4 - Traitement pour matrice de calibration

Trials = {}
acc_statics = np.array([])
channels = np.array([])
for file_name in os.listdir(f"{path}Trials"):
    with open(f"{path}Trials/{file_name}", "rb") as file:
        Trials[file_name] = pickle.load(file)
        acc_statics = np.append(
            acc_statics, -np.median(Trials[file_name]["IMU"]["Acc"], axis=0)
        )
        channels = np.append(
            channels, np.median(Trials[file_name]["Analog"]["Force"], axis=0)
        )

acc_statics = np.reshape(acc_statics, (len(Trials), 3))
channels = np.transpose(np.reshape(channels, (len(Trials), 6)))

acc_bias = np.transpose(estimate_acc_bias(acc_statics)[0])

DelsysTrials = {}
with open(f"{path}DelsysRef.csv") as file:
    spamreader = csv.reader(file, delimiter=",")
    for row in spamreader:
        if row[0] == "Trial":
            pass
        else:
            row[1] = float(row[1])
            row[2] = float(row[2])
            row[3] = float(row[3])
            DelsysTrials[row[0]] = np.array(row[1:])

base = wc.get_delsys_reference(
    -Trials["XStaticTrial0.pkl"]["IMU"]["Acc"],
    -Trials["XStaticTrial1.pkl"]["IMU"]["Acc"],
    DelsysTrials["Z-Axis"],
)

FMs = np.array([])

Trials["StaticTrial0.pkl"]["Degree"] = 0.0
for trial in Trials:
    F, M = calculate_forces_moments(
        Trials[trial],
        acc_bias,
        base,
    )

    FM = np.append(F, M)

    FMs = np.append(FMs, FM, axis=0)


FMs = np.transpose(np.reshape(FMs, (len(Trials), 6)))

A = calculate_calibration_matrix(FMs, channels)
