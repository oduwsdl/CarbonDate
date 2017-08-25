import calendar
import time
# replace parts of date
from datetime import datetime


def validateDate(date):
    '''
    Force date to last second of the day if date is set at midnight
    For example: 2017-07-04T00:00:00 -> 2017-07-04T23:59:59
    '''
    try:
        urlDate = datetime.strptime(
            date, '%Y-%m-%dT%H:%M:%S')

        if urlDate.hour == 0 and urlDate.minute == 0 and urlDate.second == 0:

            newDate = urlDate.replace(hour=23, minute=59, second=59)
            newDate = newDate.strftime('%Y-%m-%dT%H:%M:%S')
            return newDate

        return date
    except Exception:
        return date


def getLowest(dates):
    '''
    Find the earliest date, in YYYY-MM-DDTHH:MM:SS format, in a given dates
    array.
    '''
    lowest_epoch = 99999999999
    for date in dates:
        try:
            epoch = int(calendar.timegm(
                time.strptime(date, '%Y-%m-%dT%H:%M:%S')))

            limitEpoch = int(calendar.timegm(time.strptime(
                "1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))
            if(epoch < limitEpoch):
                continue

            if(epoch < lowest_epoch):
                lowest_epoch = epoch
        except:
            continue

    if(lowest_epoch == 99999999999):
        return ""

    return time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest_epoch))


def getLowestSources(sources):
    '''
    Find earliest date from the 'sources' dictionary. Each dictionary
    must have a 'earliest' key to compare dates.

    Returns date of earliest sources(s) and array of source(s) that
    found the earliest date.
    '''
    lowest_epoch = 99999999999
    earliest_sources = []
    earliest_date = ""

    for source, sourceDict in sources.items():
        try:
            date = sourceDict["earliest"]
            epoch = int(calendar.timegm(
                time.strptime(date, '%Y-%m-%dT%H:%M:%S')))

            limitEpoch = int(calendar.timegm(time.strptime(
                "1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))
            if(epoch < limitEpoch):
                continue

            if(epoch < lowest_epoch):
                lowest_epoch = epoch
                earliest_date = date
                earliest_sources.append(source)
            elif(epoch == lowest_epoch):
                earliest_sources.append(source)
        except:
            continue

    return earliest_date, earliest_sources
