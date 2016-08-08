import sqlite3
from datetime import date, timedelta
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

    return str(dblist)

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
      return '{ "var1":"%d", "var2":"%d", "var3":"%d", "var4":"%d"}' % (int(random()*34), int(random()*33), int(random()*33), int(random()*33))
    
    @cherrypy.expose
    def submit (self, **vars):
        return fetchData(int(vars['start']), int(vars['end']))

cherrypy.quickstart(HelloWorld(), '/api')

