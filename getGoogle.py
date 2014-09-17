import sys
import os
import calendar
import time
import commands
from getLowest import getLowest

	

def getGoogleCreationDate(url, outputArray, indexOfOutputArray):
	inurl_creation_date = ""
	try:
		query = 'https://www.google.com/search?hl=en&tbo=d&tbs=qdr:y15&q=inurl:'+url+'&oq=inurl:'+url
		page = commands.getoutput('curl --silent -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" "'+query+'"')

		
		
		signatureString = ' - </span>'
		locationOfSignature = 0
		lowest_date = 99999999999
		while(True):
			

			

			#retrieve date from preceding " - </span>" signature - start
			#this logic is meant to retrieve date from a string of form: ">DateIsHere- </span>"
			locationOfSignature = page.find(signatureString, locationOfSignature)
			locationOfSignature
			timestamp = ''
			
			
			if locationOfSignature != -1:
				k = locationOfSignature
				while 1==1 and k > -1:
					#end marker
    					if page[k] != '>' :
						timestamp = page[k] + timestamp
					else :
						break
					k = k - 1;
				locationOfSignature = locationOfSignature + len(signatureString)
				
				timestamp = timestamp.strip()
			else :
				break
			#retrieve date from preceding " - </span>" signature - end
			
			#print ""
			#print "timestamp: " + timestamp


			epoch = int(calendar.timegm(time.strptime(timestamp, '%b %d, %Y')))
		

			limitEpoch = int(calendar.timegm(time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))
			if(epoch<limitEpoch):
				continue
			
			if(epoch<lowest_date):
				lowest_date = epoch
			inurl_creation_date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest_date))
			
	except:
		pass

	search_creation_date = ""
	try:
		query = 'https://www.google.com/search?hl=en&tbo=d&tbs=qdr:y15&q='+url
		page = commands.getoutput('curl --silent -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" "'+query+'"')

		
		signatureString = ' - </span>'
		locationOfSignature = 0
		lowest_date = 99999999999
		while(True):

			
			
			#firstaid, not permanent fix
			#retrieve date from preceding " - </span>" signature - start
			#this logic is meant to retrieve date from a string of form: ">DateIsHere- </span>"
			locationOfSignature = page.find(signatureString, locationOfSignature)
			timestamp = ''
			
			
			if locationOfSignature != -1:
				k = locationOfSignature
				while 1==1 and k > -1:
    					if page[k] != '>' :
						timestamp = page[k] + timestamp
					else :
						break
					k = k - 1;
				locationOfSignature = locationOfSignature + len(signatureString)

				timestamp = timestamp.strip()
			else :
				break
			#retrieve date from preceding " - </span>" signature - end
			
			#print ""
			#print "timestamp: " + timestamp
			
			epoch = int(calendar.timegm(time.strptime(timestamp, '%b %d, %Y')))

			limitEpoch = int(calendar.timegm(time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))
			if(epoch<limitEpoch):
				continue

			if(epoch<lowest_date):
				lowest_date = epoch
			search_creation_date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest_date))
			
	except:
		pass
	
	lowerDate = getLowest([search_creation_date,inurl_creation_date])
	outputArray[indexOfOutputArray] = lowerDate
	print "Done Google"
	return lowerDate
	

