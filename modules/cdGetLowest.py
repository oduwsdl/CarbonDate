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
    lowest_epoch = 99999999999
    for date in dates:
        if(date == "" or date == "Bitly Key has expired"):
            continue
        epoch = int(calendar.timegm(time.strptime(date, '%Y-%m-%dT%H:%M:%S')))

        limitEpoch = int(calendar.timegm(time.strptime(
            "1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))
        if(epoch < limitEpoch):
            continue

        if(epoch < lowest_epoch):
            lowest_epoch = epoch

    if(lowest_epoch == 99999999999):
        return ""

    return time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest_epoch))
