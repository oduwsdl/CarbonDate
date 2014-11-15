import sys
import os
from getLowest import getLowest
from getTopsyScrapper import getTopsyCreationDate
from getBitly import getBitlyCreationDate
from getArchives import getArchivesCreationDate
from getGoogle import getGoogleCreationDate
from getFirstAppearanceInArchives import getFirstAppearance, getFirstAppearanceForThread
import commands
import calendar
import time
import urllib

from threading import Thread

def getBacklinks(url):
	inlinks = []
	url = urllib.quote(url, '')
	try:	
		query = 'https://www.google.com/search?hl=en&tbo=d&tbs=qdr:y15&q=link:'+url+'&oq=link:'+url
		com = 'curl --silent -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" "'+query+'"'
		
		page = commands.getoutput(com)

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
		print sys.exc_info()

	return inlinks

def getBacklinksCreationDates(url):
	links = getBacklinks(url)
	backlinks = []
	outputArrayDummyNotUsed = []
	try:
		for link in links:
			bitly = getBitlyCreationDate(link)
			archives = getArchivesCreationDate(link)
			topsy = getTopsyCreationDate(link, outputArrayDummyNotUsed, 0)
			google = getGoogleCreationDate(link)
			lowest = getLowest([bitly,topsy,google,archives["Earliest"]])
			
			if(lowest==""):
				continue
			backlinks.append(lowest)

	except:
		print sys.exc_info()
	return backlinks

def getLowestDateInList(listOfDates):

	datestamp = ''
	lowest_epoch = 99999999999
	limitEpoch = int(calendar.timegm(time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))

	if( len(listOfDates) > 0 ):

		for datestamp in listOfDates:

			if(datestamp==''):
					continue

			epoch = int(calendar.timegm(time.strptime(datestamp, '%Y-%m-%dT%H:%M:%S')))

			if(epoch<limitEpoch):
				continue

			if(epoch<lowest_epoch):
				lowest_epoch = epoch

		return lowest_epoch

#spawns numberOfThreadsToSpawn targetFunction threads passing each argumentsListOfList argument 
def spawnThreads(numberOfThreadsToSpawn, argumentsListOfList):

	if( numberOfThreadsToSpawn > 0 and numberOfThreadsToSpawn == len(argumentsListOfList) ):

		threads = []

		for i in range(0, numberOfThreadsToSpawn):

			#args: url, inurl, outputArray[0]
			threads.append(Thread(target=getFirstAppearanceForThread, args=(argumentsListOfList[i], argumentsListOfList[i][1], argumentsListOfList[i][2])))

		for t in threads :
			t.start()

		# Wait for all threads to complete
		for t in threads:
			t.join()

def getBacklinksFirstAppearanceDatesForThread(url):

	links = getBacklinks(url)
	numberOfThreadsToSpawn = len(links)

	print "links: ", len(links)


	argumentsListOfList = []

	#listOfArguments: <resultHere, url, inurl>
	#argumentsListOfList:
	#< <resultHere, url, inurl>,
	#  <resultHere, url, inurl>,
	#	...
	# <resultHere, url, inurl>>
	

	#build arguments list
	count = 0
	for link in links:
		count = count + 1
		listOfArguments = []
		listOfArguments.append(str(count))
		listOfArguments.append(url)
		listOfArguments.append(link)
		argumentsListOfList.append(listOfArguments)


	spawnThreads(numberOfThreadsToSpawn, argumentsListOfList)

	listOfDates = []
	print ""
	for date in argumentsListOfList:
		listOfDates.append(date[0])

	return listOfDates

def getBacklinksFirstAppearanceDates_old(url, outputArray, outputArrayIndex):

	lowest_epoch = 99999999999
	try:

		listOfDates = getBacklinksFirstAppearanceDatesForThread(url)
		lowest_epoch = getLowestDateInList(listOfDates)
	except:
		print sys.exc_info()

	if(lowest_epoch == 99999999999):
		outputArray[outputArrayIndex] = ''
		print 'Done Backlinks'
		return ''
	
	timeVal = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest_epoch))
	outputArray[outputArrayIndex] = timeVal
	print 'Done Backlinks'
	return timeVal

def getBacklinksFirstAppearanceDates(url, outputArray, outputArrayIndex):
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
		print sys.exc_info()

	if(lowest_epoch == 99999999999):
		outputArray[outputArrayIndex] = ""
		print "Done Backlinks"
		return ""
	
	timeVal = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest_epoch))
	outputArray[outputArrayIndex] = timeVal
	print "Done Backlinks"
	return timeVal


