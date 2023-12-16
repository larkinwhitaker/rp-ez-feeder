from datetime import datetime
from settings import getSettings, updateFeedingTime, toggleEnabled, wasFedToday, updateLastFedDate
import json

settings = getSettings()
print (settings)

toggleEnabled()
updateFeedingTime(10,0)

settings = getSettings()
print (json.dumps(settings))

# https://www.geeksforgeeks.org/python-program-to-print-current-hour-minute-second-and-microsecond/

isTimeToFeed = datetime.now().hour == settings['feed_at_hour'] and datetime.now().minute == settings['feed_at_minute']

if not wasFedToday() and isTimeToFeed and settings.enabled:
	print ('now feeding')
	updateLastFedDate()
else :
	print ('NOT feeding')