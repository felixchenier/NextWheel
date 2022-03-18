'''
Author: Clémence Starosta
year : 2022
'''

'''This library contains all the useful functions for extracting 
and formatting data about the wheel.

the table will look like this

[time,Channels[0],Channels[1],Channels[2],Channels[3],Channels[4],Channels[5],Battery,Forces[0],Forces[1],Forces[2],Forces[3],Moments[0],Moments[1],Moments[2],Moments[3] ]
[  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ]
    .
    .
    .
[  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ]'''

import csv
import numpy as np
file_data_wheel='kinetics_test.csv'

def csv_count_line(filename):
    '''count line number in a csv file'''
    with open(filename, 'r') as f:
        i = 0
        for line in f:
            i += 1
    return i

def open_add_data(filename):
    '''opening the file and inserting the data into a table. Returns the table'''
    with open(filename, newline='') as csvfile:       
        data_wheel1=np.zeros((csv_count_line(filename),16))
        lire=csv.reader(csvfile, delimiter=',')
        data_wheel1 = list(lire)
        data_wheel=list(np.float_(data_wheel1))
    return data_wheel

def print_data_wheel(data):
    '''Displaying the data table'''
    for elt in data:
        np.set_printoptions(precision = 6, suppress = True) 
        print(str(elt), ", ");

def element_data(time,column,data):
    '''
    time : 
        give the corresponding time in seconds
    column :
        7 for battery
        8 or 9 or 10 or 11 for force
        12 or 13 or 14 or 15 for moment
    '''
    for i in range(0,csv_count_line(file_data_wheel)):
        if data[i][0]==time:
            return data[i][column]

def return_data_time(time,data,column):
    for i in range(0,24):
        if data[i][0]==time:
            return data[i][column]
        
def average_data(data,filename):
    '''Averages two data and rounds up to the nearest ms'''
    average_data=np.zeros((24, 15))
    for i in range(0,csv_count_line(file_data_wheel)-2,2):
        for j in range(0,14):
            elt=(data[i][j]+data[i+1][j])/2
            k=int(i/2)
            average_data[k][j]=elt
    for i in range(0,int(csv_count_line(file_data_wheel)/2)):
        average_data[i][0]=round(average_data[i][0],3)
    return average_data