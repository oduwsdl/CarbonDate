import os
import sys
import datetime
import urllib.request, urllib.parse, urllib.error
import json
import time
import subprocess
import calendar
import json
import os.path
import logging

moduleTag="Bitly.com"

def GetBitlyJson(URL):	

	ACCESS_TOKENs = []
	try:
		access_token_env=os.getenv('CD_Bitly_token')
		if access_token_env is not None:
			logging.warning ( 'cdGetBitly: Access token is found in environment variable, overwite local config values.' )
			ACCESS_TOKENs=[access_token_env]
		else:
			fileConfig = open(os.path.dirname(__file__)+"/../config", "r")
			config = fileConfig.read()
			fileConfig.close()

			ACCESS_TOKENs = json.loads(config)
			ACCESS_TOKENs = ACCESS_TOKENs['AccessToken']
	except:
		logging.exception ( 'cdGetBitly: %s', sys.exc_info() )
		return ''

	if( len(ACCESS_TOKENs) == 0 ):
		logging.warning ( 'cdGetBitly.py::GetBitlyJson(), ACCESS_TOKENs empty' )
		return ''
	elif( ACCESS_TOKENs[0] == 'YourBitlyAccessTokenHere' ):
		logging.warning ( 'cdGetBitly.py::GetBitlyJson(), please set bitly access token in config' )
		return ''
	
	jsonData = ""
	for access_token in ACCESS_TOKENs:
		
		URL = URL.replace("ACCESS_TOKEN", access_token)
		command = 'curl --silent -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" "'+URL+'"'
		
		page = subprocess.getoutput(command)
		page = page.encode('ascii', 'ignore')
		
		if(page.find(b'"error": "NOT_FOUND"')!=-1):
			break

		jsonData = json.loads(page.decode())

		if(jsonData['status_code']==403):
			continue
	return jsonData

def getBitly(url, outputArray, indexOfOutputArray,verbose=False,**kwargs):
	try:
		
		# Get aggregated url
		
		URL = "https://api-ssl.bitly.com/v3/link/lookup?access_token=ACCESS_TOKEN&url="+url
		jsonData = GetBitlyJson(URL)
		
		if len(jsonData) < 1:
			return ""

		if(jsonData['status_code']!=200):
			outputArray[indexOfOutputArray] = "Bitly Key has expired"
			kwargs['displayArray'][indexOfOutputArray] = ""
			logging.debug ( "Done Bitly" )
			return "Bitly Key has expired"

		if(jsonData =="" or ('error' in jsonData['data']['link_lookup'][0]  and jsonData['data']['link_lookup'][0]['error']=='NOT_FOUND')):
			outputArray[indexOfOutputArray] = ""
			kwargs['displayArray'][indexOfOutputArray] = ""
			logging.debug ( "Done Bitly" )
			return ""
		url = jsonData['data']['link_lookup'][0]['aggregate_link']

		# Get creation timestamp
		URL = "https://api-ssl.bitly.com/v3/info?access_token=ACCESS_TOKEN&shortUrl="+url
		jsonData = GetBitlyJson(URL)

		if(jsonData['status_code']!=200):
			outputArray[indexOfOutputArray] = "Bitly Key has expired"
			kwargs['displayArray'][indexOfOutputArray] = ""
			logging.debug ( "Done Bitly" )
			return "Bitly Key has expired"
	
		if(jsonData['data'] == None or 'created_at' not in jsonData['data']['info'][0]):
			outputArray[indexOfOutputArray] = ""
			kwargs['displayArray'][indexOfOutputArray] = ""
			logging.debug ( "Done Bitly" )
			return ""
		epoch = jsonData['data']['info'][0]['created_at']

		limitEpoch = int(calendar.timegm(time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))
		if(epoch<limitEpoch):
			outputArray[indexOfOutputArray] = ""
			kwargs['displayArray'][indexOfOutputArray] = ""
			logging.debug ( "Done Bitly" )
			return ""
		
	
		creation_date = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(epoch))


		
		outputArray[indexOfOutputArray] = creation_date
		kwargs['displayArray'][indexOfOutputArray] = creation_date
		logging.debug ( "Done Bitly" )
		return str(creation_date)
	
	except:
		logging.exception('cdGetBitly: %s', sys.exc_info())
		outputArray[indexOfOutputArray] = ""
		kwargs['displayArray'][indexOfOutputArray] = ""
		logging.debug("Done Bitly")
		return ""

