"""
NextWheel Interface.

_init_.py: Management of received data in the corresponding lists.
"""


__author__ = "Clémence Starosta, Félix Chénier"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"


import gui
import comm


# Lists used to enable display in gui.py
lists = {
    'adc_values': [],
    'imu_values': [],
    'power_values': [],
}

wheel = comm.Wheel(lists=lists)
ui = gui.Ui_NextWheel(lists=lists, wheel=wheel)
ui.show()
ui.activateWindow()
ui.raise_()
