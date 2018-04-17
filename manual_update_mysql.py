import requests
import json
import datetime
import pymysql.cursors
import config
import warnings

#make sure to edit the file "config.py" to include your MySQL database connection information, your Pendo API key, and the time period for which you want to retrive data

def date_ms(date):
	dt = datetime.datetime.strptime(date, '%Y-%m-%d')
	return str(dt.timestamp() * 1000)

def fix(dictionary, first, second):
	for i in range(len(dictionary['results'])):
		if first in dictionary['results'][i]['metadata']:
			if second in dictionary['results'][i]['metadata'][first]:
				pass
			else:
				dictionary['results'][i]['metadata'][first][second] = None
		else:
			dictionary['results'][i]['metadata'][first] = {second: None}

def nice_encode(string):
	if isinstance(string, str):
		return string.encode('utf-8')
	else:
		return string

def nice_convert_timestamp(ts):
	if ts is not None:
		return datetime.datetime.fromtimestamp(ts/1000.0)
	else:
		return ts

def update_lists(connection):
	cursor = connection.cursor()

	#filter out warnings about duplicated keys
	warnings.filterwarnings('ignore', "\(1062.*")

	sources = ["page", "feature", "guide"]

	for source in sources:
		#information for API call
		url = "https://app.pendo.io/api/v1/" + source
		headers = {'x-pendo-integration-key': config.pendo_key, 'content-type': "application/json"}

		response = requests.get(url, headers = headers)
		response_dictionary = json.loads(response.content)

		#insert data
		sql = "INSERT IGNORE INTO `" + source + "s` (`id`, `name`) VALUES (%s,%s)"
		for i in range(len(response_dictionary)):
			cursor.execute(sql,(response_dictionary[i]["id"], response_dictionary[i]["name"]))
		connection.commit()

		print(source, "s written successfully", sep="")

	cursor.close()

def update_accounts(connection):
	cursor = connection.cursor()

	#information for API call
	url = "https://app.pendo.io/api/v1/aggregation"
	headers = {'x-pendo-integration-key': config.pendo_key, 'content-type': "application/json"}
	data = "{\"response\":{\"mimeType\":\"application/json\"},\"request\":{\"pipeline\":[{\"source\":{\"accounts\":null}}]}}"

	response = requests.post(url, data = data, headers = headers)
	response_dictionary = json.loads(response.content)

	for first in ['auto', 'salesforce']:
		if first == 'auto':
			for second in ['firstvisit', 'lastupdated', 'lastvisit']:
				fix(response_dictionary, first, second)
		elif first == 'salesforce':
			for second in ['name', 'id']:
				fix(response_dictionary, first, second)

	#insert data
	sql = "INSERT INTO `accounts` (`accountId`, `accountName`, `firstvisit`, `lastupdated`, `lastvisit`, `salesforceId`) VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `lastupdated` = %s, `lastvisit` = %s"
	for i in range(len(response_dictionary['results'])):
		cursor.execute(sql,(nice_encode(response_dictionary['results'][i]['accountId']), nice_encode(response_dictionary['results'][i]['metadata']['salesforce']['name']), nice_convert_timestamp(response_dictionary['results'][i]['metadata']['auto']['firstvisit']), nice_convert_timestamp(response_dictionary['results'][i]['metadata']['auto']['lastupdated']), nice_convert_timestamp(response_dictionary['results'][i]['metadata']['auto']['lastvisit']), nice_encode(response_dictionary['results'][i]['metadata']['salesforce']['id']), nice_convert_timestamp(response_dictionary['results'][i]['metadata']['auto']['lastupdated']), nice_convert_timestamp(response_dictionary['results'][i]['metadata']['auto']['lastvisit'])))
	connection.commit()

	cursor.close()
	print("accounts written successfully")

