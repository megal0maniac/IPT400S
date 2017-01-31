#Michael Rodger 213085208
#Cape Peninsula University of Technology
#January 31 2017

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

ser = serial.Serial(serial_device, serial_baud, timeout=serial_timeout)
print 'Starting collector daemon...'

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
            f.write(currentdb.split('/')[-1])
            print 'folder'
            print currentdb.split('/')[-1]
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
        ser.write(' ')
        data = ast.literal_eval(ser.readline())
        lasttime = data['time'] = int(time.time())
        writeToDB(data)
        time.sleep(0.2)
    else:
        time.sleep(0.2)
