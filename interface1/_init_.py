"""
NextWheel Interface.

_init_.py: Management of received data in the corresponding lists.
"""


import comm as co
import json
import constant as c

__author__ = "Clémence Starosta"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"


# Lists used to enable display in gui.py

graph_time = [0]
graph_battery = [0]
graph_force0 = [0]
graph_force1 = [0]
graph_force2 = [0]
graph_force3 = [0]
graph_moment0 = [0]
graph_moment1 = [0]
graph_moment2 = [0]
graph_moment3 = [0]
graph_channel0 = [0]
graph_channel1 = [0]
graph_channel2 = [0]
graph_channel3 = [0]
graph_channel4 = [0]
graph_channel5 = [0]


def receive_streaming():
    """
    Receives data from the stream, places it in the corresponding lists.

    Removes items from the list to avoid overloading the display.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    flag_stop = False

    # Connecting main.py to the right socket
    client = co.wheel.client_name()

    while flag_stop is False:

        # Reception of the frames
        buffer = client.recv(c.LENGTH_BUFFER)
        trame = json.loads(buffer.decode())

        for i_receiving in range(0, c.nbr_JSON_per_framme):
            data = dict(trame["data"][i_receiving])

            # Put data in the corresponding lists
            graph_time.append(data['time'])
            graph_battery.append(data['battery'])
            graph_force0.append(data['forces'][0])
            graph_force1.append(data['forces'][1])
            graph_force2.append(data['forces'][2])
            graph_force3.append(data['forces'][3])
            graph_moment0.append(data['moment'][0])
            graph_moment1.append(data['moment'][1])
            graph_moment2.append(data['moment'][2])
            graph_moment3.append(data['moment'][3])
            graph_channel0.append(data['channel'][0])
            graph_channel1.append(data['channel'][1])
            graph_channel2.append(data['channel'][2])
            graph_channel3.append(data['channel'][3])
            graph_channel4.append(data['channel'][4])
            graph_channel5.append(data['channel'][5])

            # lists length management
        if (len(graph_time) > 3*int(c.nbr_JSON_per_second)):
            del graph_time[0:int(c.nbr_JSON_per_second)]
            del graph_battery[0:int(c.nbr_JSON_per_second)]
            del graph_force0[0:int(c.nbr_JSON_per_second)]
            del graph_force1[0:int(c.nbr_JSON_per_second)]
            del graph_force2[0:int(c.nbr_JSON_per_second)]
            del graph_force3[0:int(c.nbr_JSON_per_second)]
            del graph_moment0[0:int(c.nbr_JSON_per_second)]
            del graph_moment1[0:int(c.nbr_JSON_per_second)]
            del graph_moment2[0:int(c.nbr_JSON_per_second)]
            del graph_moment3[0:int(c.nbr_JSON_per_second)]
            del graph_channel0[0:int(c.nbr_JSON_per_second)]
            del graph_channel1[0:int(c.nbr_JSON_per_second)]
            del graph_channel2[0:int(c.nbr_JSON_per_second)]
            del graph_channel3[0:int(c.nbr_JSON_per_second)]
            del graph_channel4[0:int(c.nbr_JSON_per_second)]
            del graph_channel5[0:int(c.nbr_JSON_per_second)]
