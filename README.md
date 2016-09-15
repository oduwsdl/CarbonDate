# CarbonDate

## Prerequisites
* Python 3 only.
* Running in docker container is strongly recommanded.
* Install tornado server (to run server).
* Insert your bitly oauth access token in config file. Visit https://bitly.com/a/oauth_apps to get your access token.
* Insert your Bing search api key in config file. Visit https://www.microsoft.com/cognitive-services/en-us/bing-web-search-api to get your api key.
* (optional) Change server ip/port number in config.
* All other packages that generate error "No module named" does exist, must be installed.

## Instructions

To run it as a server:

```
$ ./main.py -s
```
To CarbonDate `http://example.com`:

Open in a Web browser: `http://localhost:8888/cd?url=http://example.com`

To run it as a local script:

```
$ ./main.py -l search URL
```

The backlinks calculation is costy to your computers, so it is recommanded to turn it off:

```
$ ./main.py -l search URL -e cdGetBacklinks
```
## How to add your module:

Name your module main script as cdGet\<Module name\>.py

And ensure the entry function is named  
```
get<Module name>(url,outputArray, indexOfOutputArray,verbose=False,**kwargs)  
```
or customize your own entry function name by assign string value to 'entry' varable in the beginning of your script  
for example your module name is Service, 

then the script should be named cdGetService, and interface function should be named  
```
getService (url,outputArray, indexOfOutputArray,verbose=False,**kwargs)  
```

Copy your scripts and to folder ./modules, then the system will automaticaly detects and loads it.  
###Data returned from your module:  
The data returned from your module should be a string of date, in the format like '1995-01-01T12:00:00'  
Put your result date in to outputArray\[indexOfOutputArray\] for result comparasion,  
```
outputArray[outputArrayIndex] = time
```
and put the result and other data you want to show in the "displayArray" like:  
```
kwargs['displayArray'][outputArrayIndex] = time_and_other_data_in_array_of_tuples
```
Where the varable outputArray,indexOfOutputArray and displayArray are past in by the system.  


###If your module have sub-module:

* If the sub-script is in a subfolder,bring folder with your script, carbon tool will ignore subfolders while loading
* If the sub-script is not in a subfolder, after copying it to ./modules folder, add them into config file, under 'SystemUtility' field

##For more help please visit [wiki page](https://github.com/DarkAngelZT/CarbonDate/wiki)

## Support

Fallenangel0813@gmail.com
