import sys
import os
import calendar
import time
import requests
import logging

moduleTag="Last Modified"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

def getLastModified(url, outputArray, indexOfOutputArray,verbose=False,**kwargs):
	creation_date = ""
	try:
		response=requests.get(url,headers)
		header=response.headers

		lowest_date = 99999999999
		loc = 0


		tag = 'last-modified'

		if(tag in header):
		
			timestamp = header[tag]
			epoch = int(calendar.timegm(time.strptime(timestamp, '%a, %d %b %Y %H:%M:%S %Z')))

			limitEpoch = int(calendar.timegm(time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))

			if(epoch<lowest_date):
				lowest_date = epoch

			creation_date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest_date))
	except Exception as e:
		logging.exception(e)
		outputArray[indexOfOutputArray] = ""
		logging.debug ( "Done Last Modified" )
		return time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(99999999999))
	
	outputArray[indexOfOutputArray] = creation_date
	kwargs['displayArray'][indexOfOutputArray] = creation_date
	logging.debug ( "Done Last Modified" )
	return creation_date