import sys
import os
import traceback
import calendar
import time
import commands
from cdGetLowest import getLowest
from random import randint

cdGetGoogle::randSleep(),
def randSleep():
	sleepSeconds = randint(2, 7)
	print 'cdGetGoogle::randSleep(), sleep:', sleepSeconds
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

def genericGetCreationDate(query):

	allDatesEpoch = []
	try:
		userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30'
		#userAgent = 'Carbon Date test service to estimate creation date of a website. http://cd.cs.odu.edu/'
		page = commands.getoutput('curl --silent -L -A "'+userAgent+'" "'+query+'"')

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
		print '\tERROR:', errorMessage

	#print query
	#for date in allDatesEpoch:
	#	print date
	#print
	return getLowestDate(allDatesEpoch)

def getGoogleCreationDate(url, outputArray, indexOfOutputArray):
	
	#Caution google blocks bots which do not play nice
	#return ''
	randSleep()
	query = 'https://www.google.com/search?hl=en&tbo=d&tbs=qdr:y15&q=inurl:'+url+'&oq=inurl:'+url
	inurl_creation_date = genericGetCreationDate(query)

	randSleep()
	query = 'https://www.google.com/search?hl=en&tbo=d&tbs=qdr:y15&q='+url
	search_creation_date = genericGetCreationDate(query)

	#print 'inurl_creation_date:', inurl_creation_date
	#print 'search_creation_date:', search_creation_date

	lowerDate = ''
	if( inurl_creation_date != 0 and search_creation_date != 0 ):

		lowerDate = getLowest([search_creation_date, inurl_creation_date])
		outputArray[indexOfOutputArray] = lowerDate

	elif( inurl_creation_date == 0 and search_creation_date != 0 ):

		lowerDate = getLowest([search_creation_date, search_creation_date])
		outputArray[indexOfOutputArray] = lowerDate

	else:
		#this else means: inurl_creation_date != 0 and search_creation_date = 0
		lowerDate = getLowest([inurl_creation_date, inurl_creation_date])
		outputArray[indexOfOutputArray] = lowerDate
	
	return lowerDate