"""
NextWheel Interface
===================
client.py: Submodule that that connects with the instrumented wheels.
"""

__author__ = "Clémence Starosta"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"

import sys
import comm as co

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Stream(QtWidgets.QMainWindow):
    def __init__(self, client_stream):
        """
       Initializes the class

        Returns
        -------
        None.
       """
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("Stream")
        self.setGeometry(100, 100, 200, 300)
        self.flag = True

        self.time_stream = QLabel(self)
        self.time_stream.setGeometry(50, 150, 100, 30)
        self.time_stream.setStyleSheet("border : 4px solid black;")
        self.time_stream.setText("0.00")
        self.time_stream.setFont(QFont('Arial', 15))
        self.time_stream.setAlignment(Qt.AlignCenter)

        self.data_stream = QLabel(self)
        self.data_stream.setGeometry(50, 100, 100, 30)
        self.data_stream.setStyleSheet("border : 4px solid black;")
        self.data_stream.setText("0.00")
        self.data_stream.setFont(QFont('Arial', 15))
        self.data_stream.setAlignment(Qt.AlignCenter)
        QtCore.QCoreApplication.processEvents()

        self.stop = QLabel(self)
        self.stop = QtWidgets.QPushButton("Stop Streaming", self)
        self.stop.setGeometry(50, 50, 100, 30)
        self.stop.clicked.connect(self.stop_streaming)

        self.show()

        self.streaming(client_stream)

    def streaming(self, client_stream):
        """
        Launch the strealing

        Returns
        -------
        None.

        """
        while self.flag is True:
            time = client_stream.recv(255).decode("utf-8")
            print(time)
            self.time_stream.setText(time)
            QtCore.QCoreApplication.processEvents()
            data = client_stream.recv(255).decode("utf-8")
            print(data)
            self.data_stream.setText(data)
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
       Initializes the class

       """
        self.wheel = co.Wheel()
        self.wheel.__init__()
        self.client = self.wheel.client
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("Next Wheel")
        self.setGeometry(450, 100, 500, 500)

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
        self.button_streaming.setGeometry(200, 100, 130, 30)
        self.data = QComboBox(self)
        data_list = ["Channel[0]", "Channel[1]", "Channel[2]", "Channel[3]",
                     "Channel[4]", "Channel[5]", "Battery", "Forces[0]",
                     "Forces[1]", "Forces[2]", "Forces[3]", " Moment[0]",
                     "Forces[1]", "Forces[2]", "Forces[3]"]
        self.data.addItems(data_list)
        self.data.setGeometry(30, 100, 150, 30)

        # recording
        self.button_recording = QtWidgets.QPushButton('Reccording', self)
        self.button_recording.clicked.connect(self.reccording)
        self.button_recording.setGeometry(200, 200, 130, 34)
        self.data1 = QComboBox(self)
        data_list1 = ["Channel[0]", "Channel[1]", "Channel[2]", "Channel[3]",
                      "Channel[4]", "Channel[5]", "Battery", "Forces[0]",
                      "Forces[1]", "Forces[2]", "Forces[3]", " Moment[0]",
                      "Forces[1]", "Forces[2]", "Forces[3]"]
        self.data1.addItems(data_list1)
        self.data1.setGeometry(30, 200, 150, 30)

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
        choice = self.data.currentText()
        self.client.send(bytes("1", encoding="utf-8"))
        self.client.sendall(bytes(choice, encoding="utf-8"))
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    choice = Choice()
    choice.show()
    sys.exit(app.exec_())
    sys.exit(app.exec_())
