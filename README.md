# CarbonDate

## Prerequisites

* Install cherrypy server
* Insert your bitly oauth access token in config file. Visit https://bitly.com/a/oauth_apps to get your access token
* Install casperjs and insert location of file in config file
* (optional) Change server ip/port number in config
* All other packages that generate error "No module named" does exist, must be installed, e.g simplejson

## Instructions

To run it as a server:

```
$ python server.py
```
To CarbonDate `http://example.com`:
Open in a Web browser: `http://localhost:8080/cd?url=http://example.com`

To run it as a local script:

```
$ python local.py url
```
