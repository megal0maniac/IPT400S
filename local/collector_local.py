#Michael Rodger 213085208
#Cape Peninsula University of Technology
#January 31 2017

import threading
import Queue
import os
import sqlite3
from datetime import date, timedelta, datetime
from ConfigParser import SafeConfigParser
import cherrypy
from random import random
from time import time

parser = SafeConfigParser()
parser.read('collector_local.conf')

listen_ip = parser.get('collector_local', 'listen_ip')
listen_port = int(parser.get('collector_local', 'listen_port'))
res = int(parser.get('collector_local', 'maxres'))
cherrypy.config.update({'server.socket_host': listen_ip,
                        'server.socket_port': listen_port,
                       })

cardinal_points = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
queryData = []

# Query all data for a given time range on the given db
def querydball(dbname, start, end):
    data = []
    if not os.path.exists('db/{}'.format(dbname)):
        print 'Warning! {} not found'.format(dbname)
        return

    conn = sqlite3.connect('db/{}'.format(dbname))
    cursor = conn.execute('SELECT * FROM WEATHER WHERE time >= {} AND time <= {}'.format(start, end))
    for row in cursor.fetchall():
        timestamp, windspeed, winddirection, temperature, humidity, rain = row
        data.append({'timestamp' : int(timestamp), 'windspeed' : float(windspeed), 'winddirection' : int(winddirection), 'temperature' : float(temperature), 'humidity' : float(humidity), 'rain' : float(rain)*0.2794 })

    global queryData
    queryData.extend(data)
    conn.close()

# Query the average values for a time range on the given db
def querydbaggregated(dbname, start, end):
    data = []
    if not os.path.exists('db/{}'.format(dbname)):
        print 'Warning! {} not found'.format(dbname)
        return

    conn = sqlite3.connect('db/{}'.format(dbname))
    cursor = conn.execute('SELECT MIN(time), AVG(windspeed), AVG(temperature), AVG(humidity), SUM(rain) FROM WEATHER WHERE time >= {} AND time <= {} GROUP BY strftime("%H", datetime(time, "unixepoch", "localtime"))'.format(start, end))
    for row in cursor.fetchall():
        timestamp, windspeed, temperature, humidity, rain = row
        data.append({'timestamp' : int(timestamp), 'windspeed' : float(windspeed), 'temperature' : float(temperature), 'humidity' : float(humidity), 'rain' : float(rain)*0.2794 })

    global queryData
    queryData.extend(data)
    conn.close()

# Generates a list of database filenames based on a time range
def getdblist(start, end):
    dblist = []
    startdate = date.fromtimestamp(start)
    enddate = date.fromtimestamp(end)
    if start > end:
        return ''
        #TODO throw exception
    else:
        delta = enddate - startdate
        for i in range(delta.days + 1):
            dblist.append('{}.db'.format(startdate + timedelta(days=i)))

    return dblist

# Multi-threaded fetch aggregated data
def fetchAggregatedData(start, end):
    dblist = getdblist(start, end)
    print str(dblist)

    # Collect the data
    data = []
    q = Queue.Queue()
    for database in dblist:    
        if database!= []:
            q.put(database)

    global queryData
    queryData = []
    threads = []
    while not q.empty():
        t = threading.Thread(target=querydbaggregated, args=(q.get(), start, end,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    queryDataSorted = []
    perm = sorted(xrange(len(queryData)), key=lambda x:queryData[x]['timestamp'])
    for p in perm:
        queryDataSorted.append({'timestamp' : queryData[p]['timestamp'], 'windspeed' : queryData[p]['windspeed'], 'temperature' : queryData[p]['temperature'], 'humidity' : queryData[p]['humidity'], 'rain' : queryData[p]['rain'] })

    return queryDataSorted

# Multi-threaded fetch all data
def fetchAllData(start, end):
    # Generate a list of all required database files to be read
    dblist = getdblist(start, end)
    print str(dblist)

    # Collect the data
    data = []
    q = Queue.Queue()
    for database in dblist:    
        if database!= []:
            q.put(database)

    global queryData
    queryData = []
    threads = []
    while not q.empty():
        t = threading.Thread(target=querydball, args=(q.get(), start, end,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    queryDataSorted = []
    perm = sorted(xrange(len(queryData)), key=lambda x:queryData[x]['timestamp'])
    for p in perm:
        queryDataSorted.append({'timestamp' : queryData[p]['timestamp'], 'windspeed' : queryData[p]['windspeed'], 'winddirection' : queryData[p]['winddirection'], 'temperature' : queryData[p]['temperature'], 'humidity' : queryData[p]['humidity'], 'rain' : queryData[p]['rain'] })

    return queryDataSorted

#Main function for the web interface
class Collector(object):
    @cherrypy.expose
    def index(self):
        return ':)'

    @cherrypy.expose
    def getdata (self, **vars):
        if len(vars) == 0: #Default to last 24 hours
            dataall = fetchAllData(int(time())-86400, int(time()))
            datahourly = fetchAggregatedData(int(time())-86400, int(time()))
        else:
            dataall = fetchAllData(int(vars['start']), int(vars['end']))
            datahourly = fetchAggregatedData(int(vars['start']), int(vars['end']))
        return '{{ "time" : {}, "timehourly" : {}, "windspeed" : {}, "winddirection" : {}, "temperature" : {}, "humidity" : {}, "rain" : {}, "raintotal" : {} }}'.format(
            str([datetime.fromtimestamp(dataall[x]['timestamp']).strftime('%Y-%m-%d %H:%M:%S') for x in range(0,len(dataall))]),
            str([datetime.fromtimestamp(datahourly[x]['timestamp']).strftime('%Y-%m-%d %H:%M:%S') for x in range(0,len(datahourly))]),
            str([dataall[x]['windspeed'] for x in range(0,len(dataall))]),
            str([dataall[x]['winddirection'] for x in range(0,len(dataall))]),
            str([dataall[x]['temperature'] for x in range(0,len(dataall))]),
            str([dataall[x]['humidity'] for x in range(0,len(dataall))]),
            str([datahourly[x]['rain'] for x in range(0,len(datahourly))]),
            str(sum([datahourly[x]['rain'] for x in range(0,len(datahourly))]))).replace('\'', '"')

    @cherrypy.expose
    def submit (self, **vars):
        print 'Submitted vars:'
        for x in vars:
            print '{}: {}\tType: {}\tLength: {}'.format(x, vars[x], type(vars[x]), len(vars[x]))

cherrypy.quickstart(Collector(), '/api')

