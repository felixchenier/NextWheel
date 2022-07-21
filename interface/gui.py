"""
NextWheel Interface.

gui.py: A submodule that manages the gui as well as the graph displays.
"""

__author__ = "Clémence Starosta, Félix Chénier"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"


import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QLineEdit
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavTbar
from PyQt5 import QtCore
import threading

IP_adress = 'None'


class Ui_NextWheel(QtWidgets.QMainWindow):
    """Implements the interface related to the Next Wheel application."""

    def __init__(self, lists, wheel):
        super().__init__()
        self.setWindowTitle("Next Wheel interface")
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.lists = lists
        self.wheel = wheel
        self.layout = QtWidgets.QHBoxLayout(self._main)
        self.IP_adress = '0.0.0.0'

        layout_graph = QtWidgets.QVBoxLayout()

        layout_bouton = QtWidgets.QVBoxLayout()

        self.label_title = QtWidgets.QLabel()
        self.label_title.setText('Next Wheel interface')
        self.label_title.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        layout_bouton.addWidget(self.label_title)

        self.spacerItem = QtWidgets.QSpacerItem(
            20, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        layout_bouton.addItem(self.spacerItem)

        self.label_IP = QtWidgets.QLabel()
        self.label_IP.setText('Enter IP address')
        self.label_IP.setFont(QtGui.QFont("Times", 8))
        layout_bouton.addWidget(self.label_IP)

        self.IP_wheel = QLineEdit()
        layout_bouton.addWidget(self.IP_wheel)
        self.pushButton_ok = QtWidgets.QPushButton("OK")
        self.pushButton_ok.setObjectName("pushButton_ok")
        layout_bouton.addWidget(self.pushButton_ok)
        self.pushButton_ok.clicked.connect(self.ip_ok)

        self.spacerItem1 = QtWidgets.QSpacerItem(
            20, 150, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        layout_bouton.addItem(self.spacerItem1)

        # connection button
        self.pushButton_connect = QtWidgets.QPushButton("Connection")
        self.pushButton_connect.setObjectName("pushButton_connect")
        layout_bouton.addWidget(self.pushButton_connect)
        self.pushButton_connect.clicked.connect(self.connexion)

        # disconnection button
        self.pushButton_disconnect = QtWidgets.QPushButton("Disconnection")
        self.pushButton_disconnect.setObjectName("pushButton_disconnect")
        layout_bouton.addWidget(self.pushButton_disconnect)
        self.pushButton_disconnect.clicked.connect(self.deconnexion)

        self.label_connect = QtWidgets.QLabel()
        self.label_connect.setText('Waiting connexion... (Enter an IP adress)')
        self.label_connect.setFont(QtGui.QFont("Times", 8))
        layout_bouton.addWidget(self.label_connect)

        self.spacerItem3 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        layout_bouton.addItem(self.spacerItem3)

        # reccord button
        self.pushButton_reccord = QtWidgets.QPushButton("Reccord")
        self.pushButton_reccord.setObjectName("pushButton_reccord")
        layout_bouton.addWidget(self.pushButton_reccord)
        self.pushButton_reccord.clicked.connect(self.reccord)

        self.label_record = QtWidgets.QLabel()
        self.label_record.setText('No recording in progress')
        self.label_record.setFont(QtGui.QFont("Times", 8))
        layout_bouton.addWidget(self.label_record)

        # stop reccord button
        self.pushButton_stop_reccord = QtWidgets.QPushButton("Stop Reccord")
        self.pushButton_stop_reccord.setObjectName("pushButton_stop_reccord")
        layout_bouton.addWidget(self.pushButton_stop_reccord)
        self.pushButton_stop_reccord.clicked.connect(self.stop_reccord)

        self.spacerItem2 = QtWidgets.QSpacerItem(
            20, 150, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        layout_bouton.addItem(self.spacerItem2)

        # graph
        self.fig = plt.figure(figsize=(12, 6), facecolor='#DEDEDE')
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavTbar(self.canvas, self)
        layout_graph.addWidget(self.toolbar)
        layout_graph.addWidget(self.canvas)

        # adc graph
        self.adc_plot = plt.subplot(3, 1, 1)
        self.adc_plot.title.set_text('ADC')

        # imu graph
        self.imu_plot = plt.subplot(3, 1, 2)
        self.imu_plot.title.set_text('IMU')

        # power graph
        self.power_plot = plt.subplot(3, 1, 3)
        self.power_plot.title.set_text('Power')

        self.layout.addLayout(layout_bouton)
        self.layout.addLayout(layout_graph)

    def _update_(self):
        """
        Update of the graphs every 50 ms thanks to the timer_update.

        Parameters
        ----------
        self.

        Returns
        -------
        None
        """
        # Update of the events on the canvas
        self.fig.canvas.flush_events()

        self.adc_plot.cla()
        x_vals = [x[0] for x in self.lists["adc_values"]]
        y_vals = [x[1] for x in self.lists["adc_values"]]
        self.adc_plot.plot(x_vals, y_vals)
        self.adc_plot.title.set_text('ADC')

        self.imu_plot.cla()
        x_vals = [x[0] for x in self.lists["imu_values"]]
        y_vals = [x[1] for x in self.lists["imu_values"]]
        self.imu_plot.plot(x_vals, y_vals)
        self.imu_plot.title.set_text('IMU')

        self.power_plot.cla()
        x_vals = [x[0] for x in self.lists["power_values"]]
        y_vals = [x[1] for x in self.lists["power_values"]]
        self.power_plot.plot(x_vals, y_vals)
        self.power_plot.title.set_text('Power')

        # Display of graphs
        self.fig.canvas.draw()

        # Update events on the Qt
        QtCore.QCoreApplication.processEvents()

    def ip_ok(self):
        """
        Retrieve IP address.

        Parameters
        ----------
        self.

        Returns
        -------
        None
        """
        self.IP_adress = self.IP_wheel.text()
        self.label_connect.setText('Waiting connexion...')

    def connexion(self):
        """
        Connect to the Next Wheel electronic board.

        Parameters
        ----------
        self.

        Returns
        -------
        None
        """
        self.label_connect.setText('Connected to the Wheel')

        # connexion to the wheel
        self.stream = True
        self.thread_stream = threading.Thread(
            target=self.wheel.connect, args=(self.IP_adress,))
        self.thread_stream.start()

        # launch of the timer
        self.timer_update = QtCore.QTimer()
        self.timer_update.timeout.connect(self._update_)
        self.timer_update.start(50)

    def deconnexion(self):
        """
        Disconnect to the Next Wheel electronic board.

        Parameters
        ----------
        self.

        Returns
        -------
        None
        """
        self.label_connect.setText('Disconnected from the Wheel')

        # disconnexion to the wheel
        self.thread_disconnect = threading.Thread(target=self.wheel.disconnect)
        self.thread_disconnect.start()

    def reccord(self):
        """
        Launch the reccord on SD cards.

        Parameters
        ----------
        self.

        Returns
        -------
        None
        """
        self.label_record.setText('Recording in SD card...')

        self.thread_reccord = threading.Thread(target=self.wheel.reccord,
                                               args=(self.IP_adress,))
        self.thread_reccord.start()

    def stop_reccord(self):
        """
        Stop the reccord on SD cards.

        Parameters
        ----------
        self.

        Returns
        -------
        None
        """
        self.label_record.setText('No recording in progress')

        self.thread_stop_reccord = threading.Thread(
            target=self.wheel.stop_reccord, args=(self.IP_adress,))
        self.thread_stop_reccord.start()
