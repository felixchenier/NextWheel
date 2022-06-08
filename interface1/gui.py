"""
NextWheel Interface.

gui.py: A submodule that manages the gui as well as the graph displays.
"""

__author__ = "Clémence Starosta"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"

from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import threading
import comm as co
import _init_ as m
import sys
import constant as c
import time


class Ui_NextWheel(object):
    """Implements the interface related to the Next Wheel application."""

    def __init__(self):
        """
        Iniatialises flags.

        Parameters
        ----------
        stream: flag. Streaming flag.
        flag_stop: flag. End streaming flag.

        Returns
        -------
        None
        """
        self.stream = False
        self.flag_stop = False

    def setupUi(self, NextWheel: object):
        """
        Iniatialises all widgets in the application.

        Parameters
        ----------
        NextWheel: object. Object that represents the gui.

        Returns
        -------
        None
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
        self.battery1 = QtWidgets.QCheckBox(NextWheel)
        self.battery1.setObjectName("Battery1")
        self.verticalLayout.addWidget(self.battery1)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)

        self.forces1 = QtWidgets.QCheckBox(NextWheel)
        self.forces1.setObjectName("Forces1")
        self.verticalLayout.addWidget(self.forces1)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem2)

        self.moment1 = QtWidgets.QCheckBox(NextWheel)
        self.moment1.setObjectName("Moment1")
        self.verticalLayout.addWidget(self.moment1)
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

        # graph one
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
        self.doubleSpinBoxGrap1.setMinimum(1.5)
        # self.doubleSpinBoxGrap1.setMaximum(2)
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
        self.doubleSpinBox_2Grap_2.setMinimum(1.5)
        # self.doubleSpinBox_2Grap_2.setMaximun(2)
        self.verticalLayout_4.addWidget(self.doubleSpinBox_2Grap_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.graph_two.setBackground('w')

        self.retranslateUi(NextWheel)
        QtCore.QMetaObject.connectSlotsByName(NextWheel)

    def retranslateUi(self, NextWheel: object):
        """
        Display text in the application.

        Parameters
        ----------
        NextWheel: object. Object that represents the gui.

        Returns
        -------
        None
        """
        _translate = QtCore.QCoreApplication.translate
        NextWheel.setWindowTitle(_translate("NextWheel", "Next Wheel"))
        self.label_3.setText(_translate("NextWheel", "Graph 1"))
        self.battery1.setText(_translate("NextWheel", "Battery"))
        self.forces1.setText(_translate("NextWheel", "Forces"))
        self.moment1.setText(_translate("NextWheel", "Moments"))
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

    def baterry1_checked(self):
        """Display battery graph 1 every 10 ms."""
        self.graph_one.plot(m.graph_time, m.graph_battery,
                            pen=pg.mkPen(color="r",))

        self.graph_one.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBoxGrap1.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def baterry2_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_two.plot(m.graph_time, m.graph_battery,
                            pen=pg.mkPen(color="r",))

        self.graph_two.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox_2Grap_2.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def forces1_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_one.plot(m.graph_time, m.graph_force0,
                            name="Force[0]", pen=pg.mkPen(color="g",))
        self.graph_one.plot(m.graph_time, m.graph_force1,
                            name="Force[1]", pen=pg.mkPen(color="r",))
        self.graph_one.plot(m.graph_time, m.graph_force2,
                            name="Force[2]", pen=pg.mkPen(color="b",))
        self.graph_one.plot(m.graph_time, m.graph_force3,
                            name="Force[3]", pen=pg.mkPen(color="y",))

        self.graph_one.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox_2Grap_2.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def forces2_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_two.plot(m.graph_time, m.graph_force0,
                            name="Force[0]", pen=pg.mkPen(color="g",))
        self.graph_two.plot(m.graph_time, m.graph_force1,
                            name="Force[1]", pen=pg.mkPen(color="r",))
        self.graph_two.plot(m.graph_time, m.graph_force2,
                            name="Force[2]", pen=pg.mkPen(color="b",))
        self.graph_two.plot(m.graph_time, m.graph_force3,
                            name="Force[3]", pen=pg.mkPen(color="y",))

        self.graph_two.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox_2Grap_2.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def moment1_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_one.plot(m.graph_time, m.graph_moment0,
                            name="Moment[0]", pen=pg.mkPen(color="g",))
        self.graph_one.plot(m.graph_time, m.graph_moment1,
                            name="Moment[1]", pen=pg.mkPen(color="r",))
        self.graph_one.plot(m.graph_time, m.graph_moment2,
                            name="Moment[2]", pen=pg.mkPen(color="b",))
        self.graph_one.plot(m.graph_time, m.graph_moment3,
                            name="Moment[3]", pen=pg.mkPen(color="y",))

        self.graph_one.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBoxGrap1.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def moment2_checked(self):
        """Display battery graph 1  every 10 ms."""
        tic = time.perf_counter()
        self.graph_two.plot(m.graph_time, m.graph_moment0,
                            name="Moment[0]", pen=pg.mkPen(color="g",))
        self.graph_two.plot(m.graph_time, m.graph_moment1,
                            name="Moment[1]", pen=pg.mkPen(color="r",))
        self.graph_two.plot(m.graph_time, m.graph_moment2,
                            name="Moment[2]", pen=pg.mkPen(color="b",))
        self.graph_two.plot(m.graph_time, m.graph_moment3,
                            name="Moment[3]", pen=pg.mkPen(color="y",))

        self.graph_two.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox_2Grap_2.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()
        toc = time.perf_counter()
        print(toc-tic)

    def channel01_checked(self):
        """Display battery graph 1  every 10 ms."""
        # tic = time.perf_counter()
        self.graph_one.plot(m.graph_time, m.graph_channel0,
                            pen=pg.mkPen(color="b",
                                         style=QtCore.Qt.DashLine))

        self.graph_one.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBoxGrap1.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()
        # toc = time.perf_counter()
        # print(toc-tic)

    def channel02_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_two.plot(m.graph_time, m.graph_channel0,
                            pen=pg.mkPen(color="b",
                                         style=QtCore.Qt.DashLine))

        self.graph_two.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox_2Grap_2.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def channel11_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_one.plot(m.graph_time, m.graph_channel1,
                            pen=pg.mkPen(color="b",
                                         style=QtCore.Qt.DashLine))

        self.graph_one.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBoxGrap1.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def channel12_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_two.plot(m.graph_time, m.graph_channel1,
                            pen=pg.mkPen(color="b",
                                         style=QtCore.Qt.DashLine))

        self.graph_two.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox_2Grap_2.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def channel21_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_one.plot(m.graph_time, m.graph_channel2,
                            pen=pg.mkPen(color="b",
                                         style=QtCore.Qt.DashLine))

        self.graph_one.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBoxGrap1.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def channel22_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_two.plot(m.graph_time, m.graph_channel2,
                            pen=pg.mkPen(color="b",
                                         style=QtCore.Qt.DashLine))

        self.graph_two.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox_2Grap_2.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def channel31_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_one.plot(m.graph_time, m.graph_channel3,
                            pen=pg.mkPen(color="b",
                                         style=QtCore.Qt.DashLine))

        self.graph_one.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBoxGrap1.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def channel32_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_two.plot(m.graph_time, m.graph_channel3,
                            pen=pg.mkPen(color="b",
                                         style=QtCore.Qt.DashLine))

        self.graph_two.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox_2Grap_2.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def channel41_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_one.plot(m.graph_time, m.graph_channel4,
                            pen=pg.mkPen(color="b",
                                         style=QtCore.Qt.DashLine))

        self.graph_one.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBoxGrap1.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def channel42_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_two.plot(m.graph_time, m.graph_channel4,
                            pen=pg.mkPen(color="b",
                                         style=QtCore.Qt.DashLine))

        self.graph_two.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox_2Grap_2.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def channel51_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_one.plot(m.graph_time, m.graph_channel5,
                            pen=pg.mkPen(color="b",
                                         style=QtCore.Qt.DashLine))

        self.graph_one.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBoxGrap1.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def channel52_checked(self):
        """Display battery graph 1  every 10 ms."""
        self.graph_two.plot(m.graph_time, m.graph_channel5,
                            pen=pg.mkPen(color="b",
                                         style=QtCore.Qt.DashLine))

        self.graph_two.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox_2Grap_2.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def etat_streaming(self):
        """
        Request to be in stream status.

        Parameters
        ----------
        self.

        Returns
        -------
        None
        """
        # launch of the thread that sends the desired state to comm.py
        self.stream = True
        self.thread_stream = threading.Thread(target=co.streaming)
        self.thread_stream.start()

        if self.battery1.isChecked():
            self.timer_battery1 = QtCore.QTimer()
            self.timer_battery1.timeout.connect(self.baterry1_checked)
            self.timer_battery1.start(c.timer_fresh)

        if self.battery2.isChecked():
            self.timer_battery2 = QtCore.QTimer()
            self.timer_battery2.timeout.connect(self.baterry2_checked)
            self.timer_battery2.start(c.timer_fresh)

        if self.forces1.isChecked():
            self.timer_forces1 = QtCore.QTimer()
            self.timer_forces1.timeout.connect(self.forces1_checked)
            self.timer_forces1.start(c.timer_fresh)

        if self.forces2.isChecked():
            self.timer_forces2 = QtCore.QTimer()
            self.timer_forces2.timeout.connect(self.forces2_checked)
            self.timer_forces2.start(c.timer_fresh)

        if self.moment1.isChecked():
            self.timer_moment1 = QtCore.QTimer()
            self.timer_moment1.timeout.connect(self.moment1_checked)
            self.timer_moment1.start(c.timer_fresh)

        if self.moments2.isChecked():
            self.timer_moment2 = QtCore.QTimer()
            self.timer_moment2.timeout.connect(self.moment2_checked)
            self.timer_moment2.start(c.timer_fresh)

        if self.channel01.isChecked():
            self.timer_channel01 = QtCore.QTimer()
            self.timer_channel01.timeout.connect(self.channel01_checked)
            self.timer_channel01.start(c.timer_fresh)

        if self.channel02.isChecked():
            self.timer_channel02 = QtCore.QTimer()
            self.timer_channel02.timeout.connect(self.channel02_checked)
            self.timer_channel02.start(c.timer_fresh)

        if self.channel11.isChecked():
            self.timer_channel11 = QtCore.QTimer()
            self.timer_channel11.timeout.connect(self.channel11_checked)
            self.timer_channel11.start(c.timer_fresh)

        if self.channel12.isChecked():
            self.timer_channel12 = QtCore.QTimer()
            self.timer_channel12.timeout.connect(self.channel12_checked)
            self.timer_channel12.start(c.timer_fresh)

        if self.chanel21.isChecked():
            self.timer_channel21 = QtCore.QTimer()
            self.timer_channel21.timeout.connect(self.channel21_checked)
            self.timer_channel21.start(c.timer_fresh)

        if self.channel22.isChecked():
            self.timer_channel22 = QtCore.QTimer()
            self.timer_channel22.timeout.connect(self.channel22_checked)
            self.timer_channel22.start(c.timer_fresh)

        if self.channel31.isChecked():
            self.timer_channel31 = QtCore.QTimer()
            self.timer_channel31.timeout.connect(self.channel31_checked)
            self.timer_channel31.start(c.timer_fresh)

        if self.channel32.isChecked():
            self.timer_channel32 = QtCore.QTimer()
            self.timer_channel32.timeout.connect(self.channel32_checked)
            self.timer_channel32.start(c.timer_fresh)

        if self.channel41.isChecked():
            self.timer_channel41 = QtCore.QTimer()
            self.timer_channel41.timeout.connect(self.channel41_checked)
            self.timer_channel41.start(c.timer_fresh)

        if self.channel42.isChecked():
            self.timer_channel42 = QtCore.QTimer()
            self.timer_channel42.timeout.connect(self.channel42_checked)
            self.timer_channel42.start(c.timer_fresh)

        if self.channel51.isChecked():
            self.timer_channel51 = QtCore.QTimer()
            self.timer_channel51.timeout.connect(self.channel51_checked)
            self.timer_channel51.start(c.timer_fresh)

        if self.channel52.isChecked():
            self.timer_channel52 = QtCore.QTimer()
            self.timer_channel52.timeout.connect(self.channel52_checked)
            self.timer_channel52.start(c.timer_fresh)

    def end_streaming(self):
        """
        Request tostop to be in stream status.

        Parameters
        ----------
        self.

        Returns
        -------
        None
        """
        # end of the stream
        self.stream = False
        self.flag_stop = True

        # launch of the thread that sends the desired state to comm.py
        self.thread_end_stream = threading.Thread(target=co.end_streaming)
        self.thread_end_stream.start()


app = QtWidgets.QApplication(sys.argv)
NextWheel = QtWidgets.QDialog()
ui = Ui_NextWheel()
ui.setupUi(NextWheel)
NextWheel.show()
sys.exit(app.exec_())
