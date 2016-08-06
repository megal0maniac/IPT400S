import sqlite3
import os
import sys
import time
import serial
import ast

wind_dir = {0 : 'N', 1 : 'NNW', 2 : 'NW', 3 : 'WNW', 4 : 'W', 5 : 'WSW', 6 : 'SW', 7 : 'SSW', 8 : 'S', 9 : 'SSE', 10 : 'SE', 11 : 'ESE', 12 : 'E', 13 : 'ENE', 14 : 'NE', 15 : 'NNE', 16 : 'N'}
resolution = 2
#TODO: This should become a variable later, both baud and device
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

#Read data from serial every minute
#This relies on reading serial data taking less than 59 seconds
while True:
    if int(time.time())%resolution != 0:
        time.sleep(1)
    else:
        #serial code here
        ser.flush()
        ser.write(' ') #TODO: Single byte generates response, this should be more specific
        data = ast.literal_eval(ser.readline())
        print '{} Temperature: {}C, Humidity: {}%, Wind speed: {}km/h, Wind direction: {}, Rain (since last reading): {}mm'.format(int(time.time()) - int(time.time())%resolution, data['t'], data['h'], data['ws'], wind_dir[data['wd']], data['rain']*2.46)
        time.sleep(1)

