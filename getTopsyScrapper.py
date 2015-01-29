import commands
import sys
import time
import calendar

import logging
import os
import json



try:
	fileConfig = open("config", "r")
	config = fileConfig.read()
	fileConfig.close()
	json = json.loads(config)

	CasperJsLocation = json["CasperJSLocation"]

	if( len(CasperJsLocation) < 1):
		print "CasperJsLocation not set"
		sys.exit(0)
except:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print "check config file location/format"
	print exc_type , fname , exc_tb.tb_lineno
	sys.exit(0)



def extract(A, B, strt, page):
	extracted = ""

	loc = page.find(A, strt)
	if(loc==-1):
		return extracted, False, -1
	loc2 = page.find(B, loc)
	if(loc2==-1):
		return extracted, False, -1

	extracted = page[loc+len(A):loc2]
	return extracted, True, loc2

def getTopsyCreationDate(URL, outputArray, indexOfOutputArray):
	try:

	
		allpages = ""
		offset = 0

		while(True):

			URL = "http://topsy.com/trackback?url="+URL+"&perpage=100&offset="+str(offset)
			#print "casperjs topsy.js '"+URL+"'"

			page = commands.getoutput(str(CasperJsLocation) + " topsy.js '"+URL+"'")
			#print page
			#print page
			#print "\n\n\n\n\n--------------------------------------------------------\n\n"
			#print page
			if(page.find('No results found')!=-1):
				break
			allpages = allpages + page	
			offset = offset + 100	
			
			

			#for debug
			#if(offset>500):
			#	print page
			#	break

		page = allpages	
		

		loc = 0
		hasTopsys = False
		lowest_date = 99999999999

		while(loc!=-1):
			extracted, found, loc = extract('<div class="result-tweet">', '</ul></div></div></div>', loc, page)
			if(found==False):
				break
			tweet, found, l = extract('<div>', '</div>', 0, extracted)

			found = True
			while(found):
				tag, found, l = extract('<a', '>', 0, tweet)
				tag = '<a'+tag+'>'
				tweet = tweet.replace(tag,'')
			tweet = tweet.replace('</a>','')
			tweet = tweet.replace(',', ';')
			tweetLink, found, l = extract('<ul class="inline"><li><small><a href="', '" class="muted">', 0, extracted)
			tweetTime, found, l = extract('data-timestamp="', '">', 0, extracted)
		

			date = int(tweetTime)
			limitEpoch = int(calendar.timegm(time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))
			if(date<limitEpoch):
				continue

			if(date<lowest_date):
				lowest_date = date

		
		creation_date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest_date))
		
		outputArray[indexOfOutputArray] = creation_date
		print "Done Topsy"
		return creation_date
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print exc_type , fname , exc_tb.tb_lineno

	print "Done Topsy"
	return

