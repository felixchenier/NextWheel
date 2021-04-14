#!/usr/bin/python3
# coding=UTF-8

"""
battery.py

Usage : battery.py

This script prints the battery charge in percentage.

Adaptive Sports Biomechanics Research Lab

Date : October 2019
Author : Felix Chenier
"""

import spidev
import RPi.GPIO as GPIO
from debugMode import debugMode


#============================================
# CONSTANTS
full_battery = 26700
empty_battery = 23500


#============================================
# Do not execute if we are recording.
try:
    with open('RECORDING'):
        print('Recording...')
except:

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

    GPIO.setwarnings(False)
    GPIO.setup([pinD1, pinD2, pinD3, pinD4, pinRDn], GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup([pinCONVST], GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup([pinBUSYn], GPIO.IN)

    currentChannel = 7

    for i_sample in range(2):  # Send two inputs. One to start the acquisition, the
                               # other to receive the result.
    
        # Configuring control bits
    
        # Mux address: SGL, ODDSIGN, SELECT0, SELECT1
        SGL = 1
        ODDSIGN = currentChannel % 2
        SELECT0 = (currentChannel >> 1) % 2
        SELECT1 = (currentChannel >> 2) % 2
    
        # Input range
        UNI = 0     # 0 = Bipolaire, 1 = Unipolaire
        GAIN = 1    # 0 = ±5V, 1 = ±10 V
    
        # Power down : Always ON.
        NAP = 0
        SLEEP = 0
    
        # Wait for completion of last conversion
        if (debugMode == 0):
            while(GPIO.input(pinBUSYn) == GPIO.LOW):
                pass    
    
        # Send channel configuration
        msb = ((SGL << 7) + (ODDSIGN << 6) + (SELECT1 << 5) +
               (SELECT0 << 4) + (UNI << 3) + (GAIN << 2) + (NAP << 1)) + SLEEP
        lsb = 0;
        receivedData = spi.xfer([msb, lsb])
        msb = receivedData[0]
        lsb = receivedData[1]
    
        # Start the next conversion now
        GPIO.output(pinCONVST, GPIO.LOW)

        if(msb < 128):
            data = int(msb<<8 | lsb)
        else:
            data = int(msb<<8 | lsb) - 65536

        # Put back CONVST to 1
        GPIO.output(pinCONVST, GPIO.HIGH)

    print(int((data - empty_battery) / (full_battery - empty_battery) * 100))
