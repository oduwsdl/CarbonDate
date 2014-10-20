import cherrypy
from checkForModules import checkForModules
import json
from ordereddict import OrderedDict
import simplejson

import re

from getBitly import getBitlyCreationDate
from getArchives import getArchivesCreationDate
from getGoogle import getGoogleCreationDate
from getBacklinks import *
from getLowest import getLowest
from getLastModified import getLastModifiedDate
from getTopsyScrapper import getTopsyCreationDate
from htmlMessages import *
from pprint import pprint

from threading import Thread
import Queue
import datetime

import sys, traceback



class CarbonDateServer(object):
    @cherrypy.expose
    def cd(self, url):

        if(len(url) < 1):
            return "Url length less than 1"

        response = cherrypy.response
        response.headers['Content-Type'] = 'application/json'

        print 'Getting Creation dates for: ' + url

        threads = []
        outputArray =['','','','','','']
        now0 = datetime.datetime.now()
        
       
        lastmodifiedThread = Thread(target=getLastModifiedDate, args=(url, outputArray, 0))
        bitlyThread = Thread(target=getBitlyCreationDate, args=(url, outputArray, 1))
        googleThread = Thread(target=getGoogleCreationDate, args=(url, outputArray, 2))
        archivesThread = Thread(target=getArchivesCreationDate, args=(url, outputArray, 3))
        backlinkThread = Thread(target=getBacklinksFirstAppearanceDates, args=(url, outputArray, 4))
        topsyThread = Thread(target=getTopsyCreationDate, args=(url, outputArray, 5))
        

        # Add threads to thread list
        threads.append(lastmodifiedThread)
        threads.append(bitlyThread)
        threads.append(googleThread)	
        threads.append(archivesThread)
        threads.append(backlinkThread)
        threads.append(topsyThread)	

        
        # Start new Threads
        lastmodifiedThread.start()
        bitlyThread.start()
        googleThread.start()
        archivesThread.start()
        backlinkThread.start()
        topsyThread.start()

        
        # Wait for all threads to complete
        for t in threads:
            t.join()
            
        # For threads
        lastmodified = outputArray[0]
        bitly = outputArray[1] 
        google = outputArray[2] 
        archives = outputArray[3] 
        backlink = outputArray[4]
        topsy = outputArray[5]  
        
        #note that archives["Earliest"] = archives[0][1]
        try:
            lowest = getLowest([lastmodified, bitly, google, archives[0][1], backlink, topsy]) #for thread
        except:
           print sys.exc_type, sys.exc_value , sys.exc_traceback
        
        

        result = []
        
        result.append(("URI", url))
        result.append(("Estimated Creation Date", lowest))
        result.append(("Last Modified", lastmodified))
        result.append(("Bitly.com", bitly))
        result.append(("Topsy.com", topsy))
        result.append(("Backlinks", backlink))
        result.append(("Google.com", google))
        result.append(("Archives", archives))
        values = OrderedDict(result)
        r = json.dumps(values, sort_keys=False, indent=2, separators=(',', ': '))
        
        now1 = datetime.datetime.now() - now0

        
        #print "runtime in seconds: " 
        #print now1.seconds
        #print r
        print 'runtime in seconds:  ' +  str(now1.seconds) + '\n' + r + '\n'
        return r
    



if __name__ == '__main__':
    #fix for none-thread safe strptime
    #If time.strptime is used before starting the threads, then no exception is raised (the issue may thus come from strptime.py not being imported in a thread safe manner). -- http://bugs.python.org/issue7980
    time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')

    fileConfig = open("config", "r")
    config = fileConfig.read()
    fileConfig.close()
    jsonFile = simplejson.loads(config)
    ServerIP = jsonFile["ServerIP"]
    ServerPort = jsonFile["ServerPort"]

    cherrypy.config.update({'server.socket_host': str(ServerIP),
                          'server.socket_port': int(ServerPort)})
    cherrypy.quickstart(CarbonDateServer())
  
  
  
  
  





