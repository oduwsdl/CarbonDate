import re
import time
import os
import sys, traceback
import datetime
import json
import calendar
import requests
import math

import logging
from datetime import datetime
from .cdGetArchives import getMementos

headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate',
		'Connnection': 'keep-alive',
		'Cache-Control':'max-age=0'	
		}

def getWebpage(url):
	try:
		response = requests.get(url, headers=headers)
		return response
	except:
		return None

def isInPage(url,page):

	page = getWebpage(page)
	if page is None:
		return False,''

	loc = page.text.find(url)
	
	date = ""
	if(loc==-1):
		return False, date

	if "X-Archive-Orig-last-modified" in page.headers:
		date=page.headers["X-Archive-Orig-last-modified"]
	elif 'X-Archive-Orig-date' in page.headers:
		date=page.headers['X-Archive-Orig-date']

	if date != "" :
		epoch = int(calendar.timegm(time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')))
		date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(epoch))
		return True, date
	else:	
		return False, ""

def getFirstAppearance(url, inurl):
	
	try:
		mementos = getMementos(inurl)

		if(len(mementos) == 0):
			return ""
		
		#binary search to find earliest backlink that contain url (early one may not have the back link)
		start = 0
		end = len(mementos)
		previous = -1
		i = 0
		foundbefore = False
		#count = 0

		#binary search for first appearance re-implemented by Neo
		date=""
		while (True):
			res, date = isInPage(url, mementos[int(i)]["link"])
			#special case: only one version of memento bitween other two versions have this reference (the link might be removed from page later)
			if( (res==True and int(math.fabs(previous-i))==1 and foundbefore == False) or (res==False and int(math.fabs(previous-i))==1 and foundbefore == True) ):
				return date

			previous = i

			if res==True:
				#The appearance found, that means the link appeared in the earlier record
				end=i
				i=int((end-start)/2)+start
				foundbefore = False
			else:
				#The appearance didn't found, that means the link appeared in the later record
				start=i
				i=int((end - start)/2)+start
				foundbefore = True

			#The search range has merged together, we get the result
			if end == (start+1):
				return date

	except:

		logging.exception ( sys.exc_info() )
		return ""

