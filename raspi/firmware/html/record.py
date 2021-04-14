#!/usr/bin/python3
# coding=UTF-8

"""
record.py

Usage : record.py <Time in seconds> <Trial name>
Example : record.py 10 "test trial"

This script records the ADC signals into a CSV file, then generates a PNG plot
of the recorded data.

Adaptive Sports Biomechanics Research Lab

Date : May 2018
Author : Felix Chenier
"""

import time
import datetime
import sys
import spidev
import os
import RPi.GPIO as GPIO


from time import gmtime, strftime
from datetime import datetime
from datetime import timedelta
from debugMode import debugMode

# Create a RECORDING flag to know that we are recording.
os.system("touch files/RECORDING")

# Read input parameters
recordTime = int(sys.argv[1])
trial_name = sys.argv[2]

#============================================
# SPI and GPIO Configuration
#
# SPI from:
# http://www.takaitra.com/posts/492
#
# GPIO from:
# https://www.raspberrypi.org/documentation/usage/gpio/python/README.md
#--------------------------------------------

# Open SPI
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 15600000 # 15.6 MHz (Max de 20 MHz de l'ADC)

# Configure GPIO
GPIO.setmode(GPIO.BOARD)

# outputs
pinD1 = 3
pinD2 = 5
pinD3 = 7
pinD4 = 29
pinRDn = 24
pinCONVST = 13

# inputs
pinBUSYn = 31

GPIO.setup([pinD1, pinD2, pinD3, pinD4, pinRDn], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup([pinCONVST], GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup([pinBUSYn], GPIO.IN)

#============================================
# Opening output file
#--------------------------------------------
fileList = os.listdir('files')
nFiles = len(fileList)

filename = ("files/" + str(nFiles-1).rjust(4, '0') + "_" +
            trial_name.replace(' ', '') + '_' +
            str(recordTime) + "s.csv")
fid = open(filename, "w")

#============================================
# Start the record loop
#--------------------------------------------
startTime = time.time()
currentTime = startTime

currentChannel = 0
lastChannel = -1
currentCSVLine = '0,'

while(currentTime - startTime < recordTime):
	
	# Configuring control bits
	
	# Mux address: SGL, ODDSIGN, SELECT0, SELECT1
	SGL = 1
	ODDSIGN = currentChannel % 2
	SELECT0 = (currentChannel >> 1) % 2
	SELECT1 = (currentChannel >> 2) % 2
	
	# Input range
	UNI = 0		# 0 = Bipolaire, 1 = Unipolaire
	GAIN = 1	# 0 = ±5V, 1 = ±10 V
	
	# Power down : Always ON.
	NAP = 0
	SLEEP = 0
	
	# Wait for completion of last conversion
	if (debugMode == 0):
		while(GPIO.input(pinBUSYn) == GPIO.LOW):
			pass	
	
	# Send channel configuration
	msb = (SGL << 7) + (ODDSIGN << 6) + (SELECT1 << 5) + (SELECT0 << 4) + (UNI << 3) + (GAIN << 2) + (NAP << 1) + SLEEP
	lsb = 0;
	receivedData = spi.xfer([msb, lsb])
	msb = receivedData[0]
	lsb = receivedData[1]
	
	# Start the next conversion now
	GPIO.output(pinCONVST, GPIO.LOW)
	
	if(lastChannel >= 0):
		
		if(msb < 128):
			data = int(msb<<8 | lsb)
		else:
			data = int(msb<<8 | lsb) - 65536

		currentCSVLine = currentCSVLine + str(data)
		
		if(lastChannel < 7):
			currentCSVLine = currentCSVLine + ','
		else:
			# Line is complete. Write on file and start next line.
			fid.write(currentCSVLine + '\n')
			currentTime = time.time()
			timeStamp = str((round((currentTime - startTime)*100000))/100000)
			currentCSVLine = timeStamp + ','
		
	# Next channel
	lastChannel = currentChannel
	currentChannel = currentChannel + 1
	if(currentChannel > 7):
		currentChannel = 0
		
	# Put back CONVST to 1
	GPIO.output(pinCONVST, GPIO.HIGH)


# Close the file
fid.close
GPIO.cleanup()

# Create a picture
import matplotlib.pyplot as plt
import numpy as np

data = np.genfromtxt(filename, delimiter=',')
print(data)
fig = plt.figure()
plt.plot(data[:,0], data[:,1:8])
plt.legend(['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz', 'Battery'])
plt.ylabel('Raw ADC Values')
plt.xlabel('Time (s)')
plt.title(filename)
fig.set_size_inches(20, 3)
fig.tight_layout()
fig.savefig(filename + '.png')

os.system(f"sudo -u pi cp -f {filename} files/latest.csv")
os.system(f"sudo -u pi cp -f {filename + '.png'} files/latest.png")

# Clear the RECORDING flag
os.system("rm files/RECORDING")
