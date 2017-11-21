import calendar
import time
import requests
from .cdGetLowest import getLowest, validateDate
from random import randint
import logging
import urllib.parse
import re

moduleTag = 'google.com'


def randSleep():
    """
    Sleep on page load
    """
    sleepSeconds = randint(2, 7)
    logging.debug('cdGetGoogle::randSleep(), sleep: %s', sleepSeconds)
    time.sleep(sleepSeconds)


def getTimestampFromSERP(locationOfSignature, page):
    """
    Iterate backwards from position of signature to find timestamp
    """
    timestamp = ''
    k = locationOfSignature

    while k > -1:
        # end marker
        if page[k] != '>':
            timestamp = page[k] + timestamp
        else:
            break
        k = k - 1

    timestamp = timestamp.strip()

    return timestamp


def mimicBrowser(query):
    """
    Mimic browser request to Google on query
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; '
            'rv:38.0) Gecko/20100101 Firefox/38.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
            '*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connnection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        }

        response = requests.get(query, headers=headers)
        return response.text
    except Exception as e:
        logging.debug('Failed to complete request. Return with error:', e)
        return ''


def findSignatures(page):
    """
    Regex to the last possible position of a date in a rendered page.
    Searches for dash surrounded by spaces with a span or div element at the
    end of a possible text entry.
    """
    positions = []
    # Date located before this regex
    p = re.compile('( [-] )(.*?<\/div>|<\/span>)')
    for m in p.finditer(page):
        positions.append(m.start())

    return positions


def genericGetCreationDate(page):
    """
    Go to each date position and attempt to get date
    """

    randSleep()
    allDates = []
    signaturePositions = findSignatures(page)

    for p in signaturePositions:
        timestamp = getTimestampFromSERP(p, page)
        # print('timestamp/locationOfSignature:', timestamp)

        try:
            epoch = calendar.timegm(
                time.strptime(timestamp, '%b %d, %Y'))
            date = time.strftime('%Y-%m-%dT%H:%M:%S',
                                 time.gmtime(epoch))
            allDates.append(date)
        except:
            pass

    return getLowest(allDates)


def getGoogle(url, outputArray, indexOfOutputArray, verbose=False, **kwargs):
    """
    Return earliest date found on a page rendered from Google
    """
    # Caution google blocks bots which do not play nice
    url = urllib.parse.quote(url, safe='')
    query = ('https://www.google.com/search?hl=en&tbo=d&tbs=qdr:y15'
             '&q=inurl:' + url + '&oq=inurl:' + url)

    page = mimicBrowser(query)
    inurl_creation_date = genericGetCreationDate(page)

    lowerDate = validateDate(inurl_creation_date)
    outputArray[indexOfOutputArray] = lowerDate
    kwargs['displayArray'][indexOfOutputArray] = lowerDate

    return lowerDate