def update_visitors(connection):
	cursor = connection.cursor()

	#information for API call
	url = "https://app.pendo.io/api/v1/aggregation"
	headers = {'x-pendo-integration-key': config.pendo_key, 'content-type': "application/json"}
	data = "{\"response\":{\"mimeType\":\"application/json\"},\"request\":{\"pipeline\":[{\"source\":{\"visitors\":null}}]}}"

	response = requests.post(url, data = data, headers = headers)
	response_dictionary = json.loads(response.content)

	for second in ['accountid', 'firstvisit', 'lastbrowsername', 'lastbrowserversion', 'lastoperatingsystem', 'lastservername', 'lastupdated', 'lastuseragent', 'lastvisit']:
		fix(response_dictionary, 'auto', second)

	#insert data
	sql = "INSERT INTO `visitors` (`visitorId`, `accountId`, `firstvisit`, `lastbrowsername`, `lastbrowserversion`, `lastoperatingsystem`, `lastservername`, `lastupdated`, `lastuseragent`, `lastvisit`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `lastbrowsername` = %s, `lastbrowserversion` = %s, `lastoperatingsystem` = %s, `lastservername` = %s, `lastupdated` = %s, `lastuseragent` = %s, `lastvisit` = %s"
	for i in range(len(response_dictionary['results'])):
		cursor.execute(sql,(nice_encode(response_dictionary['results'][i]['visitorId']), nice_encode(response_dictionary['results'][i]['metadata']['auto']['accountid']), nice_convert_timestamp(response_dictionary['results'][i]['metadata']['auto']['firstvisit']), nice_encode(response_dictionary['results'][i]['metadata']['auto']['lastbrowsername']), nice_encode(response_dictionary['results'][i]['metadata']['auto']['lastbrowserversion']), nice_encode(response_dictionary['results'][i]['metadata']['auto']['lastoperatingsystem']), nice_encode(response_dictionary['results'][i]['metadata']['auto']['lastservername']), nice_convert_timestamp(response_dictionary['results'][i]['metadata']['auto']['lastupdated']), nice_encode(response_dictionary['results'][i]['metadata']['auto']['lastuseragent']), nice_convert_timestamp(response_dictionary['results'][i]['metadata']['auto']['lastvisit']), nice_encode(response_dictionary['results'][i]['metadata']['auto']['lastbrowsername']), nice_encode(response_dictionary['results'][i]['metadata']['auto']['lastbrowserversion']), nice_encode(response_dictionary['results'][i]['metadata']['auto']['lastoperatingsystem']), nice_encode(response_dictionary['results'][i]['metadata']['auto']['lastservername']), nice_convert_timestamp(response_dictionary['results'][i]['metadata']['auto']['lastupdated']), nice_encode(response_dictionary['results'][i]['metadata']['auto']['lastuseragent']), nice_convert_timestamp(response_dictionary['results'][i]['metadata']['auto']['lastvisit'])))
	connection.commit()

	cursor.close()
	print("visitors written successfully")

