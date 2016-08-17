# CarbonDate

## Prerequisites

* Install cherrypy server (to run server.py)
* Insert your bitly oauth access token in config file. Visit https://bitly.com/a/oauth_apps to get your access token
* Insert your Bing search api key in config file. Visit https://www.microsoft.com/cognitive-services/en-us/bing-web-search-api to get your api key
* (optional) Change server ip/port number in config
* All other packages that generate error "No module named" does exist, must be installed.

## Instructions

To run it as a server:

```
$ python server.py
```
To CarbonDate `http://example.com`:

Open in a Web browser: `http://localhost:8080/cd?url=http://example.com`

To run it as a local script:

```
$ python local.py search URL
```

The backlinks calculation is costy to your computers, so it is recommanded to turn it off:

```
$ python local.py search URL -e cdGetBacklinks
```
## How to add your module:

Copy your scripts and to folder ./modules, then the system will automaticaly detects and loads it.
###If your module have sub-module:

* If the sub-script is in a subfolder,bring folder with your script, carbon tool will ignore subfolders while loading
* If the sub-script is not in a subfolder, after copying it to ./modules folder, add them into config file, under 'SystemUtility' field

##For more help please visit [wiki page](https://github.com/DarkAngelZT/CarbonDate/wiki)

## Support

Fallenangel0813@gmail.com
