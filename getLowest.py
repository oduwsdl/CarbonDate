
import calendar
import time

def getLowest(dates):
	lowest_epoch = 99999999999
	for date in dates:
		if(date== "" or date=="Topsy Key has expired" or date=="Bitly Key has expired"):
			continue
		epoch = int(calendar.timegm(time.strptime(date, '%Y-%m-%dT%H:%M:%S')))

		limitEpoch = int(calendar.timegm(time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')))
		if(epoch<limitEpoch):
			continue

		if(epoch<lowest_epoch):
			lowest_epoch = epoch

	if(lowest_epoch == 99999999999):
		return ""
	return time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(lowest_epoch))

