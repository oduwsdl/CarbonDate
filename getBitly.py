import os
import sys
import datetime
import urllib
import simplejson
import time
import commands
import calendar

fileConfig = open("config", "r")
config = fileConfig.read()
fileConfig.close()
json = simplejson.loads(config)
ACCESS_TOKENs = json["BitlyKeys"]

def GetBitlyJson(URL):	
	json = ""
	for access_token in ACCESS_TOKENs:
		URL = URL.replace("ACCESS_TOKEN", access_token)
		command = 'curl --silent -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" "'+URL+'"'
		page = commands.getoutput(command)
		page = page.encode('ascii', 'ignore')
		if(page.find('"error": "NOT_FOUND"')!=-1):
			break
		json = simplejson.loads(page)
		if(json['status_code']==403):
			continue
	return json

def getBitlyCreationDate(url):
	try:
		# Get aggregated url
		URL = "https://api-ssl.bitly.com/v3/link/lookup?access_token=ACCESS_TOKEN&url="+url
		json = GetBitlyJson(URL)

		if(json['status_code']!=200):
			return "Bitly Key has expired"

		if(json =="" or ('error' in json['data']['link_lookup'][0]  and json['data']['link_lookup'][0]['error']=='NOT_FOUND')):
			return ""
		url = json['data']['link_lookup'][0]['aggregate_link']

		# Get creation timestamp
		URL = "https://api-ssl.bitly.com/v3/info?access_token=ACCESS_TOKEN&shortUrl="+url
		json = GetBitlyJson(URL)

		if(json['status_code']!=200):
			return "Bitly Key has expired"
	
		if(json['data'] == None or 'created_at' not in json['data']['info'][0]):
			return ""
		epoch = json['data']['info'][0]['created_at']

		limitEpoch = int(calendar.timegm(time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))
		if(epoch<limitEpoch):
			return ""

		creation_date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(epoch))

		return str(creation_date)
	
	except:
		print sys.exc_info()
		return ""

