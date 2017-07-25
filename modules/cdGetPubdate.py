from bs4 import BeautifulSoup
import requests
import re
import dateutil.parser
import logging

# pretend we are firefox browser, this ensure we can get right web page
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686 (x86_64); rv:2.0b4pre) '
    'Gecko/20100812 Minefield/4.0b4pre'}
moduleTag = "Pubdate tag"


def parseStrDate(dateString):
    try:
        dateTimeObj = dateutil.parser.parse(dateString)
        return dateTimeObj
    except:
        return None


def _extractFromURL(url):
    '''
    Regex by Newspaper3k  -
    https://github.com/codelucas/newspaper/blob/master/newspaper/urls.py
    '''
    m = re.search(
        r'([\./\-_]{0,1}(19|20)\d{2})[\./\-_]{0,1}(([0-3]{0,1}[0-9][\./\-_])'
        '|(\w{3,5}[\./\-_]))([0-3]{0,1}[0-9][\./\-]{0,1})?', url)
    if m:
        return parseStrDate(m.group(0))

    return None


def getPubdate(url, outputArray, indexOfOutputArray, verbose=False, **kwargs):
    date = None
    try:
        logging.debug("cdGetPubdate: Try to get time from url")
        logging.debug("cdGetPubdate: Date extracted from url: %s", date)
        logging.debug("cdGetPubdate: Downloading web page")
        response = requests.get(url, headers=headers)
    except Exception:
        logging.debug("cdGetPubdate: Error while downloading web page")
        date = _extractFromURL(url)
        if date is not None:
            date_str = date.strftime('%Y-%m-%dT%H:%M:%S')
            outputArray[indexOfOutputArray] = date_str
            kwargs['displayArray'][indexOfOutputArray] = date_str
            logging.debug("Done Pubdate")
            return date_str
        else:
            return ''

    html = response.text
    soup = BeautifulSoup(html, 'lxml')

    # get pubdate in meta tag
    logging.debug("cdGetPubdate: Try to get time from meta tag")
    metaDate = None
    for meta in soup.findAll("meta"):
        metaName = meta.get('name', '').lower()
        itemProp = meta.get('itemprop', '').lower()
        httpEquiv = meta.get('http-equiv', '').lower()
        metaProperty = meta.get('property', '').lower()

        # Different types of meta attributes that can hold creation date.
        # date should be the last entry
        metaAttrs = set(['pubdate', 'publishdate', 'timestamp',
                         'dc.date.issued',
                         'article:published_time', 'bt:pubdate', 'og:pubdate',
                         'sailthru.date', 'article.published',
                         'published-date',
                         'article.created', 'article_date_original',
                         'cxenseparse:recs:publishtime', 'date_published',
                         'datepublished', 'datecreated', 'date'])

        if metaName in metaAttrs:
            metaDate = meta['content'].strip()
            break
        elif itemProp in metaAttrs:
            metaDate = meta['content'].strip()
            break
        elif httpEquiv in metaAttrs:
            metaDate = meta['content'].strip()
            break
        elif metaProperty in metaAttrs:
            metaDate = meta['content'].strip()
            break

    if metaDate is None:
        date = _extractFromURL(url)

    if metaDate is not None:
        date = parseStrDate(metaDate)

    date_str = ''
    if date is not None:
        date_str = date.strftime('%Y-%m-%dT%H:%M:%S')
    outputArray[indexOfOutputArray] = date_str
    kwargs['displayArray'][indexOfOutputArray] = date_str
    logging.debug("Done Pubdate")
    return date_str
