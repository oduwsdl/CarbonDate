import requests
from requests.auth import HTTPBasicAuth
import urllib.parse
import json
import os
import sys
from surt import surt
from requests.utils import quote
import logging

moduleTag='Bing.com'

def getBing(url,outputArray, indexOfOutputArray,verbose=False, **kwargs):
	apiKey = []
	try:
		apiKey_env=os.getenv('CD_Bing_key')
		if apiKey_env is not None:
			logging.debug ( 'cdGetBing: Bing api key detected in environment variable, overwite local config values.')
			apiKey=apiKey_env
		else:
			fileConfig = open(os.path.dirname(__file__)+"/../config", "r")
			config = fileConfig.read()
			fileConfig.close()

			apiKey = json.loads(config)
			apiKey = apiKey['BingAPIKey']
	except:
		logging.debug ( 'cdGetBing: ', sys.exc_info() )
		return ''

	if( len(apiKey) == 0 ):
		logging.info ( 'cdGetBing: apiKey empty' )
		return ''
	elif( apiKey == 'YourBingSearchAPIKey' ):
		logging.info ( 'cdGetBing.py: please set Bing search api key in config' )
		return ''



	api_key = apiKey
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux i686 (x86_64); rv:2.0b4pre) Gecko/20100812 Minefield/4.0b4pre',
		'Ocp-Apim-Subscription-Key':api_key
		}
	base_url = 'https://api.cognitive.microsoft.com/bing/v5.0/search?q='
	parsedUrl = urllib.parse.urlparse(url)
	if( len(parsedUrl.scheme)<1 ):
		url = 'http://'+url
	searchUrl=url[7:]
	converted_url=quote(url,safe='')
	url = base_url + converted_url +'&count=10'
	auth = HTTPBasicAuth(api_key,api_key)

	response = requests.get(url, headers=headers)
	json_result=response.json()
	#print json_result

	result=''
	canonical_search_url=surt(searchUrl)
	for category in json_result:
		if category == 'webPages' :
			for page in json_result[category]['value']:
				result_url=surt(page['displayUrl'])
				if result_url==canonical_search_url :
					result = page['dateLastCrawled']
					break

		elif category == 'images' :
			for page in json_result[category]['value']:
				result_url=surt(page['contentUrl'])
				if result_url==canonical_search_url :
					result = page['datePublished']
					break

		elif category == 'news' :
			for page in json_result[category]['value']:
				result_url=surt(page['url'])
				if result_url==canonical_search_url :
					result = page['datePublished']
					break

		elif category == 'videos' :
			for page in json_result[category]['value']:
				result_url=surt(page['hostPageDisplayUrl'])
				if result_url==canonical_search_url :
					result = page['datePublished']
					break
		if result != '' :
			break

	outputArray[indexOfOutputArray]=result
	kwargs['displayArray'][indexOfOutputArray] = result
	logging.debug ( 'Done Bing' )
	return result

if __name__ == '__main__':
	import sys
	if len(sys.argv)<2:
		print("Usage: %s URL"%sys.argv[0])
		sys.exit(1)
	dummyArray=['']
	print(getBing(sys.argv[1],dummyArray,0,True))