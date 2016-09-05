import re
import time
import urllib.request, urllib.error, urllib.parse
import os
import sys, traceback
import datetime
import urllib.request, urllib.parse, urllib.error
import json
import calendar
import subprocess
import math

import logging
from datetime import datetime
from .cdGetArchives import getMementos
from .cdGetGoogle import mimicBrowser

'''
#ongoing refactoring
def getMementos(uri):

    uri = uri.replace(' ', '')
    orginalExpression = re.compile( r"<http://[A-Za-z0-9.:=/%-_ ]*>; rel=\"original\"," )


    mementoExpression = re.compile( r"<http://[A-Za-z0-9.:=/&,%-_ \?]*>;rel=\"(memento|first memento|last memento|first memento last memento|first last memento)\";datetime=\"(Sat|Sun|Mon|Tue|Wed|Thu|Fri), \d{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (19|20)\d\d \d\d:\d\d:\d\d GMT\"" )

   

    zeroMementoExpression = re.compile(r"Resource: http://[A-Za-z0-9.:=/&,%-_ ]*")
    #old, new on next: baseURI = 'http://mementoproxy.cs.odu.edu/aggr/timemap/link/'

    #baseURI = 'http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/'
    #OR
    baseURI = 'http://mementoweb.org/timemap/link/'


    memento_list = []

    try:


	search_results = urllib.urlopen(baseURI+uri)
	
	the_page = search_results.read()
        timemapList = the_page.split('\n')

	
        count = 0

	
        for line in timemapList:
           

            if count <= 1:
                if line.find('Resource not in archive') > -1:
                    result = zeroMementoExpression.search( line )
                count = count + 1
                continue
            elif count == 2:
                result = orginalExpression.search( line )
                if result:
                     originalResult = result.group(0)
                     originalUri = originalResult[1:len(originalResult)-17]

            else:

		if(line.find("</memento")>0):
			line = line.replace("</memento", "<http://api.wayback.archive.org/memento")

		loc = line.find('>;rel="')
	       	#tofind = ';datetime="'
		tofind = '; datetime="'
	        loc2 = line.find(tofind)

		

		if(loc!=-1 and loc2!=-1):

                    mementoURL = line[2:loc]
		    timestamp = line[loc2+len(tofind):line.find('"',loc2+len(tofind)+3)]

		  

		    epoch = int(calendar.timegm(time.strptime(timestamp, '%a, %d %b %Y %H:%M:%S %Z')))

		 
		    day_string = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(epoch))

		   
                    uri = mementoURL
         
                    cdlib = 'webarchives.cdlib.org'
                    archiefweb = 'enterprise.archiefweb.eu'
                    webARchive= 'api.wayback.archive.org'
                    yahoo1 = 'uk.wrs.yahoo.com'
                    yahoo2 = 'rds.yahoo.com'
                    yahoo3 = 'wrs.yahoo.com'
                    diigo = 'www.diigo.com'
                    bing = 'cc.bingj.com'
                    wayback = 'wayback.archive-it.org'
                    webArchiveNationalUK = 'webarchive.nationalarchives.gov.uk'
                    webHarvest = 'webharvest.gov'
                    webArchiveOrgUK = 'www.webarchive.org.uk'
                    webCitation = 'webcitation.org'
                    mementoWayBack='memento.waybackmachine.org'
                    type = ''
                    category = ''
                    # @type uri str
                    if (uri.find(webARchive)!=-1):
                        type = 'Internet Archive'
                        category = 'IA'
                    elif (uri.find(yahoo1)!=-1 or uri.find(yahoo2)!=-1 or uri.find(yahoo3)!=-1):
                        type = 'Yahoo'
                        category = 'SE'
                    elif (uri.find(diigo)!=-1):
                        type = 'diigo'
                        category = 'Others'
                    elif (uri.find(bing)!=-1):
                        type = 'Bing'
                        category = 'SE'
                    elif (uri.find(wayback)!=-1):
                        type = 'Archive-It'
                        category = 'Others'
                    elif (uri.find(webArchiveNationalUK)!=-1):
                        type = 'UK National Archive'
                        category = 'Others'
                    elif (uri.find(webHarvest)!=-1):
                        type = 'Web Harvest'
                        category = 'Others'
                    elif (uri.find(webArchiveOrgUK)!=-1):
                        type = 'UK Web Archive'
                        category = 'Others'
                    elif (uri.find(webCitation)!=-1):
                        type = 'Web Citation'
                        category = 'Others'
                    elif (uri.find(cdlib)!=-1):
                        type = 'CD Lib'
                        category = 'Others'
                    elif (uri.find(archiefweb)!=-1):
                        type = 'ArchiefWeb'
                        category = 'Others'
                    elif (uri.find(mementoWayBack)!=-1):
                        type = 'Wayback Machine'
                        category = 'Others'
                    else:
                        type = 'Not Known'
                        category = 'Others'
                
                    memento = {}
                    memento["type"] = type
                    memento["category"] = category
                    memento["time"] = day_string
                    memento["link"] = mementoURL
		    memento["link"] = urllib.quote(memento["link"])
		    memento["link"] = memento["link"].replace("http%3A//", "http://")
		    memento["link"] = memento["link"][memento["link"].find("http://"):]
            
		 
                    memento_list.append(memento)
		   
		else:
			pass

            count = count + 1
	    
    
    except urllib2.URLError:
        pass

    return memento_list
'''

