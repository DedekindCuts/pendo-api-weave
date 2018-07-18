import requests
import json
import datetime
import pymysql.cursors
import config
import warnings

#make sure to edit the file "config.py" to include your MySQL database connection information and your Pendo API key

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
	elif string is None:
		return ""
	else:
		return string

def nice_convert_timestamp(ts):
	if ts is not None:
		return datetime.datetime.fromtimestamp(ts/1000.0)
	else:
		return ts

def first_date(connection, source):
	cursor = connection.cursor()
	if source in ("feature", "page"):
		sql = "SELECT DATE_ADD(DATE(MAX(`day`)), INTERVAL 1 DAY) AS `start_date` FROM " + source + "_events"
	elif source in ("guide", "poll"):
		sql = "SELECT DATE_ADD(DATE(MAX(`browserTime`)), INTERVAL 1 DAY) AS `start_date` FROM " + source + "_events"
	else:
		print("Source not recognized")
	cursor.execute(sql)
	cursor.close()
	return cursor.fetchone()['start_date']

def day_count(first_date):
	return (datetime.date.today() - first_date).days

def update_lists(connection, source):
	cursor = connection.cursor()

	#filter out warnings about duplicated keys
	warnings.filterwarnings('ignore', "\(1062.*")

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

def update_events(connection, source_name):
	cursor = connection.cursor()

	#information for Pendo API
	url = "https://app.pendo.io/api/v1/aggregation"
	headers = {'x-pendo-integration-key': config.pendo_key, 'content-type': "application/json"}

	#pull and write for each source for each day
	#get first_date and day_count by checking most recent dates in MySQL database
	first = first_date(connection, source_name)
	days = day_count(first)
	first = date_ms(str(first))
	for j in range(days):
		data = "{\"response\":{\"mimeType\":\"application/json\"},\"request\":{\"pipeline\":[{\"source\":{\"" + source_name + "Events\":{\"eventClass\":[\"web\", \"ios\"]},\"timeSeries\":{\"first\":\"" + first + "+" + str(j) + "*24*60*60*1000\",\"count\":1,\"period\":\"dayRange\"}}}]}}"

		#retrieve data from Pendo
		response = requests.post(url, data = data, headers = headers)
		response_dictionary = json.loads(response.content)

		#check for error in retrieving data and check if response is empty
		print(source_name, " events day ", j + 1, ": ", response, sep="")
		if(response_dictionary['results'] is not None):
			#convert ms timestamps
			if(source_name in ["feature", "page"]):
				for i in range(len(response_dictionary['results'])):
					response_dictionary['results'][i]['day'] = datetime.datetime.fromtimestamp((response_dictionary['results'][i]['day'])/1000.0)
			elif(source_name in ["guide", "poll"]):
				for i in range(len(response_dictionary['results'])):
					response_dictionary['results'][i]['browserTime'] = datetime.datetime.fromtimestamp((response_dictionary['results'][i]['browserTime'])/1000.0)
			else:
				print("Warning: Timestamps not converted")

			#try to write to the appropriate MySQL table
			try:
				if(source_name == "feature"):
					sql = "INSERT INTO `feature_events` (`accountId`,`visitorId`,`numEvents`,`numMinutes`,`server`,`remoteIp`,`parameters`,`userAgent`,`day`,`appId`,`featureId`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
					for i in range(len(response_dictionary['results'])):
						cursor.execute(sql,(response_dictionary['results'][i]['accountId'],response_dictionary['results'][i]['visitorId'],response_dictionary['results'][i]['numEvents'],response_dictionary['results'][i]['numMinutes'],response_dictionary['results'][i]['server'],response_dictionary['results'][i]['remoteIp'],response_dictionary['results'][i]['parameters'],response_dictionary['results'][i]['userAgent'],response_dictionary['results'][i]['day'],response_dictionary['results'][i]['appId'],response_dictionary['results'][i]['featureId']))
				elif(source_name == "guide"):
					sql = "INSERT INTO `guide_events` (`accountIds`,`browserTime`,`country`,`elementPath`,`eventId`,`type`,`guideId`,`guideStepId`,`latitude`,`loadTime`,`longitude`,`region`,`remoteIp`,`serverName`,`url`,`userAgent`,`visitorId`,`accountId`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
					for i in range(len(response_dictionary['results'])):
						cursor.execute(sql,(response_dictionary['results'][i]['accountIds'],response_dictionary['results'][i]['browserTime'],response_dictionary['results'][i]['country'],response_dictionary['results'][i]['elementPath'],response_dictionary['results'][i]['eventId'],response_dictionary['results'][i]['type'],response_dictionary['results'][i]['guideId'],response_dictionary['results'][i]['guideStepId'],response_dictionary['results'][i]['latitude'],response_dictionary['results'][i]['loadTime'],response_dictionary['results'][i]['longitude'],response_dictionary['results'][i]['region'],response_dictionary['results'][i]['remoteIp'],response_dictionary['results'][i]['serverName'],response_dictionary['results'][i]['url'],response_dictionary['results'][i]['userAgent'],response_dictionary['results'][i]['visitorId'],response_dictionary['results'][i]['accountId']))
				elif(source_name == "page"):
					sql = "INSERT INTO `page_events` (`accountId`,`visitorId`,`numEvents`,`numMinutes`,`server`,`remoteIp`,`parameters`,`userAgent`,`day`,`appId`,`pageId`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
					for i in range(len(response_dictionary['results'])):
						cursor.execute(sql,(response_dictionary['results'][i]['accountId'],response_dictionary['results'][i]['visitorId'],response_dictionary['results'][i]['numEvents'],response_dictionary['results'][i]['numMinutes'],response_dictionary['results'][i]['server'],response_dictionary['results'][i]['remoteIp'],response_dictionary['results'][i]['parameters'],response_dictionary['results'][i]['userAgent'],response_dictionary['results'][i]['day'],response_dictionary['results'][i]['appId'],response_dictionary['results'][i]['pageId']))
				elif(source_name == "poll"):
					sql = "INSERT INTO `poll_events` (`accountIds`,`browserTime`,`country`,`elementPath`,`eventId`,`type`,`guideId`,`guideStepId`,`latitude`,`loadTime`,`longitude`,`pollId`,`region`,`remoteIp`,`serverName`,`url`,`userAgent`,`visitorId`,`accountId`,`pollResponse`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
					for i in range(len(response_dictionary['results'])):
						cursor.execute(sql,(response_dictionary['results'][i]['accountIds'],response_dictionary['results'][i]['browserTime'],response_dictionary['results'][i]['country'],response_dictionary['results'][i]['elementPath'],response_dictionary['results'][i]['eventId'],response_dictionary['results'][i]['type'],response_dictionary['results'][i]['guideId'],response_dictionary['results'][i]['guideStepId'],response_dictionary['results'][i]['latitude'],response_dictionary['results'][i]['loadTime'],response_dictionary['results'][i]['longitude'],response_dictionary['results'][i]['pollId'],response_dictionary['results'][i]['region'],response_dictionary['results'][i]['remoteIp'],response_dictionary['results'][i]['serverName'],response_dictionary['results'][i]['url'],response_dictionary['results'][i]['userAgent'],response_dictionary['results'][i]['visitorId'],response_dictionary['results'][i]['accountId'],response_dictionary['results'][i]['pollResponse']))
				else:
					print("Error: Source not recognized")
				connection.commit()
				print(source_name, "s written successfully", sep="")
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

#update pages, features, guides
sources = ["page", "feature", "guide"]
for source in sources:
	update_lists(connection, source)

#update accounts and visitors
update_accounts(connection)
update_visitors(connection)

#update feature, page, poll, and guide events
sources = ["feature", "guide", "page", "poll"]
for source in sources:
	update_events(connection, source)

#close the connection
connection.close()