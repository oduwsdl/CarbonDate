import re
import time
import urllib2
import os
import sys
import datetime
import urllib
import simplejson
import calendar
import commands
import urlparse

from datetime import datetime

def getMementos(uri):

    uri = uri.replace(' ', '')
    orginalExpression = re.compile( r"<http://[A-Za-z0-9.:=/%-_ ]*>; rel=\"original\"," )
    mementoExpression = re.compile( r"<http://[A-Za-z0-9.:=/&,%-_ \?]*>;rel=\"(memento|first memento|last memento|first memento last memento|first last memento)\";datetime=\"(Sat|Sun|Mon|Tue|Wed|Thu|Fri), \d{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (19|20)\d\d \d\d:\d\d:\d\d GMT\"" )
    zeroMementoExpression = re.compile(r"Resource: http://[A-Za-z0-9.:=/&,%-_ ]*")

    #baseURI = 'http://timetravel.mementoweb.org/timemap/link/'
    #baseURI = 'http://mementoweb.org/timemap/link/'
    #OR
    baseURI = 'http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/'
    memento_list = []

    try:
        search_results = urllib.urlopen(baseURI+uri)
        the_page = search_results.read()

        timemapList = the_page.split('\n')
        mementoNames = []
        for line in timemapList:

            #reconsider this
            if(line.find("</memento")>0):
                line = line.replace("</memento", "<http://api.wayback.archive.org/memento")
    
    
            loc = line.find('>;rel="')

            #tofind = ';datetime="'
            tofind = '; datetime="'

            loc2 = line.find(tofind)
            if(loc!=-1 and loc2!=-1):
                mementoURL = line[3:loc]
                timestamp = line[loc2+len(tofind):line.find('"',loc2+len(tofind)+3)]

                epoch = int(calendar.timegm(time.strptime(timestamp, '%a, %d %b %Y %H:%M:%S %Z')))
                day_string = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(epoch))


                memento = {}
                
                memento["time"] = day_string

                name = urlparse.urlparse(mementoURL.strip())

                memento["name"] = name.netloc
                memento["link"] = mementoURL

                memento["link"] = urllib.quote(memento["link"])
                memento["link"] = memento["link"].replace("http%3A//", "http://")
                memento["link"] = memento["link"][memento["link"].find("http://"):]

                #assumption that first memento is youngest - ON - start
                
                if( name.netloc not in mementoNames ):
                    memento_list.append(memento)
                    mementoNames.append(name.netloc)
                
                #assumption that first memento is youngest - ON - end

                #assumption that first memento is NOT youngest - ON - start
                #memento_list.append(memento)
                #assumption that first memento is NOT youngest - ON - end




        
    
    except urllib2.URLError:
        pass


    return memento_list
  

def getRealDate(url, memDate):   
    co = 'curl -i --silent -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" "'+url+'"'
    page = commands.getoutput(co)
    date = ""

    #to_find = "X-Archive-Orig-Last-modified: "
    to_find = "X-Archive-Orig-last-modified: "
    loc = page.find(to_find)

    

    if(loc !=-1):
        end = page.find("\r", loc)
        date = page[loc+len(to_find):end]
        date = date.strip()

    if(date ==""):        
        #to_find = "X-Archive-Orig-Date: "
        to_find = "X-Archive-Orig-date: "
        loc = page.find(to_find)
        if(loc !=-1):
            end = page.find("\r", loc)
            date = page[loc+len(to_find):end]
            date = date.strip()

    if(date ==""):
        date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(memDate))    
    else:
        epoch = int(calendar.timegm(time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')))
        date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(epoch))
    
    return date  

def getArchivesCreationDate(url, outputArray, outputArrayIndex):
    
    try:
        mementos = getMementos(url)

        if(len(mementos) == 0):
            result = []
            result.append(("Earliest", ""))
            result.append(("By_Archive", dict([])))
            outputArray[outputArrayIndex] = result
            print "Done Archives 0"
            return dict(result)

        archives = {}

        for memento in mementos:
            epoch = int(calendar.timegm(time.strptime(memento["time"], '%Y-%m-%dT%H:%M:%S')))
            if(memento["name"] not in archives):
                archives[memento["name"]] = {"link":memento["link"], "time": epoch}
            else:
                if(epoch<archives[memento["name"]]["time"]):
                    archives[memento["name"]]["time"] = epoch
                    archives[memento["name"]]["link"] = memento["link"]



        lowest = 99999999999
        link = ""

        limitEpoch = int(calendar.timegm(time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))


        for archive in archives:
            date = getRealDate(archives[archive]["link"],archives[archive]["time"])
            epoch = int(calendar.timegm(time.strptime(date, '%Y-%m-%dT%H:%M:%S')))
            
            if(epoch<limitEpoch):
                archives[archive]["time"] = ""
                continue

            archives[archive]["time"] = date
            if(epoch<lowest):
                lowest = epoch

        lowest = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest))

        result = []
        result.append(("Earliest", lowest))

        result2 = []
        for archive in archives:
            if(archives[archive]["time"]==""):
                continue
            #result2.append((archive, str(archives[archive]["time"])))
            result2.append((archives[archive]["link"], str(archives[archive]["time"])))
        result.append(("By_Archive", dict(result2)))
        
        outputArray[outputArrayIndex] = result
        print "Done Archives 1"
        return dict(result)

    except:
        print sys.exc_info() 
        result = []
        result.append(("Earliest", ""))
        result.append(("By_Archive", dict([])))

        outputArray[outputArrayIndex] = result
        print "Done Archives 2"
        return dict(result)