def isInPage(url,page):

	#co = 'curl -i --silent -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" "'+page+'"'
	#page = commands.getoutput(co)

	page = mimicBrowser(page)

	#url = url.decode().encode('utf-8')
	loc = page.find(url)
	
	date = ""
	if(loc==-1):
		return False, date

	#"l not L": to_find = "X-Archive-Orig-Last-modified: "
	to_find = "X-Archive-Orig-last-modified: "

	loc = page.find(to_find)

	#this 2 blocks eventhough not if else are mutually exclusive since if loc!=-1, date will be
	#assigned a value thus precluding the subsequent if from running.
	if(loc !=-1):

		end = page.find("\r", loc)
		date = page[loc+len(to_find):end]
		date = date.strip()

	if(date ==""):	
		
		#"d not D": to_find = "X-Archive-Orig-Date: "
		to_find = 'X-Archive-Orig-date: '

	
		loc = page.find(to_find)
		
		if(loc !=-1):
			end = page.find("\r", loc)
			date = page[loc+len(to_find):end]
			date = date.strip()


	if date != "" :
		epoch = int(calendar.timegm(time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')))
		date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(epoch))
		return True, date
	else:	
		return False, ""

def getFirstAppearance_inprogress(url, inurl):
	print('remove from cdGetArchives import getMementos after implementation')
	payloadJson = ''
	try:
		co = 'curl --silent http://memgator.cs.odu.edu:1208/timemap/json/' + '"' + inurl + '"'
		jsonPage = subprocess.getoutput(co)
		payloadJson = json.loads( [str(jsonPage)] )

		if( 'memento' in payloadJson[0] ):
			if( 'list' in payloadJson[0]['mementos'] ):

				for memento in payloadJson[0]['mementos']['list']:
					res, date = isInPage(url, memento["uri"])
					if(res == True):
						return date

		return ''
	except Exception as e:
		print(str(e))
		print(sys.exc_info()[0], sys.exc_info()[1] , sys.exc_info()[2])
		return ''

def getFirstAppearance(url, inurl):
	
	try:
		mementos = getMementos(inurl)

		if(len(mementos) == 0):
			return ""
		
		#start = 0
		#end = len(mementos)
		#previous = -1
		#i = 0
		#foundbefore = False
		#count = 0

		'''
		for mem in mementos:

			res, date = isInPage(url,mem["link"])
			if(res==True):
				break

		while(True):
			res, date = isInPage(url,mementos[i]["link"])

			if(res==True and i==0):
				return date
			if(int(math.fabs(previous-i))==0):
				return ""

			if( (res==True and int(math.fabs(previous-i))==1 and foundbefore == False) or (res==False and int(math.fabs(previous-i))==1 and foundbefore == True) ):
				return date

			previous = i
			if(res == False):
				start = i
				i = (end-start)/2 + start
				foundbefore = False

			else:
				end = i
				i = (end-start)/2 + start
				foundbefore = True
		
			count = count + 1
		'''

		#experimental block to see first appearance - start
		for mem in mementos:
			#is url in this page (mem["link"])
			res, date = isInPage(url, mem["link"])
			if(res==True):
				return date

		return ""
		#experimental block to see first appearance - end

	except:
		#investigate: when run in cherry framework, exception thrown here
		logging.debug ( sys.exc_info() )
		#print traceback.print_exception(sys.exc_type, sys.exc_value, sys.exc_traceback,limit=2, file=sys.stdout)
		return ""

