import json

def searchTerm(searchWord ,jsonFile):
	with open('data.txt') as json_file:
		data = json.load(json_file)
		try:
			return data[searchWord]
		except:
			return[]

