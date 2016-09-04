import sys
import os

from cdGetLowest import getLowest
from cdGetBitly import getBitly
from cdGetArchives import getArchives
from cdGetGoogle import getGoogle, mimicBrowser
from cdGetFirstAppearanceInArchives import getFirstAppearance

import commands
import calendar
import time
import urllib
import logging

moduleTag="Backlinks"
entry="getBacklinksFirstAppearanceDates"

reload(sys)  
sys.setdefaultencoding('utf8')

def getBacklinks(url):
	inlinks = []
	url = urllib.quote(url, '')
	try:	
		query = 'https://www.google.com/search?hl=en&tbo=d&tbs=qdr:y15&q=link:'+url+'&oq=link:'+url
		
		#com = 'curl --silent -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" "'+query+'"'
		#page = commands.getoutput(com)
		page = mimicBrowser(query)

		loc = 0	
		#print page
		page=page.replace('<h3 class=r>','<h3 class="r">')
		while(True):
			start_str = '<h3 class="r"><a href="'
			loc = page.find(start_str,loc)

			#print "loc: "
			#print loc			

			if(loc==-1):
				break
			fin = page.find('"', loc+len(start_str)+1)
			url = page[loc+len(start_str):fin]
			inlinks.append(url)
			loc = fin
	except:
		logging.debug ( 'cdGetBacklinks :',sys.exc_info())

	return inlinks

def getBacklinksCreationDates(url):
	links = getBacklinks(url)
	backlinks = []
	outputArrayDummyNotUsed = []
	try:
		for link in links:
			bitly = getBitly(link)
			archives = getArchives(link)
			google = getGoogle(link)
			lowest = getLowest([bitly,google,archives["Earliest"]])
			
			if(lowest==""):
				continue
			backlinks.append(lowest)

	except:
		logging.debug ( 'cdGetBacklinks :', sys.exc_info() )
	return backlinks

def getBacklinksFirstAppearanceDates(url, outputArray, outputArrayIndex,verbose=False, **kwargs):

	links = getBacklinks(url)

	lowest_epoch = 99999999999
	limitEpoch = int(calendar.timegm(time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))
	try:
		for link in links:
			datestamp = getFirstAppearance(url, link)

			if(datestamp==""):
				continue

			epoch = int(calendar.timegm(time.strptime(datestamp, '%Y-%m-%dT%H:%M:%S')))

			if(epoch<limitEpoch):
				continue

			if(epoch<lowest_epoch):
				lowest_epoch = epoch
	except:
		logging.debug ( 'cdGetBacklinks :', sys.exc_info() )

	if(lowest_epoch == 99999999999):
		outputArray[outputArrayIndex] = ""
		logging.debug ( "Done Backlinks*" )
		return ""
	
	timeVal = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest_epoch))
	outputArray[outputArrayIndex] = timeVal
	kwargs['displayArray'][indexOfOutputArray] = timeVal
	logging.debug ( "Done Backlinks" )
	return timeVal

