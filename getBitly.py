import os
import sys
import datetime
import urllib
import simplejson
import time
import commands
import calendar
import Queue



fileConfig = open("config", "r")
config = fileConfig.read()
fileConfig.close()
json = simplejson.loads(config)

#ACCESS_TOKENs = json["BitlyKeys"] # Api key has been deprecated
ACCESS_TOKENs = json["AccessToken"]


def GetBitlyJson(URL):	

	
	json = ""

	for access_token in ACCESS_TOKENs:
		
		URL = URL.replace("ACCESS_TOKEN", access_token)
		command = 'curl --silent -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" "'+URL+'"'
		
		page = commands.getoutput(command)
		page = page.encode('ascii', 'ignore')
		
		if(page.find('"error": "NOT_FOUND"')!=-1):
			break

		try:

			if( len(page) > 0 ):
				json = simplejson.loads(page)

				if(json['status_code']==403):
					continue
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print exc_type , fname , exc_tb.tb_lineno


		
	return json

def getBitlyCreationDate(url, outputArray, indexOfOutputArray):
	try:
		# Get aggregated url
		
		URL = "https://api-ssl.bitly.com/v3/link/lookup?access_token=ACCESS_TOKEN&url="+url
		json = GetBitlyJson(URL)
		
		if len(json) < 1:
			print "Done Bitly"
			return ""

		if(json['status_code']!=200):
			outputArray[indexOfOutputArray] = "Bitly Key has expired"
			print "Done Bitly"
			return "Bitly Key has expired"

		if(json =="" or ('error' in json['data']['link_lookup'][0]  and json['data']['link_lookup'][0]['error']=='NOT_FOUND')):
			outputArray[indexOfOutputArray] = ""
			print "Done Bitly"
			return ""
		url = json['data']['link_lookup'][0]['aggregate_link']

		# Get creation timestamp
		URL = "https://api-ssl.bitly.com/v3/info?access_token=ACCESS_TOKEN&shortUrl="+url
		json = GetBitlyJson(URL)

		if(json['status_code']!=200):
			outputArray[indexOfOutputArray] = "Bitly Key has expired"
			print "Done Bitly"
			return "Bitly Key has expired"
	
		if(json['data'] == None or 'created_at' not in json['data']['info'][0]):
			outputArray[indexOfOutputArray] = ""
			print "Done Bitly"
			return ""
		epoch = json['data']['info'][0]['created_at']

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
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print exc_type , fname , exc_tb.tb_lineno

		outputArray[indexOfOutputArray] = ""
		print "Done Bitly"
		return ""

