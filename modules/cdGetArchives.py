import time
import urllib.request, urllib.error, urllib.parse
import sys
import calendar
import requests
import json
import logging

moduleTag="Archives"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

def getMementos(uri):

    uri = uri.replace(' ', '')

    #baseURI = 'http://timetravel.mementoweb.org/timemap/link/'
    #baseURI = 'http://mementoweb.org/timemap/link/'
    # baseURI = 'http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/'
    #OR
    baseURI = 'http://memgator.cs.odu.edu/timemap/json/'
    memento_list = []

    try:
        search_results = urllib.request.urlopen(baseURI+uri)
        the_page = search_results.read().decode('ascii','ignore')

        data = json.loads(the_page)

        mementoNames = []
        for item in data["mementos"]["list"]:
            memento = {}

            timestamp = item["datetime"]
            mementoURL = item["uri"]

            epoch = int(calendar.timegm(time.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')))
            day_string = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(epoch))

            memento["time"] = day_string

            name = urllib.parse.urlparse(mementoURL.strip())

            memento["name"] = name.netloc
            memento["link"] = mementoURL

            # assumption that first memento is youngest - ON - start
            if( name.netloc not in mementoNames ):
                memento_list.append(memento)
                mementoNames.append(name.netloc)

    except urllib.error.URLError:
        pass

    return memento_list


def getRealDate(url, memDate):
    try:
        response = requests.get(url,headers=headers)
        page = response.headers
        date = ""

        if "X-Archive-Orig-last-modified" in page:
            date=page["X-Archive-Orig-last-modified"]
        elif 'X-Archive-Orig-date' in page:
            date=page['X-Archive-Orig-date']

        if(date ==""):
            date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(memDate))    
        else:
            epoch = int(calendar.timegm(time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')))
            date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(epoch))
        
        return date  
    except Exception:
        date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(memDate))
        return date


def getArchives(url, outputArray, outputArrayIndex,verbose=False,**kwargs):
    
    try:
        mementos = getMementos(url)

        if(len(mementos) == 0):
            result = []
            result.append(("Earliest", ""))
            result.append(("By_Archive", dict([])))
            outputArray[outputArrayIndex] = result[0][1]
            logging.debug ("Done Archives 0")
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
        
        outputArray[outputArrayIndex] = result[0][1]
        kwargs['displayArray'][outputArrayIndex] = result
        logging.debug ("Done Archives 1")
        return dict(result)

    except:
        logging.exception (sys.exc_info())
        result = []
        result.append(("Earliest", ""))
        result.append(("By_Archive", dict([])))

        outputArray[outputArrayIndex] = result[0][1]
        kwargs['displayArray'][outputArrayIndex] = result
        logging.debug ("Done Archives 2")
        return dict(result)
