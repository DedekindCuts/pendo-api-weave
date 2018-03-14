import requests
import json
import datetime
import config
import csv

#information for API call
url = "https://app.pendo.io/api/v1/page"
headers = {
    'x-pendo-integration-key': config.pendo_key,
    'content-type': "application/json"
}

response = requests.get(url, headers = headers)
response_dictionary = json.loads(response.content)
with open('pages.csv', 'w') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(["page", "name"])
	for i in range(len(response_dictionary)):
		writer.writerow([response_dictionary[i]["id"], response_dictionary[i]["name"]])