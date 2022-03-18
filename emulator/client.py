'''
Author: Clémence Starosta
year : 2022
'''

import socket

IP_address = "localhost"
port = 50000 #same port as the server
connexion=True

'''
__________________________________________________________________________
                            CONNEXION
__________________________________________________________________________'''

#socket creation
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Successful creation of the CLIENT socket')

#server connection
client.connect((IP_address, port))
print("Connected to the server")
print("---------------------------------------------------")

'''
__________________________________________________________________________
                            FUNCTIONS
__________________________________________________________________________'''

def switch_data_for_time():
    '''Gives for a given time the channel, the battery, the forces or moments'''
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
    choice=input()
    print("At what time? ( in ms)")
    time=input()
    
    client.sendall(bytes(choice,encoding="utf-8"))
    client.sendall(bytes(time,encoding="utf-8"))
    answer = client.recv(255)
    
    if choice == "0": 
        print('Channel 0: ' ,answer.decode("utf-8"))  
    elif choice == "1": 
        print('Channel 1: ' ,answer.decode("utf-8"))  
    elif choice == "2": 
        print('Channel 2: ' ,answer.decode("utf-8"))   
    elif choice == "3": 
        print('Channel 3: ' ,answer.decode("utf-8"))    
    elif choice == "4": 
        print('Channel 4: ' ,answer.decode("utf-8"))    
    elif choice == "5": 
        print('Channel 5: ' ,answer.decode("utf-8")) 
    elif choice == "6": 
        print('Battery: ' ,answer.decode("utf-8"), " V") 
    elif choice == "7": 
        print('Force 0: ' ,answer.decode("utf-8"), " N") 
    elif choice == "8": 
        print('Force 1: ' ,answer.decode("utf-8"), " N")       
    elif choice == "9": 
        print('Force 2: ' ,answer.decode("utf-8"), " N") 
    elif choice == "10": 
        print('Force 3: ' ,answer.decode("utf-8"),  " N") 
    elif choice == "11": 
        print('Moment 0: ' ,answer.decode("utf-8"), " Nm")        
    elif choice == "12": 
        print('Moment 1: ' ,answer.decode("utf-8"), " Nm")        
    elif choice == "13": 
        print('Moment 2: ' ,answer.decode("utf-8"), " Nm")        
    elif choice == "14": 
        print('Moment 3: ' , answer.decode("utf-8"))         
    else: 
        print("Error")
        
'''
__________________________________________________________________________
                            MAIN PROGRAM
__________________________________________________________________________'''

connexion=True
while connexion==True:
    print("Welcome to the NextWheel interface")
    print("---------------------------------------------------")
    print("What do you want to do?")
    print("   -The channel, the battery, the strength, the moment corresponds to a specific time (in ms) : tape 1")
    print("   -Exit: tape stop")
    print("Your choice : ")
    option=input()
    
    if option=='1':
        client.sendall(bytes(option,encoding="utf-8"))
        switch_data_for_time()
        
    elif option=="stop":
        client.sendall(bytes(option,encoding="utf-8"))
        client.close()
        connexion=False
        


