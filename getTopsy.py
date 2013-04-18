import urllib
import simplejson
import copy
import sys
import datetime
import time
import commands
import calendar

fileConfig = open("config", "r")
config = fileConfig.read()
fileConfig.close()
json = simplejson.loads(config)
APIKey = json["TopsyKey"]

def checkKey(url):
	page = commands.getoutput('curl --silent -I -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" "'+url+'"')
	if(page.find("Warning: Expired key")==-1):
		return True
	else:
		return False		

def getTopsyCreationDate(long_url):
	try:
		keyValid = checkKey("http://otter.topsy.com/trackbacks.json?&perpage=100&page=1&url="+long_url+"&apikey="+APIKey)
		if(keyValid==False):
			return "Topsy Key has expired"	

		jsonAll = {}
		temp = []
		for page in range(1,6):
			try:
				url = "http://otter.topsy.com/trackbacks.json?&perpage=100&page="+str(page)+"&url="+long_url+"&apikey="+APIKey
				page = commands.getoutput('curl --silent -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" "'+url+'"')
				json = simplejson.loads(page)
				if(json):
					jsonAll = copy.deepcopy(json)

				newlist = json["response"]["list"]
				temp.extend(newlist)
				jsonAll["response"]["list"] = temp
			except :
				print sys.exc_info()
				pass
		all_tweets = temp
		if(len(all_tweets)==0):
			return ""
		lowest_date = 99999999999
		for tweet in all_tweets:
			date = int(tweet["date"])
			
			limitEpoch = int(calendar.timegm(time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))
			if(date<limitEpoch):
				continue

			if(date<lowest_date):
				lowest_date = date

		creation_date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest_date))
		return creation_date

	except:
		print sys.exc_info()
		return ""
