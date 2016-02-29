import os
import sys
import datetime
import urllib
import json
import time
import commands
import calendar
import Queue


#fileConfig = open("config", "r")
#config = fileConfig.read()
#fileConfig.close()
#json = simplejson.loads(config)

#ACCESS_TOKENs = json["BitlyKeys"] # Api key has been deprecated
#ACCESS_TOKENs = json["AccessToken"]
ACCESS_TOKENs = ['9aa9e4e418f1203595fa0b6a5d585b4d960c7d80']

def GetBitlyJson(URL):	

	
	jsonData = ""

	for access_token in ACCESS_TOKENs:
		
		URL = URL.replace("ACCESS_TOKEN", access_token)
		command = 'curl --silent -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" "'+URL+'"'
		
		page = commands.getoutput(command)
		page = page.encode('ascii', 'ignore')
		
		if(page.find('"error": "NOT_FOUND"')!=-1):
			break

		jsonData = json.loads(page)

		if(jsonData['status_code']==403):
			continue
	return jsonData

def getBitlyCreationDate(url, outputArray, indexOfOutputArray):
	try:
		
		# Get aggregated url
		
		URL = "https://api-ssl.bitly.com/v3/link/lookup?access_token=ACCESS_TOKEN&url="+url
		jsonData = GetBitlyJson(URL)
		
		if len(jsonData) < 1:
			return ""

		if(jsonData['status_code']!=200):
			outputArray[indexOfOutputArray] = "Bitly Key has expired"
			print "Done Bitly"
			return "Bitly Key has expired"

		if(jsonData =="" or ('error' in jsonData['data']['link_lookup'][0]  and jsonData['data']['link_lookup'][0]['error']=='NOT_FOUND')):
			outputArray[indexOfOutputArray] = ""
			print "Done Bitly"
			return ""
		url = jsonData['data']['link_lookup'][0]['aggregate_link']

		# Get creation timestamp
		URL = "https://api-ssl.bitly.com/v3/info?access_token=ACCESS_TOKEN&shortUrl="+url
		jsonData = GetBitlyJson(URL)

		if(jsonData['status_code']!=200):
			outputArray[indexOfOutputArray] = "Bitly Key has expired"
			print "Done Bitly"
			return "Bitly Key has expired"
	
		if(jsonData['data'] == None or 'created_at' not in jsonData['data']['info'][0]):
			outputArray[indexOfOutputArray] = ""
			print "Done Bitly"
			return ""
		epoch = jsonData['data']['info'][0]['created_at']

		limitEpoch = int(calendar.timegm(time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))
		if(epoch<limitEpoch):
			outputArray[indexOfOutputArray] = ""
			print "Done Bitly"
			return ""
		
	
		creation_date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(epoch))


		
		outputArray[indexOfOutputArray] = creation_date
		print "Done Bitly"
		return str(creation_date)
	
	except:
		print sys.exc_info()
		outputArray[indexOfOutputArray] = ""
		print "Done Bitly"
		return ""

