#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NextWheel Interface
===================
client.py: Submodule that that connects with the instrumented wheels.
"""

__author__ = "Clémence Starosta"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"


import class_wheel as cw

connexion = True

wheel = cw.Wheel()
wheel.__init__()


connect = wheel.connection()
if connect is False:
    print("Server connection error")
else:
    print("Connected to the server")
    print("---------------------------------------------------")

client = wheel.client

connexion = True


while connexion is True:
    print("Welcome to the NextWheel interface")
    print("---------------------------------------------------")
    print("What do you want to do?")
    print("   -Start the streaming : tape 1")
    print("   -Stop the streaming:   tape 2")
    print("   -Start the recording:  tape 3")
    print("   -Stop the recording:   tape 4")
    print("   -Exit: tape stop")
    print("Your choice : ")
    option = input()

    if option == '1':
        client.sendall(bytes(option, encoding="utf-8"))
        print("What data do you want to analyse?")
        print("| 0  : Channel[0] |")
        print("| 1  : Channel[1] |")
        print("| 2  : Channel[2] |")
        print("| 3  : Channel[3] |")
        print("| 4  : Channel[4] |")
        print("| 5  : Channel[5] |")
        print("| 6  : Battery    |")
        print("| 7  : Forces[0]  |")
        print("| 8  : Forces[1]  |")
        print("| 9  : Forces[2]  |")
        print("| 10 : Forces[3]  |")
        print("| 11 : Moment[0]  |")
        print("| 12 : Forces[1]  |")
        print("| 13 : Forces[2]  |")
        print("| 14 : Forces[3]  |")
        print("---------------------------------------------------")
        choice = input()
        client.sendall(bytes(choice, encoding="utf-8"))
        print("")

    if option == '2':
        client.sendall(bytes(option, encoding="utf-8"))
        print("")

    if option == '3':
        client.sendall(bytes(option, encoding="utf-8"))
        print("What data do you want to analyse?")
        print("| 0  : Channel[0] |")
        print("| 1  : Channel[1] |")
        print("| 2  : Channel[2] |")
        print("| 3  : Channel[3] |")
        print("| 4  : Channel[4] |")
        print("| 5  : Channel[5] |")
        print("| 6  : Battery    |")
        print("| 7  : Forces[0]  |")
        print("| 8  : Forces[1]  |")
        print("| 9  : Forces[2]  |")
        print("| 10 : Forces[3]  |")
        print("| 11 : Moment[0]  |")
        print("| 12 : Forces[1]  |")
        print("| 13 : Forces[2]  |")
        print("| 14 : Forces[3]  |")
        print("---------------------------------------------------")
        choice = input()
        client.sendall(bytes(choice, encoding="utf-8"))
        print("")

    if option == '4':
        client.sendall(bytes(option, encoding="utf-8"))
        print("")

    elif option == "stop":
        client.sendall(bytes(option, encoding="utf-8"))
        disconnect = wheel.disconnect()
        if disconnect is False:
            print("Server disconnection error")
        else:
            print("Deconnected from the server")
            print("---------------------------------------------------")
        connexion = False
