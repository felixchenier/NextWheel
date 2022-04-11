#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NextWheel Interface
===================
wheel_serveur.py: Submodule that communicates with the instrumented wheels.
"""

__author__ = "Clémence Starosta"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"

import socket
import threading
import comm as co

file_data_wheel = 'kinetics.csv'
threads_clients = []

wheel = co.Wheel()
wheel.__init__()


# extraction of the data wheel
print("Extraction of the data wheel")
data = co.open_add_data(file_data_wheel)
data_wheel = co.average_data(data, file_data_wheel)
print("Sucessful extraction")
print("---------------------------------------------------")

# socket creation
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Successful creation of the SERVER socket")

# listen for new client on port 5000
serveur.bind(('', 50000))
serveur.listen(5)
print("Listening to ongoing client connections")
print("---------------------------------------------------")


def instanceServeur(client: any, info_client: any, data_wheel: any):
    """
    Manages the client thread

   Parameters
   ----------
   client, info_client: socket and socket's information
   data_wheel: tab with wheel data


   """
    IP_address = info_client[0]
    port = str(info_client[1])
    print("Client connection: " + IP_address + ":" + port)
    server = True

    while server is True:
        client_choice = client.recv(255).decode("utf-8")

        if client_choice == "1":
            t = co.thread_with_trace(target=wheel.start_streaming,
                                     args=(1, client))
            t.start()
            print("")

        elif client_choice == "2":
            wheel.stop_streaming(t)
            print("")

        elif client_choice == "3":
            choice = client.recv(255).decode("utf-8")
            choice = int(choice)
            t = co.thread_with_trace(target=wheel.start_recording,
                                     args=(choice,))
            t.start()
            print("")

        elif client_choice == "4":
            wheel.stop_recording(t)
            print("")

        elif client_choice == "stop":
            print("Closed connection with " + IP_address + ":" + port)
            print("---------------------------------------------------")
            client.close()
            server = False


def main():
    """
    Main function.
    This function initializes the communication with the wheel(s), the gui,
    runs the event loop, etc.
    This is a work in progress.
    """
    while True:
        # we accept customers
        client, infosClient = serveur.accept()
        # launch of the thread
        threads_clients.append(threading.Thread(None, instanceServeur, None,
                                                (client, infosClient,
                                                 data_wheel), {}))
        threads_clients[-1].start()
    serveur.close()


if __name__ == "__main__":
    main()
