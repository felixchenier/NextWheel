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

if __name__ == "__main__":
    nw = nextwheel.NextWheel("192.168.1.155")

    Trials = {}
    n_trial = len(Trials)
    rim_mass = None

    if not os.path.isfile(
        "C:/Users/Nicolas/Documents/NextWheel/calibration/DelsysRef.csv"
    ):
        with open(
            "C:/Users/Nicolas/Documents/NextWheel/calibration/DelsysRef.csv",
            "w",
        ) as my_file:
            my_file.write("Trial, x, y, z")

    if not os.path.isfile(
        "C:/Users/Nicolas/Documents/NextWheel/calibration/DelsysRef.csv"
    ):
        with open(
            "C:/Users/Nicolas/Documents/NextWheel/calibration/Calibration.csv",
            "w",
        ) as my_file:
            my_file.write(
                "Trial number, Acceleration x, Acceleration y, Acceleration z, Mass, Degree"
            )

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

    omega_static = static_trial["IMU"]["Gyro"]

    gyro_bias = wc.estimate_gyro_bias(omega_static)

    with open(
        "C:/Users/Nicolas/Documents/NextWheel/calibration/DelsysRef.csv", "a"
    ) as file:
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

    omega_dynamic = dynamic_trial["IMU"]["Gyro"]

    z_axis = wc.get_z_axis_delsys_on_wheel(gyro_bias, omega_dynamic)

    with open(
        "C:/Users/Nicolas/Documents/NextWheel/calibration/DelsysRef.csv", "a"
    ) as file:
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

    acc_static1 = -static_trial_1["IMU"]["Acc"]

    with open(
        "C:/Users/Nicolas/Documents/NextWheel/calibration/DelsysRef.csv", "a"
    ) as file:
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

    acc_static2 = -static_trial_2["IMU"]["Acc"]

    with open(
        "C:/Users/Nicolas/Documents/NextWheel/calibration/DelsysRef.csv", "a"
    ) as file:
        file.write("\nStatic Acceleration 2")
        for acc in np.median(acc_static2, axis=0):
            file.write(f",{acc}")

    base = wc.get_delsys_reference(acc_static1, acc_static2, z_axis)

    li.message("")

    nw.stop_streaming()

# %% Test - Acc bias

if __name__ == "__main__":
    ########################## INTERFACE #########################################

    if rim_mass == None:
        rim_mass = li.input_dialog(
            "What is the mass of the rim? If not sure, put 0 in the box",
            icon="question",
        )
    mass = li.input_dialog("What is the mass you add on rim?", icon="question")
    degree = li.input_dialog("At witch degree on the rim?", icon="question")

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

    Trials[f"trial{n_trial}"]["Acc"] = np.median(
        static_trial_3["IMU"]["Acc"], axis=0
    )
    Trials[f"trial{n_trial}"]["Mass"] = mass
    Trials[f"trial{n_trial}"]["Degree"] = degree

    with open(
        "C:/User/Nicolas/Documents/NextWheel/calibration/Calibration.csv", "a"
    ) as file:
        file.write(f"\nStatic Acceleration {n_trial}")
        for acc in Trials[f"trial{n_trial}"]["Acc"]:
            file.write(f",{acc}")
        file.write(f",{mass}")
        file.write(f",{degree}")

    n_trial += 1

    li.message("")

    nw.stop_streaming()
