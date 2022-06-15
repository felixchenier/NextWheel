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
    'graph_time': [0],
    'graph_force0': [0],
    'graph_force1': [0],
    'graph_force2': [0],
    'graph_force3': [0],
    'graph_moment0': [0],
    'graph_moment1': [0],
    'graph_moment2': [0],
    'graph_moment3': [0],
    'graph_velocity': [0, 0, 0],
    'graph_power': [0, 0, 0],
}


wheel = comm.Wheel(lists=lists)
wheel.connect()

ui = gui.Ui_NextWheel(lists=lists, wheel=wheel)
ui.run()
