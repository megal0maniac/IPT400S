import threading
import Queue
import os
import sqlite3
from datetime import date, timedelta, datetime
from ConfigParser import SafeConfigParser
import cherrypy
from random import random

parser = SafeConfigParser()
parser.read('collector_local.conf')

listen_ip = parser.get('collector_local', 'listen_ip')
listen_port = int(parser.get('collector_local', 'listen_port'))

cherrypy.config.update({'server.socket_host': listen_ip,
                        'server.socket_port': listen_port,
                       })

queryData = []

def querydb(dbname, start, end):
    print 'Querying {} for range {} - {}'.format(dbname, start, end)
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

def fetchData(start, end):
    # Generate a list of all required database files to be read
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
    
    main_thread = threading.currentThread()
    for t in threads:
        if t is main_thread:
            print 'main thread is a thing'
            continue
        print 'joining thread {}'.format(t)
        t.join()
    
    print 'Done with collection'

    output = '<table border=1><tr><th>Time</th><th>Windspeed</th><th>Wind direction</th><th>Temperature</th><th>Humidity</th><th>Rainfall</th></tr>'
    for x in queryData:
        output = output + '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(datetime.fromtimestamp(x['timestamp']).strftime('%Y-%m-%d %H:%M:%S'), x['windspeed'], x['winddirection'], x['temperature'], x['humidity'], x['rain'])

    output = output + '</table>'
    return output

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
      return '{ "var1":"%d", "var2":"%d", "var3":"%d", "var4":"%d"}' % (int(random()*34), int(random()*33), int(random()*33), int(random()*33))
    
    @cherrypy.expose
    def getdaterange (self, **vars):
        return fetchData(int(vars['start']), int(vars['end']))

    @cherrypy.expose
    def submit (self, **vars):
        print 'Submitted vars:'
        for x in vars:
            print '{}: {}\tType: {}\tLength: {}'.format(x, vars[x], type(vars[x]), len(vars[x]))

cherrypy.quickstart(HelloWorld(), '/api')

