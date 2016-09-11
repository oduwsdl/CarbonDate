import sys
import os
import traceback
import calendar
import time
import requests
from .cdGetLowest import getLowest
from random import randint
import logging

moduleTag='Google.com'

def randSleep():
	sleepSeconds = randint(2, 7)
	logging.debug ( 'cdGetGoogle::randSleep(), sleep: %s', sleepSeconds )
	time.sleep(sleepSeconds)

def getLowestDate(allDatesEpoch):

	if( len(allDatesEpoch) == 0 ):
		return 0

	lowest_date = 99999999999
	
	for epoch in allDatesEpoch:
		#epoch = int(calendar.timegm(time.strptime(timestamp, '%b %d, %Y')))
		limitEpoch = int(calendar.timegm(time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))
		if(epoch<limitEpoch):
			continue

		if(epoch<lowest_date):
			lowest_date = epoch

	inurl_creation_date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest_date))
	return inurl_creation_date

def getTimestampFromSERP(signatureString, locationOfSignature, page):

	#retrieve date from preceding " - </span>" signature - start
	if( len(page) == 0 or len(signatureString) == 0 ):
		return '', -1

	timestamp = ''

	k = locationOfSignature
	while 1==1 and k > -1:
		#end marker
		if page[k] != '>' :
			timestamp = page[k] + timestamp
		else :
			break
		k = k - 1;
	#shift search cursor
	locationOfSignature = locationOfSignature + len(signatureString)
	timestamp = timestamp.strip()
	
	return timestamp, locationOfSignature
	#retrieve date from preceding " - </span>" signature - end

def mimicBrowser(query):
	
	try:
		headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:38.0) Gecko/20100101 Firefox/38.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate',
		'Connnection': 'keep-alive',
		'Cache-Control':'max-age=0'	
		}

		response = requests.get(query, headers=headers)
		return response.text
	except:

		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		errorMessage = fname + ', ' + str(exc_tb.tb_lineno)  + ', ' + str(sys.exc_info())
		logging.error ( '\tERROR:', errorMessage )
		logging.error ( '\tquery is: ', query )
		return ''

def genericGetCreationDate(query):

	randSleep()

	allDatesEpoch = []
	page = ''
	try:
		#userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30'
		#userAgent = 'Carbon Date test service to estimate creation date of a website. http://cd.cs.odu.edu/'
		#page = commands.getoutput('curl --silent -L -A "'+userAgent+'" "'+query+'"')

		page = mimicBrowser(query)
		
		debugOutfile = open('output.html', 'w')
		debugOutfile.write(str(page))
		debugOutfile.close()

		signatureString = ' - </span>'
		locationOfSignature = 0

		while(True):
		
			#this logic is meant to retrieve date from a string of form: ">DateIsHere- </span>"
			locationOfSignature = page.find(signatureString, locationOfSignature)
			timestamp = ''
			
			if locationOfSignature == -1:
				break
			else:
				timestamp, locationOfSignature = getTimestampFromSERP(signatureString, locationOfSignature, page)
				#print 'timestamp/locationOfSignature:', timestamp

				try:
					epoch = int(calendar.timegm(time.strptime(timestamp, '%b %d, %Y')))
					allDatesEpoch.append(epoch)
				except:
					pass
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		errorMessage = fname + ', ' + str(exc_tb.tb_lineno)  + ', ' + str(sys.exc_info())
		logging.error ( '\tERROR:', errorMessage)

	#print query
	#for date in allDatesEpoch:
	#	print date
	#print
	return getLowestDate(allDatesEpoch)

def getGoogle(url, outputArray, indexOfOutputArray,verbose=False, **kwargs):
	
	#Caution google blocks bots which do not play nice
	#return ''
	query = 'https://www.google.com/search?hl=en&tbo=d&tbs=qdr:y15&q=inurl:'+url+'&oq=inurl:'+url
	inurl_creation_date = genericGetCreationDate(query)

	#query = 'https://www.google.com/search?hl=en&tbo=d&tbs=qdr:y15&q='+url
	#search_creation_date = genericGetCreationDate(query)
	search_creation_date = 0

	#print 'inurl_creation_date:', inurl_creation_date
	#print 'search_creation_date:', search_creation_date

	lowerDate = ''
	if( inurl_creation_date != 0 and search_creation_date != 0 ):

		lowerDate = getLowest([search_creation_date, inurl_creation_date])
		outputArray[indexOfOutputArray] = lowerDate
		kwargs['displayArray'][indexOfOutputArray] = lowerDate

	elif( inurl_creation_date == 0 and search_creation_date != 0 ):

		lowerDate = getLowest([search_creation_date, search_creation_date])
		outputArray[indexOfOutputArray] = lowerDate
		kwargs['displayArray'][indexOfOutputArray] = lowerDate

	elif( inurl_creation_date != 0 and search_creation_date == 0 ):
		
		lowerDate = getLowest([inurl_creation_date, inurl_creation_date])
		outputArray[indexOfOutputArray] = lowerDate
		kwargs['displayArray'][indexOfOutputArray] = lowerDate
	
	return lowerDate