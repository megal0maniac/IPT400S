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

cherrypy.config.update({'server.socket_host': listen_ip,
                        'server.socket_port': listen_port,
                       })

cardinal_points = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
queryData = []

def querydb(dbname, start, end):
    data = []
    # TODO: Catch filenotfound exception
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

def fetchData(start, end):
    # Generate a list of all required database files to be read
    timethen = time()
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
        t = threading.Thread(target=querydb, args=(q.get(), start, end,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    queryDataSorted = []
    perm = sorted(xrange(len(queryData)), key=lambda x:queryData[x]['timestamp'])
    for p in perm:
        queryDataSorted.append({'timestamp' : queryData[p]['timestamp'], 'windspeed' : queryData[p]['windspeed'], 'winddirection' : queryData[p]['winddirection'], 'temperature' : queryData[p]['temperature'], 'humidity' : queryData[p]['humidity'], 'rain' : queryData[p]['rain'] })

#    return '{{"time": {}, "temp": {}, "humidity": {} }}'.format(str([datetime.fromtimestamp(queryDataSorted[x]['timestamp']).strftime('%Y-%m-%d %H:%M:%S') for x in range(0,len(queryDataSorted))]), str([queryDataSorted[x]['temperature'] for x in range(0,len(queryDataSorted))]), str([queryDataSorted[x]['humidity'] for x in range(0,len(queryDataSorted))])).replace('\'', '"')

    output = '<table border=1><tr><th>Time</th><th>Windspeed</th><th>Wind direction</th><th>Temperature</th><th>Humidity</th><th>Rainfall</th></tr>'
    for x in queryDataSorted:
        output = output + '<tr><td>{}</td><td>{}km/h</td><td>{}</td><td>{}C</td><td>{}%</td><td>{}mm</td></tr>'.format(datetime.fromtimestamp(x['timestamp']).strftime('%Y-%m-%d %H:%M:%S'), x['windspeed'], cardinal_points[x['winddirection']], x['temperature'], x['humidity'], x['rain'])

    output = output + '</table>'

    print time() - timethen
    return output

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
      return '{ "var1":"%d", "var2":"%d", "var3":"%d", "var4":"%d"}' % (int(random()*34), int(random()*33), int(random()*33), int(random()*33))
    
    @cherrypy.expose
    def getdaterange (self, **vars):
        if len(vars) == 0:
            return fetchData(int(time())-600, int(time()))
        else:
            return fetchData(int(vars['start']), int(vars['end']))

    @cherrypy.expose
    def submit (self, **vars):
        print 'Submitted vars:'
        for x in vars:
            print '{}: {}\tType: {}\tLength: {}'.format(x, vars[x], type(vars[x]), len(vars[x]))

cherrypy.quickstart(HelloWorld(), '/api')

