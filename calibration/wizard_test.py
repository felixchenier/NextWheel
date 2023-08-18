"""
The module is a python wizard that guide through the wheel calibration.

Form the trials dictionary and perform calculations of the calibration matrix.
In the end of the calibration, trials should look like below.

trials = {"StaticDelsysTrial1": dictionary extracted from the nextwheel module,
          "StaticDelsysTrial2": dictionary extracted from the nextwheel module,
          "DynamicTrial": dictionary extracted from the nextwheel module,
          "GravityTrial1": {dictionary extracted from the nextwheel module,
                            "Mass" : float (in kg),
                            "Angle": float (in degree),
                            "MassApplicationPosition": np.ndarray(1,3)}
          "GravityTrial2": {dictionary extracted from the nextwheel module,
                            "Mass" : float (in kg),
                            "Angle": float (in degree),
                            "MassApplicationPosition": np.ndarray(1,3)}
          etc.}

"""

import tkinter as tk
import limitedinteraction as li
from time import sleep
import wheelcalibration as wc

# from nextwheel import NextWheel


class wizard:
    def __init__(self):
        self.trials = {}

        self.nb_gravity_trial = 0
        self.step_number = 0
        self.progression = 0
        self.is_done = False

        # Create root window

        self.root = tk.Tk()
        self.root.title("Welcome !")

        # set dimension of the window

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = 800
        height = 700
        self.root.resizable(False, False)
        center_x = int((screen_width - width) / 2)
        center_y = int((screen_height - height) / 2)

        self.root.geometry(f"{width}x{height}+{center_x}+{center_y}")

        # create a center frame

        self.center_frame = tk.Frame(self.root)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create a button

        my_button = tk.Button(
            self.center_frame,
            text="Get started !",
            font=8,
            command=self.get_id_page,
        )
        my_button.pack()
        tk.mainloop()

    def clear(self):
        """
        Clear all widgets of the window.

        Returns
        -------
        None.

        """
        for widgets in self.root.winfo_children():
            widgets.destroy()

    def measure_data(self):
        """
        Measure the data with the NextWheel module.

        The measure is then place inside the dictionary trial under the key
        name trial_name. The measure is taken with the nw.fetch() method.

        Returns
        -------
        None.

        """
        li.message(
            "Please wait a few moments.", title="Measuring...", icon="clock"
        )
        sleep(3)

        # Nextwheel measurement here

        li.message("")

        if self.progression < self.step_number:
            self.progression += 1
            self.next_button.pack()
        elif self.progression == 4 and self.nb_gravity_trial > 5:
            self.is_done = True

        if self.step_number == 4:
            self.nb_gravity_trial += 1
            self.trials[
                self.trial_name
            ] = {}  # À enlever lorsque nextwheel va être inclu ?
            self.trials[self.trial_name]["Mass"] = float(self.mass_entry.get())
            self.trials[self.trial_name]["Angle"] = float(
                self.angle_entry.get()
            )

    def back_measure_next_button(
        self,
        back_command,
        measure_command,
        next_command,
    ):
        """
        Create and place the back, measure and next buttons on windows.

        Parameters
        ----------
        back_command : func
            Action of the back button.
        measure_command : func
            Action of the measure button.
        next_command : func
            Action of the next button.

        Returns
        -------
        None.

        """
        self.botom_left_frame = tk.Frame(self.root)
        self.botom_left_frame.place(relx=0.02, rely=0.98, anchor="sw")

        back_button = tk.Button(
            self.botom_left_frame,
            font=8,
            text="Back",
            command=back_command,
        )
        back_button.pack()

        self.botom_frame = tk.Frame(self.root)
        self.botom_frame.place(relx=0.5, rely=0.98, anchor="s")

        self.measure_button = tk.Button(
            self.botom_frame,
            font=8,
            text="Measure",
            command=measure_command,
        )
        self.measure_button.pack()

        self.botom_right_frame = tk.Frame(self.root)
        self.botom_right_frame.place(relx=0.98, rely=0.98, anchor="se")

        self.next_button = tk.Button(
            self.botom_right_frame,
            font=8,
            text="Next",
            command=next_command,
        )

        if self.progression >= self.step_number:
            self.next_button.pack()

    def get_id_page(self):
        """
        Page that ask the IP ADDRESS of the instrumented wheel.

        Returns
        -------
        None.

        """
        self.IP = ""
        self.clear()
        self.root.title("IP ADDRESS")

        # create center frame

        self.center_frame = tk.Frame(self.root)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # create and place label in center frame

        label = tk.Label(
            self.center_frame,
            text="Enter the ip address to connect the wheel",
            font=8,
        )
        label.pack()

        # create a entry for the adress ip with 192.168.1.254 by default

        self.ip_entry = tk.Entry(self.center_frame, borderwidth=5, font=8)
        self.ip_entry.pack()
        self.ip_entry.insert(0, "192.168.1.254")

        # create botom right frame

        self.botom_right_frame = tk.Frame(self.root)
        self.botom_right_frame.place(relx=0.9, rely=0.9, anchor="se")

        # create and place Next button that point to get_step1

        next_button = tk.Button(
            self.botom_right_frame,
            font=8,
            text="Next",
            command=self.get_step1,
        )
        next_button.pack()

    def get_step1(self):
        """
        Page that make the first measurement (StaticDelsys1).

        The first measurement is the wheel with a mass attach to the branch
        number one of the IMU.

        Returns
        -------
        None.

        """
        self.step_number = 1
        if self.IP == "":
            self.IP = self.ip_entry.get()

        self.clear()
        self.trial_name = "StaticDelsys1"

        self.root.title("Step 1 : First static measure")

        self.top_frame = tk.Frame(self.root)
        self.top_frame.place(relx=0.5, rely=0.05, anchor="center")

        label = tk.Label(
            self.top_frame,
            text="Place the wheel like in the picture below",
            font=8,
        )
        label.grid(column=0, row=0)
        # label.pack()

        label2 = tk.Label(
            self.top_frame,
            text="Click 'Measure' when ready and 'Next' when finish.",
            font=8,
        )
        label2.grid(column=0, row=1)
        # label2.pack()

        # insert image

        image = tk.PhotoImage(file="test.png")
        image_label = tk.Label(self.root, image=image)
        image_label.place(relx=0.5, rely=0.5, anchor="center")

        self.back_measure_next_button(
            self.get_id_page, self.measure_data, self.get_step2
        )

        tk.mainloop()

    def get_step2(self):
        """
        Page that make the second measurement (StaticDelsys2).

        Same as the first measurement, but with a different wheel orientation
        around the y axis.

        Returns
        -------
        None.

        """
        self.step_number = 2
        self.clear()
        self.trial_name = "StaticDelsys2"

        self.root.title("Step 2 : Second static measure")

        self.top_frame = tk.Frame(self.root)
        self.top_frame.place(relx=0.5, rely=0.05, anchor="center")

        label = tk.Label(
            self.top_frame,
            text="Adjust the wheel in a different angle (see picture below)",
            font=8,
        )
        label.pack()

        label2 = tk.Label(
            self.top_frame,
            text="Click 'Measure' when ready and 'Next' when finish.",
            font=8,
        )
        label2.pack()

        self.back_measure_next_button(
            self.get_step1, self.measure_data, self.get_step3
        )

    def get_step3(self):
        """
        Page that make the third measurement (DynamicDelsys).

        Without weight, the trial measure data when the wheel is spining.

        Returns
        -------
        None.

        """
        self.step_number = 3
        self.clear()
        self.trial_name = "DynamicDelsys"

        self.root.title("Step 3 : Dynamic measure")

        self.top_frame = tk.Frame(self.root)
        self.top_frame.place(relx=0.5, rely=0.05, anchor="center")

        label = tk.Label(
            self.top_frame,
            text="Get rid of the mass and make the wheel spin",
            font=8,
        )
        label.pack()

        label2 = tk.Label(
            self.top_frame,
            text="Click 'Measure' when ready and 'Next' when finish.",
            font=8,
        )
        label2.pack()

        self.back_measure_next_button(
            self.get_step2, self.measure_data, self.get_step4
        )

    def get_step4(
        self,
    ):  # Ajouter une étape avant qui explique comment placer la roue ?
        self.step_number = 4
        self.clear()
        self.trial_name = f"GravityTrial{self.nb_gravity_trial+1}"

        self.root.title("Step 4 : Gravity measure")

        self.top_frame = tk.Frame(self.root)
        self.top_frame.place(relx=0.5, rely=0.80, anchor="center")

        label_mass = tk.Label(
            self.top_frame,
            text="Enter the mass value",
            font=8,
        )
        label_mass.grid(column=0, row=0)

        mass_unity = tk.Label(
            self.top_frame,
            text="in kg",
            font=8,
        )
        mass_unity.grid(column=2, row=0)

        angle_unity = tk.Label(
            self.top_frame,
            text="in degree",
            font=8,
        )
        angle_unity.grid(column=2, row=1)

        label_angle = tk.Label(
            self.top_frame,
            text="Enter the angle position",
            font=8,
        )
        label_angle.grid(column=0, row=1)

        self.mass_entry = tk.Entry(self.top_frame, borderwidth=5, font=8)
        self.mass_entry.grid(column=1, row=0)

        self.angle_entry = tk.Entry(self.top_frame, borderwidth=5, font=8)
        self.angle_entry.grid(column=1, row=1)

        self.back_measure_next_button(
            self.get_step3, self.measure_data, self.get_step4
        )


w = wizard()
