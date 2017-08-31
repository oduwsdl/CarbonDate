# [CarbonDate](http://carbondate.cs.odu.edu)

[![Build Status](https://travis-ci.org/grantat/CarbonDate.svg?branch=master)](https://travis-ci.org/grantat/CarbonDate)
[![codecov](https://codecov.io/gh/grantat/CarbonDate/branch/master/graph/badge.svg)](https://codecov.io/gh/grantat/CarbonDate)

## Prerequisites
* Python 3 only.
* Running in docker container is strongly recommended.
* Install tornado server (to run server).
* Insert your Bitly OAuth access token in config file. Visit https://bitly.com/a/oauth_apps to get your access token.
* Insert your Bing search api key in config file. Visit https://www.microsoft.com/cognitive-services/en-us/bing-web-search-api to get your api key.
* (optional) Change server ip/port number in config.
* All other packages that generate error "No module named" does exist, must be installed.

### Running as a Docker Container

It is recommended to use [Docker](https://www.docker.com/) to install and run this application.

To download the container with docker use:
```
$ docker pull oduwsdl/carbondate
```

Once you have downloaded the container with docker, you can run it as a server or a local command line program.

To run as a server use:
```
$ docker run --rm -it -p 8888:8888 oduwsdl/carbondate ./main.py -s
```
Then you may open your browser to: `http://localhost:8888/`

To run locally use:
```
$ docker run --rm -it -p 8888:8888 oduwsdl/carbondate ./main.py -l search {URI-R}
```

### Running without Docker:

To run it as a server:

```
$ ./main.py -s
```
Then you may open your browser to: `http://localhost:8888/`

To run it as a local script:

```
$ ./main.py -l search {URI-R}
```

The backlinks calculation is costly to your computers, so it is recommended to turn it off:

```
$ ./main.py -l search {URI-R} -e cdGetBacklinks
```

## How to add your module:

Name your module main script as cdGet\<Module name\>.py

And ensure the entry function is named  
```
get<Module name>(url,outputArray, indexOfOutputArray,verbose=False,**kwargs)  
```
or customize your own entry function name by assigning a string value to 'entry' variable in the beginning of your script.  
For example if your module name is Service, then the script should be named cdGetService, and the interface function should be named:

```
getService (url,outputArray, indexOfOutputArray,verbose=False,**kwargs)  
```

Copy your scripts to the folder ./modules, then the system will automatically detect and load it.

### Data returned from your module:

The data returned from your module should be a string of date in the following format: '1995-01-01T12:00:00'.
If your module gathers multiple sources you can also return these sources in a dictionary but each source must have a key
called `earliest`. For example your method can return a dictionary as follows:

```
{
    "web.archive.org": {
      "uri-m": "http://web.archive.org/web/20170704152832/http://www.cnn.com/2017/07/04/politics/us-officials-meet-north-korea-missile-launch/index.html",
      "memento-datetime": "2017-07-04T15:28:32",
      "memento-pubdate": "2017-07-04T15:10:24",
      "earliest": "2017-07-04T15:10:24"
    },
    "wayback.archive-it.org": {
      "uri-m": "http://wayback.archive-it.org/all/20170704185254/http://www.cnn.com/2017/07/04/politics/us-officials-meet-north-korea-missile-launch/index.html",
      "memento-datetime": "2017-07-04T18:52:54",
      "memento-pubdate": "2017-07-04T15:10:24",
      "earliest": "2017-07-04T15:10:24"
    },
    "archive.is": {
      "uri-m": "http://archive.is/20170704205543/http://www.cnn.com/2017/07/04/politics/us-officials-meet-north-korea-missile-launch/index.html",
      "memento-datetime": "2017-07-04T20:55:43",
      "memento-pubdate": "2017-07-04T20:55:43",
      "earliest": "2017-07-04T20:55:43"
    }
}
```

Put your result date in to outputArray\[indexOfOutputArray\] for result comparison,  

```
outputArray[outputArrayIndex] = time
```

and put the result and other data you want to show in the "displayArray" like:  
```
kwargs['displayArray'][outputArrayIndex] = time_and_other_data_in_array_of_tuples
```

Where the variable outputArray, indexOfOutputArray and displayArray are past in by the system.  

### If your module has a sub-module:

* If the sub-script is in a subfolder, bring the folder with your script, carbon tool will ignore subfolders while loading
* If the sub-script is not in a subfolder, after copying it to the ./modules folder, add them into config file, under 'SystemUtility' field

## For more help please visit the [wiki page](https://github.com/DarkAngelZT/CarbonDate/wiki)
