import sqlite3
import os
import sys
import time

#Read data from serial every minute
#This relies on reading serial data taking less than 59 seconds

while True:
    if int(time.time())%60 != 0:
        time.sleep(1)
    else:
        print 'blep'
        time.sleep(1)

