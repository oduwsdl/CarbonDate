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

## Installation and Setup 

Clone the repository and move into the directory 

```
git clone https://github.com/oduwsdl/CarbonDate
cd CarbonDate 
```

Install python requirements 

```
pip install -r requirements.txt 
```  

### Missing Aysnchronous attribute 

![Example Error](https://github.com/njenn001/CarbonDate/blob/master/images/Error.jpg)

For quick installation and running purposes simply comment out the use of the server import in main.py. 

![Example Solution](https://github.com/njenn001/CarbonDate/blob/master/images/solution.JPG)

### Missing/Broken Modules

* Twitter 
* Bitly 
* Bing 



## Running as a Docker Container

It is recommended to use [Docker](https://www.docker.com/) to install and run this application.

To download the Docker image:

```
$ docker image pull oduwsdl/carbondate
```

Once you have downloaded the image, run it as a server or a local command line program (in one-off mode).

To run it as a server:

```
$ docker container run --rm -it -p 8888:8888 oduwsdl/carbondate ./main.py -s
```

Then access it at http://localhost:8888/.

To run it in one-off mode:

```
$ docker container run --rm -it oduwsdl/carbondate ./main.py -l {URI-R}
```

## Running without Docker

To run it as a server:

```
$ ./main.py -s
```

Then access it at http://localhost:8888/.

To run it in one-off mode:

```
$ ./main.py -l {URI-R}
```

### Running the GUI 


* Initialized in terminal 
```
$ ./main.py --gui 
``` 
* Use the small tkinter window to carbon date URLs

  * ![GUI Figure](https://github.com/njenn001/CarbonDate/blob/master/images/GuiFig.png)

  * Output will lie in the terminal 

### Environment variables

Carbon Date provides the option of passing in environment variables for both the Bing and Bitly services.
For Bitly, the environment key is `CD_Bitly_token`. For Bing, the environment key is `CD_Bing_key`.
Environment variables can be passed into docker using the `-e` or `--env` arguments before executing the Carbon Date application like so:

```
$ docker run -e "CD_Bitly_token=foo" -e "CD_Bing_key=bar" -it --rm oduwsdl/carbondate ./main.py -l http://www.cs.odu.edu/
```

### Disabling modules

CarbonDate provides the option of preventing searching for specified modules.
For example, if a user wants to disable backlinks and google modules the user can add the `-e` argument after a URI-R is specified like so:

```
$ ./main.py -l "https://www.cs.odu.edu/" -e cdGetBacklinks cdGetGoogle
```

A complete list of all the modules a user can disable is as follows:

```
cdGetPubdate
cdGetArchives
cdGetBing
cdGetBitly
cdGetTwitter
cdGetBacklinks
cdGetGoogle
cdGetLastModified
```

## How to add your module

Name your module's main script as `cdGet<ModuleName>.py`. If your module relies on extra code in a different folder you may bring this directory into the modules directory, the CarbonDate library will ignore subfolders while loading modules. If the extra code is not in a subfolder, after copying it to the `./modules` folder, add the file names into the config file under the `SystemUtility` field.

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

### Data returned from your module

The data returned from your module can be a string of date in the following format: `'1995-01-01T12:00:00'` or a dictionary with `earliest` as a mandatory key for a source you define along with any optional keys your module provides.

```
{
    "foo": {
      "earliest": "2017-07-04T15:10:24",
      "optional-fields": "extra stuff"
    }
}
```

If your module gathers multiple sources you can also return these sources in a dictionary but each source must have a key named `earliest`. For example your method can return a dictionary as follows:

```
{
    "foo": {
      "earliest": "2017-07-04T15:10:24"
    },
    "bar": {
      "earliest": "2015-02-01T06:05:30",
      "extra": "stuff"
    }
}
```

Put your result date in to outputArray\[indexOfOutputArray\] for result comparison,  

```
outputArray[outputArrayIndex] = time
```

and put the result and other data you want to show in the "displayArray" like:  

```
kwargs['displayArray'][outputArrayIndex] = dictionary_or_datestring_variable
```

Where the variable outputArray, indexOfOutputArray and displayArray are past in by the system.  
