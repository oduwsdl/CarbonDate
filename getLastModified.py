import sys, traceback
import os
import calendar
import time
import commands

def getLastModifiedDate(url, outputArray, indexOfOutputArray):
	creation_date = ""
	try:
		header = commands.getoutput('curl --silent -L -I -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" "'+url+'"')
		header = header.lower()

		lowest_date = 99999999999
		loc = 0

		while(True):

			start_str = 'last-modified: '
			loc = header.find(start_str,loc)
			fin = header.find("\r", loc)

			if(loc==-1):
				break
			
			timestamp = header[loc+len(start_str):fin]
			epoch = int(calendar.timegm(time.strptime(timestamp, '%a, %d %b %Y %H:%M:%S %Z')))

			limitEpoch = int(calendar.timegm(time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))

			#caused infinite loop
			#if(epoch<limitEpoch):
			#	continue

			if(epoch<lowest_date):
				lowest_date = epoch

			creation_date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest_date))
			loc = fin
	except:
		print "Date format does not match predefined format, resetting to default value"
		#print traceback.print_exception(sys.exc_type, sys.exc_value, sys.exc_traceback,limit=2,file=sys.stdout)
		#print sys.exc_info()
		outputArray[indexOfOutputArray] = ""
		print "Done Last Modified"
		return time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(99999999999))
	
	outputArray[indexOfOutputArray] = creation_date
	print "Done Last Modified"
	return creation_date