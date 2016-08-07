import sqlite3
import os
import sys
from datetime import date
import time
import serial
import ast
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('collector_remote.conf')

period = int(parser.get('collector_remote', 'period'))
serial_device = parser.get('collector_remote', 'serial_device')
serial_baud = int(parser.get('collector_remote', 'serial_baud'))
serial_timeout = int(parser.get('collector_remote', 'serial_timeout'))
database_path = parser.get('collector_remote', 'database_path')


wind_dir = {0 : 'N', 1 : 'NNW', 2 : 'NW', 3 : 'WNW', 4 : 'W', 5 : 'WSW', 6 : 'SW', 7 : 'SSW', 8 : 'S', 9 : 'SSE', 10 : 'SE', 11 : 'ESE', 12 : 'E', 13 : 'ENE', 14 : 'NE', 15 : 'NNE', 16 : 'N'}

#TODO: This should become a variable later, both baud and device
ser = serial.Serial(serial_device, serial_baud, timeout=serial_timeout)

def writeToDB(weatherdata):
    today = date.fromtimestamp(weatherdata['time'])
    currentdb = '{}{}-{:02d}-{:02d}.db'.format(database_path, today.year, today.month, today.day)
    newdb = not os.path.exists(currentdb)
    conn = sqlite3.connect(currentdb)
    if newdb:
        #create schema
        conn.execute("CREATE TABLE weather(time INT PRIMARY KEY NOT NULL, windspeed FLOAT, winddirection INT, temperature FLOAT, humidity FLOAT, rain INT)")
        #if the file is new, update the currentdb file. Hard-coded to write only the filename minus directory
        f = open('{}currentdb'.format(database_path), 'w')
        if '/' in currentdb:
            f.write(currentdb.split('/')[1])
            print 'folder'
            print currentdb.split('/')[1]
        else:
            f.write(currentdb)
            print 'pwd'
            print currentdb
        f.close()

    conn.execute("""INSERT INTO weather values({}, {}, {}, {}, {}, {})""".format(weatherdata['time'], weatherdata['ws'], weatherdata['wd'], weatherdata['t'], weatherdata['h'], weatherdata['rain']))
    conn.commit()
    conn.close()

#Read data from serial every minute
#This relies on reading serial data taking less than 59 seconds, should be fine?
lasttime = int(time.time()) - 1
while True:
    if ((int(time.time())%period == 0) and (lasttime != int(time.time()))):
        ser.flush()
        ser.write(' ') #TODO: Single byte generates response, this should be more specific
        data = ast.literal_eval(ser.readline())
        lasttime = data['time'] = int(time.time())
        #print 'Condition: {} Lasttime: {} DBTime: {} Real time: {}'.format(int(time.time())%resolution, lasttime, data['time'], time.time())
        #print '{} Temperature: {}C, Humidity: {}%, Wind speed: {}km/h, Wind direction: {}, Rain (since last reading): {}mm'.format(int(time.time()), data['t'], data['h'], data['ws'], wind_dir[data['wd']], data['rain']*2.46)
        writeToDB(data)
        time.sleep(0.2)
    else:
        time.sleep(0.2)
