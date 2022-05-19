"""
NextWheel Interface
===================
main.py: Control of the data from the wheel.
"""

import pickle
import comm as co

__author__ = "Clémence Starosta"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"


# List that will be used to display in the graph

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
    Receives data from the stream, places it in the corresponding lists
    Removes items from the list to avoid overloading the display
    """
    flag_stop = False
    # Listening on the right socket
    client = co.wheel.client_name()

    while flag_stop is False:

        # Reception of the frames
        buffer = client.recv(10000000)
        if (buffer != "stop"):
            trame = pickle.loads(buffer)

            for i in range(0, 300):
                data = dict(trame["data"][i])

                # Placement in the corresponding lists
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

            # Management of list length
            if (len(graph_time) > 6000):
                del graph_time[0:2000]
                del graph_battery[0:2000]
                del graph_force0[0:2000]
                del graph_force1[0:2000]
                del graph_force2[0:2000]
                del graph_force3[0:2000]
                del graph_moment0[0:2000]
                del graph_moment1[0:2000]
                del graph_moment2[0:2000]
                del graph_moment3[0:2000]
                del graph_channel0[0:2000]
                del graph_channel1[0:2000]
                del graph_channel2[0:2000]
                del graph_channel3[0:2000]
                del graph_channel4[0:2000]
                del graph_channel5[0:2000]
