from datetime import datetime
import json
import os

def getSettings():
	settings = {
		'updated_at': str(datetime.now()),
		'feed_at_hour': None,
		'feed_at_minute': None,
		'enabled': False,
	}

	if os.path.exists('settings.json'):
		with open('settings.json', 'r') as file:
		    settings = json.load(file)

	return settings


def updateSettings(newSettings):
	newSettings['updated_at'] = str(datetime.now())
	with open("settings.json", 'w') as file:
	    json.dump(newSettings, file, indent=4)


def updateFeedingTime(feedAtHour, feedAtMinute):
	settings = getSettings()
	settings['feed_at_hour'] = feedAtHour
	settings['feed_at_minute'] = feedAtMinute
	settings['last_fed_date'] = None
	updateSettings(settings)


def toggleEnabled():
	settings = getSettings()
	isEnabled = settings['enabled']
	settings['enabled'] = not isEnabled
	updateSettings(settings)


def wasFedToday():
	settings = getSettings()
	return settings['last_fed_date'] == datetime.now().date()


def updateLastFedDate():
	settings = getSettings()
	settings['last_fed_date'] = datetime.now().date()
	updateSettings(settings)


def clearLastFedDate():
	settings = getSettings()
	settings['last_fed_date'] = None
	updateSettings(settings)

	    