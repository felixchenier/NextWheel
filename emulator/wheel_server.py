'''
Author: Clémence Starosta
year : 2022
'''

#The server is the wheel

import time
import socket
import threading
import csv_function as csvf

file_data_wheel='kinetics_test.csv'

wheel_launch=time.time()
threads_clients = []

launch=True

def elapsed_time(wheel_launch):
   now=time.time()
   return now-wheel_launch

def instanceServeur (client, info_client, data_wheel):
    IP_address = info_client[0]
    port = str(info_client[1])
    print("Client connection: " + IP_address + ":" + port)
    server=True
    
    while server==True:
        client_choice=client.recv(255).decode("utf-8")
    
        if client_choice=="1":
            #data to be processed
            namedata=client.recv(255).decode("utf-8")
            time = client.recv(255).decode("utf-8") 
            #display of the received file
            print("Time received : " +  time)
            time=float(time)
            namedata=int(namedata)
            info=csvf.return_data_time(time,data_wheel,namedata+1)
            print("Send of ",info)
            info=str(info)
            client.sendall(bytes(info,encoding="utf-8"))
        
        elif client_choice=="stop":
            #closure of the connection
            print("Closed connection with " + IP_address + ":" + port)
            print("---------------------------------------------------")
            client.close()
            server=False

#socket creation
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Successful creation of the SERVER socket")

#extraction of the data wheel
print("Extraction of the data wheel")
data=csvf.open_add_data(file_data_wheel)
data_wheel=csvf.average_data(data, file_data_wheel)
print("Sucessful extraction")
print("---------------------------------------------------")

#listen for new client on port 5000
serveur.bind(('', 50000))
serveur.listen(5)
print("Listening to ongoing client connections")
print("---------------------------------------------------")

while launch==True:
    #we accept customers
	client, infosClient = serveur.accept()
    #launch of the thread
	threads_clients.append(threading.Thread(None, instanceServeur, None, (client, infosClient, data_wheel), {}))
	threads_clients[-1].start()

serveur.close()
    