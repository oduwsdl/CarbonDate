import sys
from bs4 import BeautifulSoup
import datetime
import requests
from cdGetLowest import getLowest
from requests.utils import quote

#this is the establishment time of Twttier, which is the ealiest time of a tweet that can be found
earliest_time=datetime.datetime.strptime("2006-03-01", '%Y-%m-%d')

#pretend we are firefox browser, this ensure we can get right web page
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686 (x86_64); rv:2.0b4pre) Gecko/20100812 Minefield/4.0b4pre'}
#Function: get all tweets in current specific duration
#parameter:
#uri: [string] the link you want to query
#date_from: [datetime] the earliest date of tweets contain this uri
#date_until: [datetime] the latest date of tweets contain this uri
#return: array of  the dates of tweets in this period time
def getDates(uri,date_from,date_until):
	#search patern of the duration specified tweet search
	#https://twitter.com/search?f=tweets&q=[request url]%20since%3A[YYYY-MM-DD]%20until%3A[YYYY-MM-DD]&src=typd
	from_date_str=date_from.strftime("%Y-%m-%d")
	until_date_str=date_until.strftime("%Y-%m-%d")
	search_str='https://twitter.com/search?f=tweets&q={uri}%20since%3A{from_date}%20until%3A{until_date}&src=typd'.format(
		uri = uri, from_date = from_date_str, until_date = until_date_str
		)
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
		time_stamp = datetime.datetime.strptime(tweet_timestamps[i]['title'], '%I:%M %p - %d %b %Y')
		timestamps.append(time_stamp)
	return timestamps
#get most likely oldest date of tweet that have uri in given time period with bnary search
def getEarliestDate(uri,from_date,until_date):
	midDate=from_date+(until_date-from_date )/2
	upperbound=from_date
	lowerbound=midDate
	result=getDates(uri,from_date,midDate)
	if len(result)==0:
		upperbound=midDate
		lowerbound=until_date
		result=getDates(uri,midDate,until_date)
	#check result
	#if still zero return none, indicate that we cannot find tweets
	if len(result)==0:
		return None
	#if there are result (less than 10 or search bound closed to one day), return last one (oldest one)
	if len(result)<=10 or from_date==until_date:
		return result[-1]
	else:
		#continue binary search
		return getEarliestDate(uri,upperbound,lowerbound)
#interface function for module
#verbose: enable debug output
def getTwitterCreationDate(uri,outputArray, indexOfOutputArray,verbose=False):
	if uri.startswith('http://'):
		uri=uri[7:]
	#convert characters in % format
	converted_url=quote(uri,safe='')
	#search original url

	date_str=''
	date=getEarliestDate(converted_url,earliest_time,datetime.datetime.now())
	if date is not None:
			date_str=date.strftime('%Y-%m-%dT%H:%M:%S')
	#search url without www prefix (result could be defferent)
	date2_str=''
	url2=''
	if uri.startswith('www.'):
		url2=uri[4:]
		converted_url=quote(url2,safe='')
		date2=getEarliestDate(converted_url,earliest_time,datetime.datetime.now())
		if date2 is not None:
			date2_str=date2.strftime('%Y-%m-%dT%H:%M:%S')
	result_str=''

	result_str=getLowest([date_str,date2_str])
	#debug output
	if verbose:
		print uri, date_str
		print url2, date2_str

	outputArray[indexOfOutputArray] = result_str
	print "Done Twitter"
	return result_str
#################test entry####################
if __name__ == '__main__':
	if len(sys.argv)<2:
		print("Unit testing usage: ", sys.argv[0] + " url  e.g: " + sys.argv[0] + " http://www.cs.odu.edu ")
	else:
		testarry=['']
		print(getTwitterCreationDate(sys.argv[1],testarry,0,verbose=True))