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
class HelloWorld(object):
    #This section is for the index. It returns a json string with random integers.
    @cherrypy.expose
    def index(self):
      return '{ "var1":"%d", "var2":"%d", "var3":"%d", "var4":"%d"}' % (int(random()*34), int(random()*33), int(random()*33), int(random()*33))
    
    #This section is for the submit section. The vars[] object is an array of dictionary items, so youd have json style data here. This works for both POST and GET (http://server/api/submit?var1=something&var2=somethingelse)
    #This method returns nothing, but that can be changed (you might want a response code, especially for a GET request)
    @cherrypy.expose
    def submit (self, **vars):
        for x in vars:
            print x,'+',vars[x]

cherrypy.quickstart(HelloWorld(), '/api')