def update_events(connection, first_date, day_count):
	cursor = connection.cursor()

	#information for Pendo API
	url = "https://app.pendo.io/api/v1/aggregation"
	headers = {'x-pendo-integration-key': config.pendo_key, 'content-type': "application/json"}

	sources = ["featureEvents", "guideEvents", "pageEvents", "pollEvents"]

	#pull and write for each source for each day
	for j in range(day_count):
		for source_name in sources:
			data = "{\"response\":{\"mimeType\":\"application/json\"},\"request\":{\"pipeline\":[{\"source\":{\"" + source_name + "\":{\"eventClass\":[\"web\", \"ios\"]},\"timeSeries\":{\"first\":\"" + first_date + "+" + str(j) + "*24*60*60*1000\",\"count\":1,\"period\":\"dayRange\"}}}]}}"

			#retrieve data from Pendo
			response = requests.post(url, data = data, headers = headers)
			response_dictionary = json.loads(response.content)

			#check for error in retrieving data and check if response is empty
			print(source_name, " day ", j + 1, ": ", response, sep="")
			if(response_dictionary['results'] is not None):
				#convert ms timestamps
				if(source_name in ["featureEvents", "pageEvents"]):
					for i in range(len(response_dictionary['results'])):
						response_dictionary['results'][i]['day'] = datetime.datetime.fromtimestamp((response_dictionary['results'][i]['day'])/1000.0)
				elif(source_name in ["guideEvents", "pollEvents"]):
					for i in range(len(response_dictionary['results'])):
						response_dictionary['results'][i]['browserTime'] = datetime.datetime.fromtimestamp((response_dictionary['results'][i]['browserTime'])/1000.0)
				else:
					print("Warning: Timestamps not converted")

				#try to write to the appropriate MySQL table
				try:
					if(source_name == "featureEvents"):
						sql = "INSERT INTO `feature_events` (`accountId`,`visitorId`,`numEvents`,`numMinutes`,`server`,`remoteIp`,`parameters`,`userAgent`,`day`,`appId`,`featureId`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
						for i in range(len(response_dictionary['results'])):
							cursor.execute(sql,(response_dictionary['results'][i]['accountId'],response_dictionary['results'][i]['visitorId'],response_dictionary['results'][i]['numEvents'],response_dictionary['results'][i]['numMinutes'],response_dictionary['results'][i]['server'],response_dictionary['results'][i]['remoteIp'],response_dictionary['results'][i]['parameters'],response_dictionary['results'][i]['userAgent'],response_dictionary['results'][i]['day'],response_dictionary['results'][i]['appId'],response_dictionary['results'][i]['featureId']))
					elif(source_name == "guideEvents"):
						sql = "INSERT INTO `guide_events` (`accountIds`,`browserTime`,`country`,`elementPath`,`eventId`,`type`,`guideId`,`guideStepId`,`latitude`,`loadTime`,`longitude`,`region`,`remoteIp`,`serverName`,`url`,`userAgent`,`visitorId`,`accountId`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
						for i in range(len(response_dictionary['results'])):
							cursor.execute(sql,(response_dictionary['results'][i]['accountIds'],response_dictionary['results'][i]['browserTime'],response_dictionary['results'][i]['country'],response_dictionary['results'][i]['elementPath'],response_dictionary['results'][i]['eventId'],response_dictionary['results'][i]['type'],response_dictionary['results'][i]['guideId'],response_dictionary['results'][i]['guideStepId'],response_dictionary['results'][i]['latitude'],response_dictionary['results'][i]['loadTime'],response_dictionary['results'][i]['longitude'],response_dictionary['results'][i]['region'],response_dictionary['results'][i]['remoteIp'],response_dictionary['results'][i]['serverName'],response_dictionary['results'][i]['url'],response_dictionary['results'][i]['userAgent'],response_dictionary['results'][i]['visitorId'],response_dictionary['results'][i]['accountId']))
					elif(source_name == "pageEvents"):
						sql = "INSERT INTO `page_events` (`accountId`,`visitorId`,`numEvents`,`numMinutes`,`server`,`remoteIp`,`parameters`,`userAgent`,`day`,`appId`,`pageId`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
						for i in range(len(response_dictionary['results'])):
							cursor.execute(sql,(response_dictionary['results'][i]['accountId'],response_dictionary['results'][i]['visitorId'],response_dictionary['results'][i]['numEvents'],response_dictionary['results'][i]['numMinutes'],response_dictionary['results'][i]['server'],response_dictionary['results'][i]['remoteIp'],response_dictionary['results'][i]['parameters'],response_dictionary['results'][i]['userAgent'],response_dictionary['results'][i]['day'],response_dictionary['results'][i]['appId'],response_dictionary['results'][i]['pageId']))
					elif(source_name == "pollEvents"):
						sql = "INSERT INTO `poll_events` (`accountIds`,`browserTime`,`country`,`elementPath`,`eventId`,`type`,`guideId`,`guideStepId`,`latitude`,`loadTime`,`longitude`,`pollId`,`region`,`remoteIp`,`serverName`,`url`,`userAgent`,`visitorId`,`accountId`,`pollResponse`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
						for i in range(len(response_dictionary['results'])):
							cursor.execute(sql,(response_dictionary['results'][i]['accountIds'],response_dictionary['results'][i]['browserTime'],response_dictionary['results'][i]['country'],response_dictionary['results'][i]['elementPath'],response_dictionary['results'][i]['eventId'],response_dictionary['results'][i]['type'],response_dictionary['results'][i]['guideId'],response_dictionary['results'][i]['guideStepId'],response_dictionary['results'][i]['latitude'],response_dictionary['results'][i]['loadTime'],response_dictionary['results'][i]['longitude'],response_dictionary['results'][i]['pollId'],response_dictionary['results'][i]['region'],response_dictionary['results'][i]['remoteIp'],response_dictionary['results'][i]['serverName'],response_dictionary['results'][i]['url'],response_dictionary['results'][i]['userAgent'],response_dictionary['results'][i]['visitorId'],response_dictionary['results'][i]['accountId'],response_dictionary['results'][i]['pollResponse']))
					else:
						print("Error: Source not recognized")
					connection.commit()
					print(source_name, "written successfully")
				except:
					print("Error: Could not write to MySQL table")
			else:
				print("Response is empty")

	cursor.close()

#connect to the MySQL database
connection = pymysql.connect(host=config.host,
                             user=config.user,
                             password=config.password,
                             db=config.database,
                             cursorclass=pymysql.cursors.DictCursor)

#get first date and day count from config file
first_date = date_ms(config.first_date)
day_count = config.day_count

#update pages, features, guides
update_lists(connection)

#update accounts and visitors
update_accounts(connection)
update_visitors(connection)

#update feature, page, poll, and guide events
update_events(connection, first_date, day_count)

#close the connection
connection.close()