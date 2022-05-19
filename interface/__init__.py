"""
NextWheel Interface
===================
__init__.py: The main file.
"""

__author__ = "Félix Chénier"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"

from PyQt5 import QtWidgets
import gui as gui
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    NextWheel = QtWidgets.QDialog()
    ui = gui.Ui_NextWheel()
    ui.setupUi(NextWheel)
    NextWheel.show()
    sys.exit(app.exec_())
    ui = gui.Ui_NextWheel()
    ui.setupUi(NextWheel)
    NextWheel.show()
    sys.exit(app.exec_())
    sys.exit(app.exec_())
    sys.exit(app.exec_())
    sys.exit(app.exec_())
