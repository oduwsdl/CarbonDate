# CarbonDate

## Prerequisites

* Python 2.6+
* Install cherrypy server
* Insert your bitly oauth access token in config file. Visit https://bitly.com/a/oauth_apps to get your access token
* Install casperjs and insert location of file in config file
* (optional) Change server ip/port number in config
* The following python modules are required:

    ```
	json
	ordereddict
	re
	htmlMessages
	pprint
	threading
	Queue
	datetime
	os
	sys
	traceback
	urllib
	time
	commands
	calendar
	urllib2
	math
	logging
	simplejson
	```

## Instructions

There are 3 ways to use the application:

* **Through the website cd.cs.odu.edu:** Given that carbon dating is highly computationally intensive, the site should be used just for a small tests as a courtesy to other users. If you have the need to carbon date a large number of URLs, you should install the application locally (local.py or server.py)

* **Through the local server (server.py)**:

	```
	$ python server.py
	```
    
	To CarbonDate `http://www.example.com`:

	Open in a Web browser: `http://localhost:8080/cd?url=http://www.example.com`

* **Through the local application (local.py):**

	To run it as a local script (backlinks module off)-

	```
	$ python local.py http://www.example.com
	```

	To run it as a local script (backlinks module on)-

	```
	$ python local.py http://www.example.com 1
	```
