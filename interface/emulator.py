"""
NextWheel Interface
===================
wheel_serveur.py: Emulator that simulates the operation of the wheel.
"""
import csv
import numpy as np
import threading
import socket
import comm as co
import sys
sys.path.append("C:/Users/moi/Documents/GitHub/NextWheel/interface")

sys.path.append("C:/Users/moi/Documents/GitHub/NextWheel/interface")
__author__ = "Clémence Starosta"
__copyright__ = "Laboratoire de recherche en mobilité et sport adapté"
__email__ = "clemence.starosta@etu.emse.fr"
__license__ = "Apache 2.0"

sys.path.append("C:/Users/moi/Documents/GitHub/NextWheel/interface")
"""
_______________________________________________________________________________
                                CSV Functions
_______________________________________________________________________________
"""


def csv_count_line(filename: any) -> int:
    """
    count line number in a csv file

    Parameters
    ----------
    filename : file with csv file

    Returns
    -------
    Return number of line
    """
    with open(filename, 'r') as f:
        i = 0
        for line in f:
            i += 1
    return i


def open_add_data(filename: any) -> float:
    """
    Open the csv file and put data into a tab

    Parameters
    ----------
    filename : file with csv file

    Returns
    -------
    Return tab of data
    """
    with open(filename, newline='') as csvfile:
        data_wheel1 = np.zeros((csv_count_line(filename), 16))
        read = csv.reader(csvfile, delimiter=',')
        data_wheel1 = list(read)
        data_wheel = list(np.float_(data_wheel1))
        for i in range(0, csv_count_line(file_data_wheel)):
            for j in range(0, 15):
                data_wheel[i][j] = round(data_wheel[i][j], 5)
    return data_wheel


"""
_______________________________________________________________________________
  Thread class (fr.acervolima.com/python-differentes-facons-de-tuer-un-fil/)
_______________________________________________________________________________
"""


class thread_with_trace(threading.Thread):
    """
    A class that helps manage threads

    Attributes
    ----------
    thread
    """

    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        """
        Launch of the thread
       """
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        """
        Create a thread trace
       """
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame: any, event: any, arg: any) -> any:
        """
        Find the local thread trace

        Parameters
        ----------
        frame, event, arg : parameter of the trace thread

        Returns
        -------
        Return the trace or None.
       """
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame: any, event: any, arg: any) -> any:
        """
        Stop execution of the local trace

        Parameters
        ----------
        frame, event, arg : parameter of the trace thread

        Returns
        -------
        Return the local trace
       """
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        """
        Killed the thread
       """
        self.killed = True


"""
_______________________________________________________________________________
                     Emulator which has the role of the server
_______________________________________________________________________________
"""


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
            t = thread_with_trace(target=wheel.start_streaming,
                                  args=(1, client, data_wheel))
            t.start()
            print("")

        elif client_choice == "2":
            wheel.stop_streaming(t)
            print("")

        elif client_choice == "3":
            choice = client.recv(255).decode("utf-8")
            choice = int(choice)
            t = thread_with_trace(target=wheel.start_recording,
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


def emulator_wheel():
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
    file_data_wheel = 'kinetics.csv'
    threads_clients = []

    wheel = co.Wheel()

    # extraction of the data wheel
    print("Extraction of the data wheel")
    data_wheel = open_add_data(file_data_wheel)
    # data_wheel = co.average_data(data, file_data_wheel)
    print("Sucessful extraction")
    print("---------------------------------------------------")

    # socket creation
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Successful creation of the wheel emulator")

    # listen for new client on port 5000
    serveur.bind(('', 50000))
    serveur.listen(5)
    print("Listening to ongoing client connections")
    print("---------------------------------------------------")
    emulator_wheel()
    serveur.bind(('', 50000))
    serveur.listen(5)
    print("Listening to ongoing client connections")
    print("---------------------------------------------------")
    emulator_wheel()
