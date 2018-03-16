import requests
import json
import datetime
import config
import csv

#make sure to edit the file "config.py" to include your Pendo API key and the time period for which you want to retrieve data

#information for Pendo API
url = "https://app.pendo.io/api/v1/aggregation"
headers = {
    'x-pendo-integration-key': config.pendo_key,
    'content-type': "application/json"
}

def date_ms(date):
	dt = datetime.datetime.strptime(date, '%Y-%m-%d')
	return str(dt.timestamp() * 1000)

sources = ["featureEvents", "guideEvents", "pageEvents", "pollEvents"]
first_date = date_ms(config.first_date)
day_count = config.day_count

#pull and write for each source for day_count days, starting at first_date
for j in range(day_count):
	for source_name in sources:
		data = "{\"response\":{\"mimeType\":\"application/json\"},\"request\":{\"pipeline\":[{\"source\":{\"" + source_name + "\":null,\"timeSeries\":{\"first\":\"" + first_date + "+" + str(j) + "*24*60*60*1000\",\"count\":1,\"period\":\"dayRange\"}}}]}}"

		#retrieve data from Pendo
		response = requests.post(url, data = data, headers = headers)
		response_dictionary = json.loads(response.content)

		#check for error in retrieving data and check if response is empty
		print(source_name, "day", j + 1, response)
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

			#try to write to the appropriate csv file
			try:
				if(source_name == "featureEvents"):
					with open('feature_events.csv', 'a') as csvfile:
						writer = csv.writer(csvfile)
						for i in range(len(response_dictionary['results'])):
							writer.writerow([response_dictionary['results'][i]['accountId'],response_dictionary['results'][i]['visitorId'],response_dictionary['results'][i]['numEvents'],response_dictionary['results'][i]['numMinutes'],response_dictionary['results'][i]['server'],response_dictionary['results'][i]['remoteIp'],response_dictionary['results'][i]['parameters'],response_dictionary['results'][i]['userAgent'],response_dictionary['results'][i]['day'],response_dictionary['results'][i]['appId'],response_dictionary['results'][i]['featureId']])
				elif(source_name == "guideEvents"):
					with open('guide_events.csv', 'a') as csvfile:
						writer = csv.writer(csvfile)
						for i in range(len(response_dictionary['results'])):
							writer.writerow([response_dictionary['results'][i]['accountIds'],response_dictionary['results'][i]['browserTime'],response_dictionary['results'][i]['country'],response_dictionary['results'][i]['elementPath'],response_dictionary['results'][i]['eventId'],response_dictionary['results'][i]['type'],response_dictionary['results'][i]['guideId'],response_dictionary['results'][i]['guideStepId'],response_dictionary['results'][i]['latitude'],response_dictionary['results'][i]['loadTime'],response_dictionary['results'][i]['longitude'],response_dictionary['results'][i]['region'],response_dictionary['results'][i]['remoteIp'],response_dictionary['results'][i]['serverName'],response_dictionary['results'][i]['url'],response_dictionary['results'][i]['userAgent'],response_dictionary['results'][i]['visitorId'],response_dictionary['results'][i]['accountId']])
				elif(source_name == "pageEvents"):
					with open('page_events.csv', 'a') as csvfile:
						writer = csv.writer(csvfile)
						for i in range(len(response_dictionary['results'])):
							writer.writerow([response_dictionary['results'][i]['accountId'],response_dictionary['results'][i]['visitorId'],response_dictionary['results'][i]['numEvents'],response_dictionary['results'][i]['numMinutes'],response_dictionary['results'][i]['server'],response_dictionary['results'][i]['remoteIp'],response_dictionary['results'][i]['parameters'],response_dictionary['results'][i]['userAgent'],response_dictionary['results'][i]['day'],response_dictionary['results'][i]['appId'],response_dictionary['results'][i]['pageId']])
				elif(source_name == "pollEvents"):
					with open('poll_events.csv', 'a') as csvfile:
						writer = csv.writer(csvfile)
						for i in range(len(response_dictionary['results'])):
							writer.writerow([response_dictionary['results'][i]['accountIds'],response_dictionary['results'][i]['browserTime'],response_dictionary['results'][i]['country'],response_dictionary['results'][i]['elementPath'],response_dictionary['results'][i]['eventId'],response_dictionary['results'][i]['type'],response_dictionary['results'][i]['guideId'],response_dictionary['results'][i]['guideStepId'],response_dictionary['results'][i]['latitude'],response_dictionary['results'][i]['loadTime'],response_dictionary['results'][i]['longitude'],response_dictionary['results'][i]['pollId'],response_dictionary['results'][i]['region'],response_dictionary['results'][i]['remoteIp'],response_dictionary['results'][i]['serverName'],response_dictionary['results'][i]['url'],response_dictionary['results'][i]['userAgent'],response_dictionary['results'][i]['visitorId'],response_dictionary['results'][i]['accountId'],response_dictionary['results'][i]['pollResponse']])
				else:
					print("Error: Source not recognized")
				print(source_name, "written successfully")
			except:
				print("Error: Could not write to spreadsheet")
		else:
			print("Response is empty")