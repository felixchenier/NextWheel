import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import limitedinteraction as li
from time import sleep

# from nextwheel import NextWheel


class wizard:
    def __init__(self):
        self.trials = {}
        self.nb_force_trial = 0
        self.step_number = 0
        self.progression = 0

        # Create root window

        self.root = tk.Tk()
        self.root.title("Welcome !")

        # set dimension of the window

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        height = 700
        width = 800
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
        self.top_frame.place(relx=0.5, rely=0.1, anchor="center")

        label = tk.Label(
            self.top_frame,
            text="Place the wheel like in the picture below",
            font=8,
        )
        label.pack()

        label2 = tk.Label(
            self.top_frame,
            text="Click on 'Measure' when ready",
            font=8,
        )
        label2.pack()

        self.botom_left_frame = tk.Frame(self.root)
        self.botom_left_frame.place(relx=0.1, rely=0.9, anchor="sw")

        back_button = tk.Button(
            self.botom_left_frame,
            font=8,
            text="Back",
            command=self.get_id_page,
        )
        back_button.pack()

        self.botom_frame = tk.Frame(self.root)
        self.botom_frame.place(relx=0.5, rely=0.9, anchor="s")

        self.measure_button = tk.Button(
            self.botom_frame,
            font=8,
            text="Measure",
            command=self.measure_data,
        )
        self.measure_button.pack()

        self.botom_right_frame = tk.Frame(self.root)
        self.botom_right_frame.place(relx=0.9, rely=0.9, anchor="se")

        self.next_button = tk.Button(
            self.botom_right_frame,
            font=8,
            text="Next",
            command=self.get_step2,
        )

        if self.progression >= self.step_number:
            self.next_button.pack()

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
        self.top_frame.place(relx=0.5, rely=0.1, anchor="center")

        label = tk.Label(
            self.top_frame,
            text="Adjust the wheel in a different angle (see picture below)",
            font=8,
        )
        label.pack()

        label2 = tk.Label(
            self.top_frame,
            text="Click on 'Measure' when ready",
            font=8,
        )
        label2.pack()

        self.botom_left_frame = tk.Frame(self.root)
        self.botom_left_frame.place(relx=0.1, rely=0.9, anchor="sw")

        back_button = tk.Button(
            self.botom_left_frame,
            font=8,
            text="Back",
            command=self.get_step1,
        )
        back_button.pack()

        self.botom_frame = tk.Frame(self.root)
        self.botom_frame.place(relx=0.5, rely=0.9, anchor="s")

        self.measure_button = tk.Button(
            self.botom_frame,
            font=8,
            text="Measure",
            command=self.measure_data,
        )
        self.measure_button.pack()

        self.botom_right_frame = tk.Frame(self.root)
        self.botom_right_frame.place(relx=0.9, rely=0.9, anchor="se")

        self.next_button = tk.Button(
            self.botom_right_frame,
            font=8,
            text="Next",
            command=self.get_step3,
        )

        if self.progression >= self.step_number:
            self.next_button.pack()

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
        self.top_frame.place(relx=0.5, rely=0.1, anchor="center")

        label = tk.Label(
            self.top_frame,
            text="Get rid of the mass and make the wheel spin",
            font=8,
        )
        label.pack()

        label2 = tk.Label(
            self.top_frame,
            text="Click on 'Measure' when ready",
            font=8,
        )
        label2.pack()

        self.botom_left_frame = tk.Frame(self.root)
        self.botom_left_frame.place(relx=0.1, rely=0.9, anchor="sw")

        back_button = tk.Button(
            self.botom_left_frame,
            font=8,
            text="Back",
            command=self.get_step2,
        )
        back_button.pack()

        self.botom_frame = tk.Frame(self.root)
        self.botom_frame.place(relx=0.5, rely=0.9, anchor="s")

        self.measure_button = tk.Button(
            self.botom_frame,
            font=8,
            text="Measure",
            command=self.measure_data,
        )
        self.measure_button.pack()

        self.botom_right_frame = tk.Frame(self.root)
        self.botom_right_frame.place(relx=0.9, rely=0.9, anchor="se")

        self.next_button = tk.Button(
            self.botom_right_frame,
            font=8,
            text="Next",
            command=self.get_step4,
        )

        if self.progression >= self.step_number:
            self.next_button.pack()

    def get_step4(self):
        print("ok")


w = wizard()
