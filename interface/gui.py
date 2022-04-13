#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NextWheel Interface
===================
gui.py: A submodule that manages the gui, plots, etc.
"""

__author__ = "Clémence Starosta"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"

import comm as co
import json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore
from PyQt5.QtGui import QFont


class Stream(QtWidgets.QMainWindow):
    def __init__(self, client_stream):
        """
       Initializes the window corresponding to the stream

        Returns
        -------
        None.
       """
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("Streaming")
        self.setGeometry(50, 50, 900, 800)
        self.flag = True

        self.time_stream = QLabel(self)
        self.time_stream.setGeometry(90, 50, 100, 30)
        self.time_stream.setStyleSheet("border : 4px solid black;")
        self.time_stream.setText("0.00")
        self.time_stream.setFont(QFont('Arial', 15))
        self.label_time = QtWidgets.QLabel(self)
        self.label_time.move(20, 50)
        self.label_time.setText("Time: ")
        self.label_time_unity = QtWidgets.QLabel(self)
        self.label_time_unity.move(200, 50)
        self.label_time_unity.setText(" s ")

        self.data_channel0 = QLabel(self)
        self.data_channel0.setGeometry(90, 100, 100, 30)
        self.data_channel0.setStyleSheet("border : 4px solid red;")
        self.data_channel0.setText("0.00")
        self.data_channel0.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_channel0 = QtWidgets.QLabel(self)
        self.label_channel0.move(20, 100)
        self.label_channel0.setText("Channel 0 : ")

        self.data_channel1 = QLabel(self)
        self.data_channel1.setGeometry(90, 150, 100, 30)
        self.data_channel1.setStyleSheet("border : 4px solid red;")
        self.data_channel1.setText("0.00")
        self.data_channel1.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_channel1 = QtWidgets.QLabel(self)
        self.label_channel1.move(20, 150)
        self.label_channel1.setText("Channel 1 : ")

        self.data_channel2 = QLabel(self)
        self.data_channel2.setGeometry(90, 200, 100, 30)
        self.data_channel2.setStyleSheet("border : 4px solid red;")
        self.data_channel2.setText("0.00")
        self.data_channel2.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_channel2 = QtWidgets.QLabel(self)
        self.label_channel2.move(20, 200)
        self.label_channel2.setText("Channel 2 : ")

        self.data_channel3 = QLabel(self)
        self.data_channel3.setGeometry(90, 250, 100, 30)
        self.data_channel3.setStyleSheet("border : 4px solid red;")
        self.data_channel3.setText("0.00")
        self.data_channel3.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_channel3 = QtWidgets.QLabel(self)
        self.label_channel3.move(20, 250)
        self.label_channel3.setText("Channel 3 : ")

        self.data_channel4 = QLabel(self)
        self.data_channel4.setGeometry(90, 300, 100, 30)
        self.data_channel4.setStyleSheet("border : 4px solid red;")
        self.data_channel4.setText("0.00")
        self.data_channel4.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_channel4 = QtWidgets.QLabel(self)
        self.label_channel4.move(20, 300)
        self.label_channel4.setText("Channel 4 : ")

        self.data_channel5 = QLabel(self)
        self.data_channel5.setGeometry(90, 350, 100, 30)
        self.data_channel5.setStyleSheet("border : 4px solid red;")
        self.data_channel5.setText("0.00")
        self.data_channel5.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_channel5 = QtWidgets.QLabel(self)
        self.label_channel5.move(20, 350)
        self.label_channel5.setText("Channel 5 : ")

        self.data_force0 = QLabel(self)
        self.data_force0.setGeometry(310, 100, 100, 30)
        self.data_force0.setStyleSheet("border : 4px solid pink;")
        self.data_force0.setText("0.00")
        self.data_force0.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_force0 = QtWidgets.QLabel(self)
        self.label_force0.move(250, 100)
        self.label_force0.setText("Force[0] : ")

        self.data_force1 = QLabel(self)
        self.data_force1.setGeometry(310, 150, 100, 30)
        self.data_force1.setStyleSheet("border : 4px solid pink;")
        self.data_force1.setText("0.00")
        self.data_force1.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_force1 = QtWidgets.QLabel(self)
        self.label_force1.move(250, 150)
        self.label_force1.setText("Force[1] : ")

        self.data_force2 = QLabel(self)
        self.data_force2.setGeometry(310, 200, 100, 30)
        self.data_force2.setStyleSheet("border : 4px solid pink;")
        self.data_force2.setText("0.00")
        self.data_force2.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_force2 = QtWidgets.QLabel(self)
        self.label_force2.move(250, 200)
        self.label_force2.setText("Force[2] : ")

        self.data_force3 = QLabel(self)
        self.data_force3.setGeometry(310, 250, 100, 30)
        self.data_force3.setStyleSheet("border : 4px solid pink;")
        self.data_force3.setText("0.00")
        self.data_force3.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_force3 = QtWidgets.QLabel(self)
        self.label_force3.move(250, 250)
        self.label_force3.setText("Force[3] : ")

        self.data_battery = QLabel(self)
        self.data_battery.setGeometry(310, 350, 100, 30)
        self.data_battery.setStyleSheet("border : 4px solid black;")
        self.data_battery.setText("0.00")
        self.data_battery.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_battery = QtWidgets.QLabel(self)
        self.label_battery.move(250, 350)
        self.label_battery.setText("Battery : ")

        self.data_moment0 = QLabel(self)
        self.data_moment0.setGeometry(510, 100, 100, 30)
        self.data_moment0.setStyleSheet("border : 4px solid purple;")
        self.data_moment0.setText("0.00")
        self.data_moment0.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_moment0 = QtWidgets.QLabel(self)
        self.label_moment0.move(450, 100)
        self.label_moment0.setText("Moment[0] : ")

        self.data_moment1 = QLabel(self)
        self.data_moment1.setGeometry(510, 150, 100, 30)
        self.data_moment1.setStyleSheet("border : 4px solid purple;")
        self.data_moment1.setText("0.00")
        self.data_moment1.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_moment1 = QtWidgets.QLabel(self)
        self.label_moment1.move(450, 150)
        self.label_moment1.setText("Moment[1] : ")

        self.data_moment2 = QLabel(self)
        self.data_moment2.setGeometry(510, 200, 100, 30)
        self.data_moment2.setStyleSheet("border : 4px solid purple;")
        self.data_moment2.setText("0.00")
        self.data_moment2.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_moment2 = QtWidgets.QLabel(self)
        self.label_moment2.move(450, 200)
        self.label_moment2.setText("Moment[2] : ")

        self.data_moment3 = QLabel(self)
        self.data_moment3.setGeometry(510, 250, 100, 30)
        self.data_moment3.setStyleSheet("border : 4px solid purple;")
        self.data_moment3.setText("0.00")
        self.data_moment3.setFont(QFont('Arial', 15))
        QtCore.QCoreApplication.processEvents()
        self.label_moment3 = QtWidgets.QLabel(self)
        self.label_moment3.move(450, 250)
        self.label_moment3.setText("Moment[3] : ")

        self.stop = QLabel(self)
        self.stop = QtWidgets.QPushButton("Stop Streaming", self)
        self.stop.setGeometry(90, 5, 100, 30)
        self.stop.clicked.connect(self.stop_streaming)

        self.show()

        self.streaming(client_stream)

    def streaming(self, client_stream):
        """
        Launch the streaming in the window

        Returns
        -------
        None.

        """
        while self.flag is True:

            data = client_stream.recv(255).decode("utf-8")
            data_json = json.loads(data)
            self.time_stream.setText(str(data_json['time']))

            self.data_channel0.setText(str(data_json['channel'][0]))
            self.data_channel1.setText(str(data_json['channel'][1]))
            self.data_channel2.setText(str(data_json['channel'][2]))
            self.data_channel3.setText(str(data_json['channel'][3]))
            self.data_channel4.setText(str(data_json['channel'][4]))
            self.data_channel4.setText(str(data_json['channel'][5]))

            self.data_force0.setText(str(data_json['forces'][0]))
            self.data_force1.setText(str(data_json['forces'][1]))
            self.data_force2.setText(str(data_json['forces'][2]))
            self.data_force3.setText(str(data_json['forces'][3]))

            self.data_battery.setText(str(data_json['battery']))

            self.data_moment0.setText(str(data_json['moment'][0]))
            self.data_moment1.setText(str(data_json['moment'][1]))
            self.data_moment2.setText(str(data_json['moment'][2]))
            self.data_moment3.setText(str(data_json['moment'][3]))

            QtCore.QCoreApplication.processEvents()
        else:
            client_stream.send(bytes("2", encoding="utf-8"))

    def stop_streaming(self):
        """
        Stop the streaming

        Returns
        -------
        None.

        """

        self.flag = False


class Choice(QtWidgets.QMainWindow):
    def __init__(self):
        """
       Initializes main window

       """
        self.wheel = co.Wheel()
        self.wheel.__init__()
        self.client = self.wheel.client
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("Next Wheel")
        self.setGeometry(450, 100, 300, 300)

        # connexion à la roue
        self.button_connexion = QtWidgets.QPushButton(
            'Connexion à la roue', self)
        self.button_connexion.clicked.connect(self.connexion)
        self.button_connexion.setGeometry(30, 20, 130, 30)

        self.labelA = QtWidgets.QLabel(self)
        self.labelA.move(170, 20)

        # streaming
        self.button_streaming = QtWidgets.QPushButton('Streaming', self)
        self.button_streaming.clicked.connect(self.streaming)
        self.button_streaming.setGeometry(80, 100, 130, 30)

        # recording
        self.button_recording = QtWidgets.QPushButton('Reccording', self)
        self.button_recording.clicked.connect(self.reccording)
        self.button_recording.setGeometry(80, 200, 130, 34)

    def connexion(self):
        """
        Connexion to the wheel

        Returns
        -------
        None.

        """
        connect = self.wheel.connection()
        if connect is False:
            self.labelA.setText("Connected")
        else:
            self.labelA.setText("Connexion Error")

    def streaming(self):
        """
        Launch the streaming

        Returns
        -------
        None.

        """
        self.client.send(bytes("1", encoding="utf-8"))
        self.stream_window = Stream(self.client)
        self.stream_window.show()

    def reccording(self):
        """
        Lauch the recording

        Returns
        -------
        None.

        """
        raise NotImplementedError()
