import sys
from bs4 import BeautifulSoup
import datetime
import requests
from cdGetLowest import getLowest
from requests.utils import quote
import logging

moduleTag="Twitter.com"
#this is the establishment time of Twttier, which is the ealiest time of a tweet that can be found
earliest_time=datetime.datetime.strptime("2006-03-01", '%Y-%m-%d')

#pretend we are firefox browser, this ensure we can get right web page
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
#Function: get all tweets in current specific duration
#parameter:
#uri: [string] the link you want to query
#date_from: [datetime] the earliest date of tweets contain this uri
#date_until: [datetime] the latest date of tweets contain this uri
#return: array of  the dates of tweets in this period time
def getDates(uri,date_from,date_until,verbose=False):
	#search patern of the duration specified tweet search
	#https://twitter.com/search?f=tweets&q=[request url]%20since%3A[YYYY-MM-DD]%20until%3A[YYYY-MM-DD]&src=typd
	from_date_str=date_from.strftime("%Y-%m-%d")
	until_date_str=date_until.strftime("%Y-%m-%d")
	search_str='https://twitter.com/search?f=tweets&q={uri}%20since%3A{from_date}%20until%3A{until_date}&src=typd'.format(
		uri = uri, from_date = from_date_str, until_date = until_date_str
		)

	logging.debug ( search_str )
	logging.debug ( 'getTwitter: Search: from %s to %s'%(date_from,date_until) )
	response = requests.get(search_str,headers=headers)
	html = response.text

	soup = BeautifulSoup(html,'lxml')

	#get all tweets and their text in result (not necessary here, debug use only)
	#tweets = soup.find_all('li', 'js-stream-item')

	#get all tweets text in result this is used for get amount fo results
	tweet_text=soup.find_all('p','js-tweet-text')

	#get all timestamp of  tweets
	tweet_timestamps=soup.find_all('a','tweet-timestamp')
	timestamps=[]


	for i in range(0, len(tweet_text)):
		#get  tweets text (no need here)
		#tweet= tweets[i].get_text().encode('ascii', 'ignore')
		#get time of the tweet
		time_stamp = datetime.datetime.fromtimestamp(
			int(tweet_timestamps[i].find('span','js-short-timestamp')['data-time']))
		timestamps.append(time_stamp)
	return timestamps
#get most likely oldest date of tweet that have uri in given time period with bnary search
def getEarliestDate(uri,from_date,until_date,verbose=False):
	midDate=from_date+(until_date-from_date )/2
	upperbound=from_date
	lowerbound=midDate
	result=getDates(uri,from_date,midDate,verbose)
	if len(result)==0:
		upperbound=midDate
		lowerbound=until_date
		result=getDates(uri,midDate,until_date,verbose)
	#check result
	#if still zero return none, indicate that we cannot find tweets
	if len(result)==0:
		return None
	#if there are result (less than 10 or search bound closed to one day), return last one (oldest one)
	if len(result)<=10 or until_date-from_date<datetime.timedelta(days=1):
		return result[-1]
	else:
		#continue binary search
		return getEarliestDate(uri,upperbound,lowerbound,verbose)
#interface function for module
#verbose: enable debug output
def getTwitter(uri,outputArray, indexOfOutputArray,verbose=False,**kwargs):
	if uri.startswith('http://'):
		uri=uri[7:]
	#convert characters in % format
	converted_url=quote(uri,safe='')
	#search original url
	#debug output

	logging.debug ( 'getTwitter: Converted Url is: %s' % converted_url)
	logging.debug ( "getTwitter: Trying %s", converted_url)
	date_str=''
	date=getEarliestDate(converted_url,earliest_time,datetime.datetime.now(),verbose)
	if date is not None:
			date_str=date.strftime('%Y-%m-%dT%H:%M:%S')
	#search url without www prefix (result could be defferent)
	date2_str=''
	url2=''

	if uri.startswith('www.'):
		url2=uri[4:]
		converted_url=quote(url2,safe='')

		logging.debug ( 'getTwitter: Remove www prefix: %s' % converted_url )
		logging.debug ( "getTwitter: Trying %s", converted_url )
		date2=getEarliestDate(converted_url,earliest_time,datetime.datetime.now(),verbose)
		if date2 is not None:
			date2_str=date2.strftime('%Y-%m-%dT%H:%M:%S')
	result_str=''

	result_str=getLowest([date_str,date2_str])
	#debug output
	logging.debug ( "getTwitter: %s\t%s",uri, date_str )
	logging.debug ( "getTwitter: %s\t%s",url2, date2_str)

	outputArray[indexOfOutputArray] = result_str
	kwargs['displayArray'][indexOfOutputArray] = result_str
	logging.debug ( "Done Twitter")
	return result_str
#################test entry####################
if __name__ == '__main__':
	if len(sys.argv)<2:
		print("Unit testing usage: ", sys.argv[0] + " url  e.g: " + sys.argv[0] + " http://www.cs.odu.edu ")
	else:
		testarry=['']
		print(getTwitterCreationDate(sys.argv[1],testarry,0,verbose=True))