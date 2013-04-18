import bottle
from bottle import route, run, template, response
import json
from ordereddict import OrderedDict

from getTopsy import getTopsyCreationDate
from getBitly import getBitlyCreationDate
from getArchives import getArchivesCreationDate
from getGoogle import getGoogleCreationDate
from getBacklinks import *
from getLowest import getLowest
from getLastModified import getLastModifiedDate

#---------------------------------------------------------------------------------------#
#--------------------------Server Section-----------------------------------------------#
#---------------------------------------------------------------------------------------#


@route("/cd/:url#.+#")
def index(url):
	response.content_type = 'application/json; charset=UTF-8'
	print"\n\n\n\n\n--------------------------------\n--- Getting Creation dates for:\n"+url+"\n\n"

	bitly = getBitlyCreationDate(url)
	print "Done Bitly"
	archives = getArchivesCreationDate(url)
	print "Done Archives"
	topsy = getTopsyCreationDate(url)
	print "Done Topsy"
	google = getGoogleCreationDate(url)
	print "Done Google"
	backlink = getBacklinksFirstAppearanceDates(url)
	print "Done Backlinks"
	lastmodified = getLastModifiedDate(url)
	print "Done Last Modified"
	lowest = getLowest([bitly,topsy,google,backlink,lastmodified,archives["Earliest"]])
	print "Got Lowest"

	result = []
	result.append(("URI", url))
	result.append(("Estimated Creation Date", lowest))
	result.append(("Last Modified", lastmodified))
	result.append(("Bitly.com", bitly))
	result.append(("Topsy.com", topsy))
	result.append(("Backlinks", backlink))
	result.append(("Google.com", google))
	result.append(("Archives", archives))
	values = OrderedDict(result)
	r = json.dumps(values, sort_keys=False, indent=2, separators=(',', ': '))
	print r
	return r
   
bottle.debug(True) 
run(host='128.82.7.232', port=80)
