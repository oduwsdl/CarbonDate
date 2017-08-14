import time
import urllib.request
import urllib.error
import urllib.parse
import sys
import calendar
import requests
import json
import logging
from .cdGetPubdate import getPubdate
from .cdGetLowest import getLowest, validateDate

moduleTag = "Archives"

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) \
    Gecko/20100101 Firefox/48.0'}


def getMementos(uri):

    uri = uri.replace(' ', '')

    # baseURI = 'http://timetravel.mementoweb.org/timemap/link/'
    # baseURI = 'http://mementoweb.org/timemap/link/'
    # baseURI = 'http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/'
    # OR
    baseURI = 'http://memgator.cs.odu.edu/timemap/json/'
    memento_list = []

    try:
        search_results = urllib.request.urlopen(baseURI + uri)
        the_page = search_results.read().decode('ascii', 'ignore')

        data = json.loads(the_page)

        mementoNames = []
        for item in data["mementos"]["list"]:
            memento = {}

            timestamp = item["datetime"]
            mementoURL = item["uri"]

            epoch = int(calendar.timegm(
                time.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')))
            day_string = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(epoch))

            memento["time"] = day_string

            name = urllib.parse.urlparse(mementoURL.strip())

            memento["name"] = name.netloc
            memento["link"] = mementoURL

            # assumption that first memento is youngest - ON - start
            if(name.netloc not in mementoNames):
                memento_list.append(memento)
                mementoNames.append(name.netloc)

    except urllib.error.URLError:
        pass

    return memento_list


def getRealDate(url, memDate):
    '''Expects epoch date as parameter'''
    try:
        response = requests.get(url, headers=headers)
        page = response.headers
        date = ""

        if "X-Archive-Orig-last-modified" in page:
            date = page["X-Archive-Orig-last-modified"]

        if(date == ""):
            date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(memDate))
        else:
            epoch = int(calendar.timegm(time.strptime(
                date, '%a, %d %b %Y %H:%M:%S %Z')))
            date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(epoch))

        return date
    except Exception:
        date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(memDate))
        return date


def getArchives(url, outputArray, outputArrayIndex, verbose=False, **kwargs):
    '''
    Return dictionary with earliest date, unique archives, or an empty
    dictionary if no mementos
    '''
    try:
        mementos = getMementos(url)

        if(len(mementos) == 0):
            result = {}
            result["Earliest"] = ""
            result["By_Archive"] = []
            outputArray[outputArrayIndex] = result["Earliest"]
            kwargs['displayArray'][outputArrayIndex] = result
            logging.debug("Done Archives 0")
            return result

        archives = {}

        for memento in mementos:
            epoch = int(calendar.timegm(time.strptime(
                memento["time"], '%Y-%m-%dT%H:%M:%S')))
            if(memento["name"] not in archives):
                archives[memento["name"]] = {
                    "link": memento["link"], "time": epoch}
            else:
                if(epoch < archives[memento["name"]]["time"]):
                    archives[memento["name"]]["time"] = epoch
                    archives[memento["name"]]["link"] = memento["link"]

        lowest = 99999999999

        limitEpoch = int(calendar.timegm(time.strptime(
            "1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))

        for archive in archives:
            date = getRealDate(
                archives[archive]["link"], archives[archive]["time"])
            epoch = int(calendar.timegm(
                time.strptime(date, '%Y-%m-%dT%H:%M:%S')))

            if(epoch < limitEpoch):
                archives[archive]["time"] = ""
                continue

            archives[archive]["time"] = date
            if(epoch < lowest):
                lowest = epoch

        lowest = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest))

        result = {}
        dates = []
        by_arch = []
        for archive in archives:
            result2 = {}
            if(archives[archive]["time"] == ""):
                continue

            result2["URI"] = archives[archive]["link"]
            result2["memento_datetime"] = archives[archive]["time"]
            result2["pubdate"] = getPubdate(archives[archive]["link"], [''], 0,
                                            verbose=False,
                                            displayArray={"Pubdate": ""})

            result2["pubdate"] = validateDate(result2["pubdate"])
            dates.append(result2["memento_datetime"])

            if result2["memento_datetime"] != "":
                dates.append(result2["memento_datetime"])

            by_arch.append(result2)

        result["Earliest"] = getLowest(dates=dates)

        result["By_Archive"] = by_arch

        outputArray[outputArrayIndex] = result["Earliest"]
        kwargs['displayArray'][outputArrayIndex] = result
        logging.debug("Done Archives 1")
        return result

    except:
        logging.exception(sys.exc_info())
        result = {}
        result["Earliest"] = ""
        result["By_Archive"] = []

        outputArray[outputArrayIndex] = result["Earliest"]
        kwargs['displayArray'][outputArrayIndex] = result
        logging.debug("Done Archives 2")
        return result
