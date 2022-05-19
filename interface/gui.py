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

from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import threading
import comm as co
import main as m


class Ui_NextWheel(object):
    def __init__(self):
        """
        Iniatialises flags

        """
        self.stream = False
        self.flag_stop = False

    def setupUi(self, NextWheel: object):
        """
        Iniatialises all widgets in the application

        """

        # main windows
        NextWheel.setObjectName("NextWheel")
        self.centralwidget = QtWidgets.QWidget(NextWheel)
        self.centralwidget.setObjectName("centralwidget")
        NextWheel.setWindowModality(QtCore.Qt.NonModal)
        NextWheel.setEnabled(True)
        NextWheel.resize(955, 599)
        NextWheel.setSizeGripEnabled(True)
        NextWheel.setModal(True)

        # Adding a layout to the main window to allow widgets to fit
        # in the window size
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(NextWheel)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_3 = QtWidgets.QLabel(NextWheel)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        spacerItem = QtWidgets.QSpacerItem(
            20, 30, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)

        # checkbox graph 1
        self.Battery1 = QtWidgets.QCheckBox(NextWheel)
        self.Battery1.setObjectName("Battery1")
        self.verticalLayout.addWidget(self.Battery1)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)

        self.Forces1 = QtWidgets.QCheckBox(NextWheel)
        self.Forces1.setObjectName("Forces1")
        self.verticalLayout.addWidget(self.Forces1)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem2)

        self.Moment1 = QtWidgets.QCheckBox(NextWheel)
        self.Moment1.setObjectName("Moment1")
        self.verticalLayout.addWidget(self.Moment1)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)

        self.channel01 = QtWidgets.QCheckBox(NextWheel)
        self.channel01.setObjectName("channel01")
        self.verticalLayout.addWidget(self.channel01)
        spacerItem4 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem4)

        self.channel11 = QtWidgets.QCheckBox(NextWheel)
        self.channel11.setObjectName("channel11")
        self.verticalLayout.addWidget(self.channel11)
        spacerItem5 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem5)

        self.chanel21 = QtWidgets.QCheckBox(NextWheel)
        self.chanel21.setObjectName("chanel21")
        self.verticalLayout.addWidget(self.chanel21)
        spacerItem6 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem6)

        self.channel31 = QtWidgets.QCheckBox(NextWheel)
        self.channel31.setObjectName("channel31")
        self.verticalLayout.addWidget(self.channel31)
        spacerItem7 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem7)

        self.channel41 = QtWidgets.QCheckBox(NextWheel)
        self.channel41.setObjectName("channel41")
        self.verticalLayout.addWidget(self.channel41)
        spacerItem8 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem8)

        self.channel51 = QtWidgets.QCheckBox(NextWheel)
        self.channel51.setObjectName("channel51")
        self.verticalLayout.addWidget(self.channel51)
        spacerItem9 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem9)

        # stremaing button
        self.pushButton_2 = QtWidgets.QPushButton(NextWheel)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        spacerItem10 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem10)
        self.pushButton_2.clicked.connect(self.etat_streaming)

        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(NextWheel)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        spacerItem11 = QtWidgets.QSpacerItem(
            20, 30, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem11)

        # checkbox graph 2
        self.battery2 = QtWidgets.QCheckBox(NextWheel)
        self.battery2.setObjectName("battery2")
        self.verticalLayout_2.addWidget(self.battery2)
        spacerItem12 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem12)

        self.forces2 = QtWidgets.QCheckBox(NextWheel)
        self.forces2.setObjectName("forces2")
        self.verticalLayout_2.addWidget(self.forces2)
        spacerItem13 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem13)

        self.moments2 = QtWidgets.QCheckBox(NextWheel)
        self.moments2.setObjectName("moments2")
        self.verticalLayout_2.addWidget(self.moments2)
        spacerItem14 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem14)

        self.channel02 = QtWidgets.QCheckBox(NextWheel)
        self.channel02.setObjectName("channel02")
        self.verticalLayout_2.addWidget(self.channel02)
        spacerItem15 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem15)

        self.channel12 = QtWidgets.QCheckBox(NextWheel)
        self.channel12.setObjectName("channel12")
        self.verticalLayout_2.addWidget(self.channel12)
        spacerItem16 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem16)

        self.channel22 = QtWidgets.QCheckBox(NextWheel)
        self.channel22.setObjectName("channel22")
        self.verticalLayout_2.addWidget(self.channel22)
        spacerItem17 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem17)

        self.channel32 = QtWidgets.QCheckBox(NextWheel)
        self.channel32.setObjectName("channel32")
        self.verticalLayout_2.addWidget(self.channel32)
        spacerItem18 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem18)

        self.channel42 = QtWidgets.QCheckBox(NextWheel)
        self.channel42.setObjectName("channel42")
        self.verticalLayout_2.addWidget(self.channel42)
        spacerItem19 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem19)

        self.channel52 = QtWidgets.QCheckBox(NextWheel)
        self.channel52.setObjectName("channel52")
        self.verticalLayout_2.addWidget(self.channel52)
        spacerItem20 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem20)

        # button stop streaming
        self.pushButton = QtWidgets.QPushButton(NextWheel)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        spacerItem21 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem21)
        self.pushButton.clicked.connect(self.end_streaming)

        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(NextWheel)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)

        # Graph one
        self.graph_one = pg.PlotWidget(NextWheel)
        self.graph_one.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.graph_one.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.graph_one.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.graph_one.setObjectName("graph_one")
        self.graph_one.setBackground('w')

        self.verticalLayout_4.addWidget(self.graph_one)
        self.doubleSpinBoxGrap1 = QtWidgets.QDoubleSpinBox(NextWheel)
        self.doubleSpinBoxGrap1.setObjectName("doubleSpinBox1")
        self.doubleSpinBoxGrap1.setMinimum(1)
        self.verticalLayout_4.addWidget(self.doubleSpinBoxGrap1)
        self.label = QtWidgets.QLabel(NextWheel)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)

        # graph two
        self.graph_two = pg.PlotWidget(NextWheel)
        self.graph_two.setObjectName("graph_two")
        self.verticalLayout_4.addWidget(self.graph_two)
        self.doubleSpinBox_2Grap_2 = QtWidgets.QDoubleSpinBox(NextWheel)
        self.doubleSpinBox_2Grap_2.setObjectName("doubleSpinBox")
        self.doubleSpinBox_2Grap_2.setMinimum(1)
        self.verticalLayout_4.addWidget(self.doubleSpinBox_2Grap_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.graph_two.setBackground('w')

        self.retranslateUi(NextWheel)
        QtCore.QMetaObject.connectSlotsByName(NextWheel)

    def retranslateUi(self, NextWheel: object):
        """
        Displaying text in the application

        """
        _translate = QtCore.QCoreApplication.translate
        NextWheel.setWindowTitle(_translate("NextWheel", "Next Wheel"))
        self.label_3.setText(_translate("NextWheel", "Graph 1"))
        self.Battery1.setText(_translate("NextWheel", "Battery"))
        self.Forces1.setText(_translate("NextWheel", "Forces"))
        self.Moment1.setText(_translate("NextWheel", "Moments"))
        self.channel01.setText(_translate("NextWheel", "Channel 0"))
        self.channel11.setText(_translate("NextWheel", "Channel 1"))
        self.chanel21.setText(_translate("NextWheel", "Channel 2"))
        self.channel31.setText(_translate("NextWheel", "Channel 3"))
        self.channel41.setText(_translate("NextWheel", "Channel 4"))
        self.channel51.setText(_translate("NextWheel", "Channel 5"))
        self.pushButton_2.setText(_translate("NextWheel", "Start streaming"))
        self.label_4.setText(_translate("NextWheel", "Graph 2"))
        self.battery2.setText(_translate("NextWheel", "Battery"))
        self.forces2.setText(_translate("NextWheel", "Forces"))
        self.moments2.setText(_translate("NextWheel", "Moments"))
        self.channel02.setText(_translate("NextWheel", "Channel 0"))
        self.channel12.setText(_translate("NextWheel", "Channel 1"))
        self.channel22.setText(_translate("NextWheel", "Channel 2"))
        self.channel32.setText(_translate("NextWheel", "Channel 3"))
        self.channel42.setText(_translate("NextWheel", "Channel 4"))
        self.channel52.setText(_translate("NextWheel", "Channel 5"))
        self.pushButton.setText(_translate("NextWheel", "Stop streaming"))
        self.label_2.setText(_translate("NextWheel", "Graph 1"))
        self.label.setText(_translate("NextWheel", "Graph 2"))

    def display_streaming(self):
        """
        Displaying graph with Data reception every 50 ms

        """

        if self.Battery1.isChecked():
            self.graph_one.plot(m.graph_time, m.graph_battery,
                                pen=pg.mkPen(color="r",))

        if self.battery2.isChecked():
            self.graph_two.plot(m.graph_time, m.graph_battery,
                                pen=pg.mkPen(color="r",))

        if self.Forces1.isChecked():
            self.graph_one.plot(m.graph_time, m.graph_force0,
                                name="Force[0]", pen=pg.mkPen(color="g",))
            self.graph_one.plot(m.graph_time, m.graph_force1,
                                name="Force[1]", pen=pg.mkPen(color="r",))
            self.graph_one.plot(m.graph_time, m.graph_force2,
                                name="Force[2]", pen=pg.mkPen(color="b",))
            self.graph_one.plot(m.graph_time, m.graph_force3,
                                name="Force[3]", pen=pg.mkPen(color="y",))

        if self.forces2.isChecked():
            self.graph_two.plot(m.graph_time, m.graph_force0,
                                name="Force[0]", pen=pg.mkPen(color="g",))
            self.graph_two.plot(m.graph_time, m.graph_force1,
                                name="Force[1]", pen=pg.mkPen(color="r",))
            self.graph_two.plot(m.graph_time, m.graph_force2,
                                name="Force[2]", pen=pg.mkPen(color="b",))
            self.graph_two.plot(m.graph_time, m.graph_force3,
                                name="Force[3]", pen=pg.mkPen(color="y",))

        if self.Moment1.isChecked():
            self.graph_one.plot(m.graph_time, m.graph_moment0,
                                name="Moment[0]", pen=pg.mkPen(color="g",))
            self.graph_one.plot(m.graph_time, m.graph_moment1,
                                name="Moment[1]", pen=pg.mkPen(color="r",))
            self.graph_one.plot(m.graph_time, m.graph_moment2,
                                name="Moment[2]", pen=pg.mkPen(color="b",))
            self.graph_one.plot(m.graph_time, m.graph_moment3,
                                name="Moment[3]", pen=pg.mkPen(color="y",))

        if self.moments2.isChecked():
            self.graph_two.plot(m.graph_time, m.graph_moment0,
                                name="Moment[0]", pen=pg.mkPen(color="g",))
            self.graph_two.plot(m.graph_time, m.graph_moment1,
                                name="Moment[1]", pen=pg.mkPen(color="r",))
            self.graph_two.plot(m.graph_time, m.graph_moment2,
                                name="Moment[2]", pen=pg.mkPen(color="b",))
            self.graph_two.plot(m.graph_time, m.graph_moment3,
                                name="Moment[3]", pen=pg.mkPen(color="y",))

        if self.channel01.isChecked():
            self.graph_one.plot(m.graph_time, m.graph_channel0,
                                pen=pg.mkPen(color="b",
                                             style=QtCore.Qt.DashLine))

        if self.channel02.isChecked():
            self.graph_two.plot(m.graph_time, m.graph_channel0,
                                pen=pg.mkPen(color="b",
                                             style=QtCore.Qt.DashLine))

        if self.channel11.isChecked():
            self.graph_one.plot(m.graph_time, m.graph_channel1,
                                pen=pg.mkPen(color="b",
                                             style=QtCore.Qt.DashLine))

        if self.channel12.isChecked():
            self.graph_two.plot(m.graph_time, m.graph_channel1,
                                pen=pg.mkPen(color="b",
                                             style=QtCore.Qt.DashLine))

        if self.chanel21.isChecked():
            self.graph_one.plot(m.graph_time, m.graph_channel2,
                                pen=pg.mkPen(color="b",
                                             style=QtCore.Qt.DashLine))

        if self.channel22.isChecked():
            self.graph_two.plot(m.graph_time, m.graph_channel2,
                                pen=pg.mkPen(color="b",
                                             style=QtCore.Qt.DashLine))

        if self.channel31.isChecked():
            self.graph_one.plot(m.graph_time, m.graph_channel3,
                                pen=pg.mkPen(color="b",
                                             style=QtCore.Qt.DashLine))

        if self.channel32.isChecked():
            self.graph_two.plot(m.graph_time, m.graph_channel3,
                                pen=pg.mkPen(color="b",
                                             style=QtCore.Qt.DashLine))

        if self.channel41.isChecked():
            self.graph_one.plot(m.graph_time, m.graph_channel4,
                                pen=pg.mkPen(color="b",
                                             style=QtCore.Qt.DashLine))

        if self.channel42.isChecked():
            self.graph_two.plot(m.graph_time, m.graph_channel4,
                                pen=pg.mkPen(color="b",
                                             style=QtCore.Qt.DashLine))

        if self.channel51.isChecked():
            self.graph_one.plot(m.graph_time, m.graph_channel5,
                                pen=pg.mkPen(color="b",
                                             style=QtCore.Qt.DashLine))

        if self.channel52.isChecked():
            self.graph_two.plot(m.graph_time, m.graph_channel5,
                                pen=pg.mkPen(color="b",
                                             style=QtCore.Qt.DashLine))

        self.graph_one.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBoxGrap1.value(),
                                 (m.graph_time[-1]), padding=0)

        self.graph_two.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBoxGrap1.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def etat_streaming(self):
        """
        Request to be in stream status

        """
        self.stream = True
        self.t_stream = threading.Thread(target=co.streaming)
        self.t_stream.start()

        # lauch of the timer
        self.timer1 = QtCore.QTimer()
        self.timer1.timeout.connect(self.display_streaming)
        self.timer1.start(50)

    def end_streaming(self):
        """
        Request to stop be in stream status

        """
        self.stream = False
        self.flag_stop = True
        self.t_end_stream = threading.Thread(target=co.end_streaming)
        self.t_end_stream.start()
        self.timer1.stop()
