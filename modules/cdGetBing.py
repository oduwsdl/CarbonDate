import requests
from requests.auth import HTTPBasicAuth
import urlparse
import json
import os
from surt import surt

moduleTag='Bing.com'

def getBing(url,outputArray, indexOfOutputArray,verbose=False):
	apiKey = []
	try:
		apiKey_env=os.getenv('CD_Bing_key')
		if apiKey_env is not None:
			print 'cdGetBing: Bing api key detected in environment variable, overwite local config values.'
			apiKey=apiKey[apiKey_env]
		else:
			fileConfig = open(os.path.dirname(__file__)+"/../config", "r")
			config = fileConfig.read()
			fileConfig.close()

			apiKey = json.loads(config)
			apiKey = apiKey['BingAPIKey']
	except:
		print 'cdGetBing: ', sys.exc_info()
		return ''

	if( len(apiKey) == 0 ):
		print 'cdGetBing: apiKey empty'
		return ''
	elif( apiKey == 'YourBingSearchAPIKey' ):
		print 'cdGetBing.py: please set Bing search api key in config'
		return ''



	api_key = apiKey
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux i686 (x86_64); rv:2.0b4pre) Gecko/20100812 Minefield/4.0b4pre',
		'Ocp-Apim-Subscription-Key':api_key
		}
	base_url = 'https://api.cognitive.microsoft.com/bing/v5.0/search?q='
	parsedUrl = urlparse.urlparse(url)
	if( len(parsedUrl.scheme)<1 ):
		url = 'http://'+url
	searchUrl=url[7:]
	url = base_url + url +'&responseFilter=webpages'
	auth = HTTPBasicAuth(api_key,api_key)

	response = requests.get(url, headers=headers)
	json_result=response.json()

	result=''
	canonical_search_url=surt(searchUrl)
	for page in json_result['webPages']['value']:
		result_url=surt(page['displayUrl'])
		if result_url==canonical_search_url :
			result = page['dateLastCrawled']
			break
	outputArray[indexOfOutputArray]=result
	print 'Done Bing'
	return result

if __name__ == '__main__':
	import sys
	if len(sys.argv)<2:
		print "Usage: %s URL"%sys.argv[0]
		sys.exit(1)
	dummyArray=['']
	print(getBing(sys.argv[1],dummyArray,0,True))