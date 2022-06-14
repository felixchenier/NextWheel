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
graph_force0 = [0]
graph_force1 = [0]
graph_force2 = [0]
graph_force3 = [0]
graph_moment0 = [0]
graph_moment1 = [0]
graph_moment2 = [0]
graph_moment3 = [0]
graph_velocity = [0, 0, 0]
graph_power = [0, 0, 0]


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
    # Connecting main.py to the right socket
    client = co.wheel.client_name()

    while co.wheel.flag_stream is True:
        # Reception of the frames
        buffer = client.recv(c.LENGTH_BUFFER)
        if (buffer.decode() != "stop"):
            trame = json.loads(buffer.decode())

            for i_receiving in range(0, c.nbr_JSON_per_framme):
                data = dict(trame["data"][i_receiving])

                # Put data in the corresponding lists
                graph_time.append(data['time'])
                graph_force0.append(data['Forces'][0])
                graph_force1.append(data['Forces'][1])
                graph_force2.append(data['Forces'][2])
                graph_force3.append(data['Forces'][3])
                graph_moment0.append(data['Moments'][0])
                graph_moment1.append(data['Moments'][1])
                graph_moment2.append(data['Moments'][2])
                graph_moment3.append(data['Moments'][3])
                graph_velocity.append(round(data['Velocity'], 2))
                graph_power.append(round(data["Power"], 2))

                # lists length management
                if (len(graph_time) > 3*int(c.nbr_JSON_per_second)):
                    del graph_time[0:int(c.nbr_JSON_per_second)]
                    del graph_force0[0:int(c.nbr_JSON_per_second)]
                    del graph_force1[0:int(c.nbr_JSON_per_second)]
                    del graph_force2[0:int(c.nbr_JSON_per_second)]
                    del graph_force3[0:int(c.nbr_JSON_per_second)]
                    del graph_moment0[0:int(c.nbr_JSON_per_second)]
                    del graph_moment1[0:int(c.nbr_JSON_per_second)]
                    del graph_moment2[0:int(c.nbr_JSON_per_second)]
                    del graph_moment3[0:int(c.nbr_JSON_per_second)]
                    del graph_velocity[0:int(c.nbr_JSON_per_second)]
                    del graph_power[0:int(c.nbr_JSON_per_second)]
        else:
            print("end")
