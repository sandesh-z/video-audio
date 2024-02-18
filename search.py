from googleapiclient.discovery import build
import json

#retrive api key from file
api_key=""
with open("/home/sg/Beginning/video_api_key.json") as jsonFile:
    data = json.load(jsonFile)
api_key= data["key"]
print(api_key)

#build youtube obj for searching with googleapiclient
youtube = build('youtube','v3',developerKey = api_key)
print(type(youtube))

#search with query param 'paradygm'
request = youtube.search().list(q='paradygm',part='snippet',type='playlist',maxResults=2)
print(type(request))
res = request.execute()

#print result
from pprint import PrettyPrinter
pp = PrettyPrinter()
pp.pprint(res)

