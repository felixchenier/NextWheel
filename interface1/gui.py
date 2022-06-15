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
from PyQt5.QtGui import QFont


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
        NextWheel.setObjectName("NextWheel")
        NextWheel.setWindowModality(QtCore.Qt.NonModal)
        NextWheel.setEnabled(True)
        NextWheel.resize(1117, 565)

        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(":/logo/logo_labo.png"),
        # QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # NextWheel.setWindowIcon(icon)
        NextWheel.setStyleSheet("background-color: rgb(255, 255, 255);")
        NextWheel.setSizeGripEnabled(True)
        NextWheel.setModal(True)

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
        self.force0 = QtWidgets.QCheckBox(NextWheel)
        self.force0.setObjectName("force0")
        self.verticalLayout.addWidget(self.force0)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        self.verticalLayout.addItem(spacerItem1)
        self.force1 = QtWidgets.QCheckBox(NextWheel)
        self.force1.setObjectName("force1")
        self.verticalLayout.addWidget(self.force1)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        self.verticalLayout.addItem(spacerItem2)
        self.force2 = QtWidgets.QCheckBox(NextWheel)
        self.force2.setObjectName("force2")
        self.verticalLayout.addWidget(self.force2)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)

        self.verticalLayout.addItem(spacerItem3)
        self.force3 = QtWidgets.QCheckBox(NextWheel)
        self.force3.setObjectName("force3")
        self.verticalLayout.addWidget(self.force3)
        spacerItem4 = QtWidgets.QSpacerItem(
            20, 100, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)

        self.verticalLayout.addItem(spacerItem4)
        self.label_vitesse = QtWidgets.QLabel(NextWheel)
        self.label_vitesse.setObjectName("label_vitesse")
        self.verticalLayout.addWidget(self.label_vitesse)

        self.display_vitesse = QtWidgets.QLabel(NextWheel)
        self.display_vitesse.setObjectName("display_vitesse")
        self.verticalLayout.addWidget(self.display_vitesse)
        self.display_vitesse.setStyleSheet("border : 4px solid red;")

        spacerItem5 = QtWidgets.QSpacerItem(
            20, 60, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem5)

        self.pushButton_stream = QtWidgets.QPushButton(NextWheel)
        self.pushButton_stream.setStyleSheet(
            "background-color: rgb(255, 240, 237);")
        self.pushButton_stream.setObjectName("pushButton_stream")
        self.verticalLayout.addWidget(self.pushButton_stream)
        spacerItem6 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
        self.pushButton_stream.clicked.connect(self.etat_streaming)

        self.verticalLayout.addItem(spacerItem6)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(NextWheel)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        spacerItem7 = QtWidgets.QSpacerItem(
            20, 30, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)

        self.verticalLayout_2.addItem(spacerItem7)
        self.moment0 = QtWidgets.QCheckBox(NextWheel)
        self.moment0.setObjectName("moment0")
        self.verticalLayout_2.addWidget(self.moment0)
        spacerItem8 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(spacerItem8)
        self.moment1 = QtWidgets.QCheckBox(NextWheel)
        self.moment1.setObjectName("moment1")
        self.verticalLayout_2.addWidget(self.moment1)
        spacerItem9 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(spacerItem9)
        self.moment2 = QtWidgets.QCheckBox(NextWheel)
        self.moment2.setObjectName("moment2")
        self.verticalLayout_2.addWidget(self.moment2)
        spacerItem10 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)

        self.verticalLayout_2.addItem(spacerItem10)
        self.moment3 = QtWidgets.QCheckBox(NextWheel)
        self.moment3.setObjectName("moment3")
        self.verticalLayout_2.addWidget(self.moment3)
        spacerItem11 = QtWidgets.QSpacerItem(
            20, 100, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)

        self.verticalLayout_2.addItem(spacerItem11)
        self.label_puissance = QtWidgets.QLabel(NextWheel)
        self.label_puissance.setObjectName("label_puissance")
        self.verticalLayout_2.addWidget(self.label_puissance)

        self.display_puissance = QtWidgets.QLabel(NextWheel)
        self.display_puissance.setObjectName("display_puissance")
        self.verticalLayout_2.addWidget(self.display_puissance)
        self.display_puissance.setStyleSheet("border : 4px solid red;")

        spacerItem12 = QtWidgets.QSpacerItem(
            20, 60, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem12)
        self.Stop = QtWidgets.QPushButton(NextWheel)
        self.Stop.setObjectName("Stop")
        self.Stop.clicked.connect(self.stop_streaming)
        self.verticalLayout_2.addWidget(self.Stop)
        self.Stop.setStyleSheet(
            "background-color: rgb(255, 240, 237);")
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        spacerItem13 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem13)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(NextWheel)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)

        self.graph_one = pg.PlotWidget(NextWheel)
        self.graph_one.setObjectName("graph_one")
        self.verticalLayout_4.addWidget(self.graph_one)
        self.graph_one.setBackground('w')

        self.doubleSpinBox1 = QtWidgets.QDoubleSpinBox(NextWheel)
        self.doubleSpinBox1.setMinimum(2.0)
        self.doubleSpinBox1.setMaximum(5.0)
        self.doubleSpinBox1.setSingleStep(0.5)
        self.doubleSpinBox1.setObjectName("doubleSpinBox1")
        self.verticalLayout_4.addWidget(self.doubleSpinBox1)
        self.label = QtWidgets.QLabel(NextWheel)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)

        self.graph_two = pg.PlotWidget(NextWheel)
        self.graph_two.setObjectName("graph_two")
        self.verticalLayout_4.addWidget(self.graph_two)
        self.graph_two.setBackground('w')

        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(NextWheel)
        self.doubleSpinBox.setMinimum(2.0)
        self.doubleSpinBox.setMaximum(5.0)
        self.doubleSpinBox.setSingleStep(0.5)

        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.verticalLayout_4.addWidget(self.doubleSpinBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

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
        self.label_3.setText(_translate(
            "NextWheel",
            "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Smart</span></p></body></html>"))
        self.force0.setText(_translate("NextWheel", "Forces[0]"))
        self.force1.setText(_translate("NextWheel", "Forces[1]"))
        self.force2.setText(_translate("NextWheel", "Forces[2]"))
        self.force3.setText(_translate("NextWheel", "Forces[3]"))
        self.label_vitesse.setText(_translate(
            "NextWheel", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Vitesse</span></p></body></html>"))
        self.display_vitesse.setText(_translate(
            "NextWheel", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">0.0</span></p></body></html>"))
        self.pushButton_stream.setText(
            _translate("NextWheel", "Start streaming"))
        self.label_4.setText(_translate(
            "NextWheel", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">wheel</span></p></body></html>"))
        self.moment0.setText(_translate("NextWheel", "Moment[0]"))
        self.moment1.setText(_translate("NextWheel", "Moment[1]"))
        self.moment2.setText(_translate("NextWheel", "Moment[2]"))
        self.moment3.setText(_translate("NextWheel", "Moment[3]"))
        self.Stop.setText(_translate("NextWheel", "Stop"))
        self.label_puissance.setText(_translate(
            "NextWheel", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Puissance</span></p></body></html>"))
        self.display_puissance.setText(_translate(
            "NextWheel", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">0.0</span></p></body></html>"))
        self.label_2.setText(_translate(
            "NextWheel", "<html><head/><body><p><span style=\" font-weight:600;\">Forces</span></p></body></html>"))
        self.label.setText(_translate(
            "NextWheel", "<html><head/><body><p><span style=\" font-weight:600;\">Moments</span></p></body></html>"))

    def force0_checked(self):
        """Display force0 graph every 10 ms."""
        self.graph_one.plot(m.graph_time, m.graph_force0,
                            pen=pg.mkPen(color="r",))

        self.graph_one.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox1.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def force1_checked(self):
        """Display force1 graph every 10 ms."""
        self.graph_one.plot(m.graph_time, m.graph_force1,
                            pen=pg.mkPen(color="b",))

        self.graph_one.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox1.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def force2_checked(self):
        """Display force2 graph every 10 ms."""
        self.graph_one.plot(m.graph_time, m.graph_force2,
                            pen=pg.mkPen(color="g",))

        self.graph_one.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox1.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def force3_checked(self):
        """Display force3 graph every 10 ms."""
        self.graph_one.plot(m.graph_time, m.graph_force3,
                            pen=pg.mkPen(color="y",))

        self.graph_one.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox1.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def moment0_checked(self):
        """Display moment0 graph every 10 ms."""
        self.graph_two.plot(m.graph_time, m.graph_moment0,
                            pen=pg.mkPen(color="g",))

        self.graph_two.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def moment1_checked(self):
        """Display moment1 graph every 10 ms."""
        self.graph_two.plot(m.graph_time, m.graph_moment1,
                            pen=pg.mkPen(color="r",))

        self.graph_two.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def moment2_checked(self):
        """Display moment2 graph every 10 ms."""
        self.graph_two.plot(m.graph_time, m.graph_moment2,
                            name="Moment[1]", pen=pg.mkPen(color="b",))

        self.graph_two.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def moment3_checked(self):
        """Display moment2 graph every 10 ms."""
        self.graph_two.plot(m.graph_time, m.graph_moment3,
                            name="Moment[1]", pen=pg.mkPen(color="y",))

        self.graph_two.setXRange((m.graph_time[-1]) -
                                 self.doubleSpinBox.value(),
                                 (m.graph_time[-1]), padding=0)

        QtCore.QCoreApplication.processEvents()

    def display_velocity(self):
        """Display velocity every 10 ms."""
        vitesse = m.graph_velocity[len(m.graph_velocity)//2+1]
        self.display_vitesse.setText(str(round(vitesse*3.6*0.35, 2)))
        self.display_vitesse.setFont(QFont('Arial', 15))

        QtCore.QCoreApplication.processEvents()

    def display_power(self):
        """Display power every 10 ms."""
        self.display_puissance.setText(
            str(m.graph_power[len(m.graph_power)//2+1]))
        self.display_puissance.setFont(QFont('Arial', 15))

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

        self.timer_velocity = QtCore.QTimer()
        self.timer_velocity.timeout.connect(self.display_velocity)
        self.timer_velocity.start(c.timer_fresh)

        self.timer_power = QtCore.QTimer()
        self.timer_power.timeout.connect(self.display_power)
        self.timer_power.start(c.timer_fresh)

        if self.force0.isChecked():
            self.timer_force0 = QtCore.QTimer()
            self.timer_force0.timeout.connect(self.force0_checked)
            self.timer_force0.start(c.timer_fresh)

        if self.force1.isChecked():
            self.timer_force1 = QtCore.QTimer()
            self.timer_force1.timeout.connect(self.force1_checked)
            self.timer_force1.start(c.timer_fresh)

        if self.force2.isChecked():
            self.timer_force2 = QtCore.QTimer()
            self.timer_force2.timeout.connect(self.force2_checked)
            self.timer_force2.start(c.timer_fresh)

        if self.force3.isChecked():
            self.timer_force3 = QtCore.QTimer()
            self.timer_force3.timeout.connect(self.force3_checked)
            self.timer_force3.start(c.timer_fresh)

        if self.moment0.isChecked():
            self.timer_moment0 = QtCore.QTimer()
            self.timer_moment0.timeout.connect(self.moment0_checked)
            self.timer_moment0.start(c.timer_fresh)

        if self.moment1.isChecked():
            self.timer_moment1 = QtCore.QTimer()
            self.timer_moment1.timeout.connect(self.moment1_checked)
            self.timer_moment1.start(c.timer_fresh)

        if self.moment2.isChecked():
            self.timer_moment2 = QtCore.QTimer()
            self.timer_moment2.timeout.connect(self.moment2_checked)
            self.timer_moment2.start(c.timer_fresh)

        if self.moment3.isChecked():
            self.timer_moment3 = QtCore.QTimer()
            self.timer_moment3.timeout.connect(self.moment3_checked)
            self.timer_moment3.start(c.timer_fresh)

    def stop_streaming(self):
        """
        Request to stop stream status.

        Parameters
        ----------
        self.

        Returns
        -------
        None
        """

        self.timer_velocity.stop()
        self.display_vitesse.setText(
            str(m.graph_velocity[len(m.graph_velocity)//2+1]))
        self.display_vitesse.setFont(QFont('Arial', 15))

        self.timer_power.stop()
        self.display_puissance.setText(
            str(m.graph_power[len(m.graph_power)//2+1]))
        self.display_puissance.setFont(QFont('Arial', 15))

        if self.force0.isChecked():
            self.graph_one.plot(m.graph_time, m.graph_force0,
                                pen=pg.mkPen(color="r",))

            self.graph_one.setXRange((m.graph_time[-1]) -
                                     self.doubleSpinBox1.value(),
                                     (m.graph_time[-1]), padding=0)
            self.timer_force0.stop()

            QtCore.QCoreApplication.processEvents()

        if self.force1.isChecked():
            self.graph_one.plot(m.graph_time, m.graph_force1,
                                pen=pg.mkPen(color="b",))

            self.graph_one.setXRange((m.graph_time[-1]) -
                                     self.doubleSpinBox1.value(),
                                     (m.graph_time[-1]), padding=0)
            self.timer_force1.stop()
            QtCore.QCoreApplication.processEvents()

        if self.force2.isChecked():
            self.graph_one.plot(m.graph_time, m.graph_force2,
                                pen=pg.mkPen(color="g",))

            self.graph_one.setXRange((m.graph_time[-1]) -
                                     self.doubleSpinBox1.value(),
                                     (m.graph_time[-1]), padding=0)
            self.timer_force2.stop()
            QtCore.QCoreApplication.processEvents()

        if self.force3.isChecked():
            self.graph_one.plot(m.graph_time, m.graph_force3,
                                pen=pg.mkPen(color="y",))

            self.graph_one.setXRange((m.graph_time[-1]) -
                                     self.doubleSpinBox1.value(),
                                     (m.graph_time[-1]), padding=0)
            self.timer_force3.stop()
            QtCore.QCoreApplication.processEvents()

        if self.moment0.isChecked():
            self.graph_two.plot(m.graph_time, m.graph_moment0,
                                pen=pg.mkPen(color="g",))

            self.graph_two.setXRange((m.graph_time[-1]) -
                                     self.doubleSpinBox.value(),
                                     (m.graph_time[-1]), padding=0)
            self.timer_moment0.stop()
            QtCore.QCoreApplication.processEvents()

        if self.moment1.isChecked():
            self.graph_two.plot(m.graph_time, m.graph_moment1,
                                pen=pg.mkPen(color="r",))

            self.graph_two.setXRange((m.graph_time[-1]) -
                                     self.doubleSpinBox.value(),
                                     (m.graph_time[-1]), padding=0)
            self.timer_moment1.stop()
            QtCore.QCoreApplication.processEvents()

        if self.moment2.isChecked():
            self.graph_two.plot(m.graph_time, m.graph_moment2,
                                name="Moment[1]", pen=pg.mkPen(color="b",))

            self.graph_two.setXRange((m.graph_time[-1]) -
                                     self.doubleSpinBox.value(),
                                     (m.graph_time[-1]), padding=0)
            self.timer_moment2.stop()
            QtCore.QCoreApplication.processEvents()

        if self.moment3.isChecked():
            self.graph_two.plot(m.graph_time, m.graph_moment3,
                                name="Moment[1]", pen=pg.mkPen(color="y",))

            self.graph_two.setXRange((m.graph_time[-1]) -
                                     self.doubleSpinBox.value(),
                                     (m.graph_time[-1]), padding=0)
            self.timer_moment3.stop()
            QtCore.QCoreApplication.processEvents()


app = QtWidgets.QApplication(sys.argv)
NextWheel = QtWidgets.QDialog()
ui = Ui_NextWheel()
ui.setupUi(NextWheel)
NextWheel.show()
sys.exit(app.exec_())
