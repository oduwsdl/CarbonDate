from checkForModules import checkForModules
import json
import re
import urlparse
import os,sys, traceback
from ordereddict import OrderedDict
from pprint import pprint
from threading import Thread
import datetime

from cdGetBitly import getBitlyCreationDate
from cdGetArchives import getArchivesCreationDate
from cdGetGoogle import getGoogleCreationDate
from cdGetBacklinks import *
from cdGetLowest import getLowest
from cdGetLastModified import getLastModifiedDate
from cdHtmlMessages import *

def cd(url, backlinksFlag = False):

    #print 'Getting Creation dates for: ' + url
    #scheme missing?
    parsedUrl = urlparse.urlparse(url)
    if( len(parsedUrl.scheme)<1 ):
        url = 'http://'+url
    
    
    threads = []
    outputArray =['','','','','','']
    now0 = datetime.datetime.now()
    
   
    lastmodifiedThread = Thread(target=getLastModifiedDate, args=(url, outputArray, 0))
    bitlyThread = Thread(target=getBitlyCreationDate, args=(url, outputArray, 1))
    googleThread = Thread(target=getGoogleCreationDate, args=(url, outputArray, 2))
    archivesThread = Thread(target=getArchivesCreationDate, args=(url, outputArray, 3))
    
    if( backlinksFlag ):
        backlinkThread = Thread(target=getBacklinksFirstAppearanceDates, args=(url, outputArray, 4))

    # Add threads to thread list
    threads.append(lastmodifiedThread)
    threads.append(bitlyThread)
    threads.append(googleThread)	
    threads.append(archivesThread)

    if( backlinksFlag ):
        threads.append(backlinkThread)
    
    # Start new Threads
    lastmodifiedThread.start()
    bitlyThread.start()
    googleThread.start()
    archivesThread.start()

    if( backlinksFlag ):
        backlinkThread.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
        
    # For threads
    lastmodified = outputArray[0]
    bitly = outputArray[1] 
    google = outputArray[2] 
    archives = outputArray[3] 
    
    if( backlinksFlag ):
        backlink = outputArray[4]
    else:
        backlink = ''
    
    #note that archives["Earliest"] = archives[0][1]
    try:
        lowest = getLowest([lastmodified, bitly, google, archives[0][1], backlink]) #for thread
    except:
       print sys.exc_type, sys.exc_value , sys.exc_traceback

    result = []
    
    result.append(("URI", url))
    result.append(("Estimated Creation Date", lowest))
    result.append(("Last Modified", lastmodified))
    result.append(("Bitly.com", bitly))
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
    



if len(sys.argv) == 1:
    print "Usage: ", sys.argv[0] + " url backlinksOnOffFlag ( e.g: " + sys.argv[0] + " http://www.cs.odu.edu  [--compute-backlinks] )"
elif len(sys.argv) == 2:
    #fix for none-thread safe strptime
    #If time.strptime is used before starting the threads, then no exception is raised (the issue may thus come from strptime.py not being imported in a thread safe manner). -- http://bugs.python.org/issue7980
    time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')
    cd(sys.argv[1])
elif len(sys.argv) == 3:
    time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')
    
    if(sys.argv[2] == '--compute-backlinks'):
        cd(sys.argv[1], True)
    else:
        cd(sys.argv[1])
  
  
  
  





