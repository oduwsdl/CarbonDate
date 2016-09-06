import sys
from bs4 import BeautifulSoup
import datetime
import requests
from requests.utils import quote
import re
import dateutil.parser
import logging

#pretend we are firefox browser, this ensure we can get right web page
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686 (x86_64); rv:2.0b4pre) Gecko/20100812 Minefield/4.0b4pre'}
moduleTag="Pubdate tag"


def parseStrDate(dateString):
	try:
		dateTimeObj = dateutil.parser.parse(dateString)
		return dateTimeObj
	except:
		return None

def _extractFromURL(url):

	#Regex by Newspaper3k  - https://github.com/codelucas/newspaper/blob/master/newspaper/urls.py
	m = re.search(r'([\./\-_]{0,1}(19|20)\d{2})[\./\-_]{0,1}(([0-3]{0,1}[0-9][\./\-_])|(\w{3,5}[\./\-_]))([0-3]{0,1}[0-9][\./\-]{0,1})?', url)
	if m:
		return parseStrDate(m.group(0))


	return None

def getPubdate(url,outputArray, indexOfOutputArray,verbose=False,**kwargs):
	date=None
	try:
		logging.debug ( "cdGetPubdate: Try to get time from url" )
		date=_extractFromURL(url)
		logging.debug ( "cdGetPubdate: Date extracted from url: %s", date )
		logging.debug ( "cdGetPubdate: Downloading web page" )
		response = requests.get(url,headers=headers)
	except Exception as e:
		logging.debug ("cdGetPubdate: Error while downloading web page")
		if date is not None:
			date_str=date.strftime('%Y-%m-%dT%H:%M:%S')
			outputArray[indexOfOutputArray] = date_str
			logging.debug ("Done Pubdate" )
			return date_str
		else:
			return ''
	
	html = response.text
	soup = BeautifulSoup(html,'lxml')

	#try get time tag
	logging.debug ( "cdGetPubdate: Try to get time from time tag" )
	for time in soup.findAll("time"):
		datetime = time.get('datetime', '')
		if len(datetime) > 0:
			date = parseStrDate(datetime)

		logging.debug ( "cdGetPubdate: Date extracted from time tag:", date )
	if date is None:
	#get pubdate in meta tag
		logging.debug ("cdGetPubdate: Try to get time from meta tag")
		metaDate = None
		for meta in soup.findAll("meta"):
			metaName = meta.get('name', '').lower()
			itemProp = meta.get('itemprop', '').lower()
			httpEquiv = meta.get('http-equiv', '').lower()
			metaProperty = meta.get('property', '').lower()

			#<meta name="pubdate" content="2015-11-26T07:11:02Z" >
			if 'pubdate' == metaName:
				metaDate = meta['content'].strip()
				break

			#<meta name='publishdate' content='201511261006'/>
			if 'publishdate' == metaName:
				metaDate = meta['content'].strip()
				break

			#<meta name="timestamp"  data-type="date" content="2015-11-25 22:40:25" />
			if 'timestamp' == metaName:
				metaDate = meta['content'].strip()
				break

			#<meta name="DC.date.issued" content="2015-11-26">
			if 'dc.date.issued' == metaName:
				metaDate = meta['content'].strip()
				break

			#<meta property="article:published_time"  content="2015-11-25" />
			if 'article:published_time' == metaProperty:
				metaDate = meta['content'].strip()
				break
			#<meta name="Date" content="2015-11-26" />
			if 'date' == metaName:
				metaDate = meta['content'].strip()
				break

			#<meta property="bt:pubDate" content="2015-11-26T00:10:33+00:00">
			if 'bt:pubdate' == metaProperty or 'og:pubdate' == metaProperty :
				metaDate = meta['content'].strip()
				break
			#<meta name="sailthru.date" content="2015-11-25T19:56:04+0000" />
			if 'sailthru.date' == metaName:
				metaDate = meta['content'].strip()
				break

			#<meta name="article.published" content="2015-11-26T11:53:00.000Z" />
			if 'article.published' == metaName:
				metaDate = meta['content'].strip()
				break

			#<meta name="published-date" content="2015-11-26T11:53:00.000Z" />
			if 'published-date' == metaName:
				metaDate = meta['content'].strip()
				break

			#<meta name="article.created" content="2015-11-26T11:53:00.000Z" />
			if 'article.created' == metaName:
				metaDate = meta['content'].strip()
				break

			#<meta name="article_date_original" content="Thursday, November 26, 2015,  6:42 AM" />
			if 'article_date_original' == metaName:
				metaDate = meta['content'].strip()
				break

			#<meta name="cXenseParse:recs:publishtime" content="2015-11-26T14:42Z"/>
			if 'cxenseparse:recs:publishtime' == metaName:
				metaDate = meta['content'].strip()
				break

			#<meta name="DATE_PUBLISHED" content="11/24/2015 01:05AM" />
			if 'date_published' == metaName:
				metaDate = meta['content'].strip()
				break


			#<meta itemprop="datePublished" content="2015-11-26T11:53:00.000Z" />
			if 'datepublished' == itemProp:
				metaDate = meta['content'].strip()
				break


			#<meta itemprop="datePublished" content="2015-11-26T11:53:00.000Z" />
			if 'datecreated' == itemProp:
				metaDate = meta['content'].strip()
				break


			#<meta http-equiv="data" content="10:27:15 AM Thursday, November 26, 2015">
			if 'date' == httpEquiv:
				metaDate = meta['content'].strip()
				break
		
		if metaDate is not None:
			date = parseStrDate(metaDate)

	date_str=''
	if date is not None:
		date_str=date.strftime('%Y-%m-%dT%H:%M:%S')
	outputArray[indexOfOutputArray] = date_str
	kwargs['displayArray'][indexOfOutputArray] = date_str
	logging.debug ("Done Pubdate")
	return date_str

#################test entry####################
if __name__ == '__main__':
	import argparse
	parser=argparse.ArgumentParser()
	parser.add_argument("-v",action="store_true",help="Show verbose in output")
	parser.add_argument("url",help="The url to inspect")
	args=parser.parse_args()
	if len(sys.argv)<2:
		print("Unit testing usage: ", sys.argv[0] + " url  e.g: " + sys.argv[0] + " http://www.cs.odu.edu ")
	else:
		testarry=['']
		print(getPubdate(sys.argv[1],testarry,0,verbose=args.v))