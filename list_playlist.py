""" Pull All Youtube Videos from a Playlist """

from googleapiclient.discovery import build
import json
from pprint import PrettyPrinter

api_key=""
with open("/home/sg/Beginning/video_api_key.json") as jsonFile:
    data = json.load(jsonFile)
api_key= data["key"]

DEVELOPER_KEY = api_key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def fetch_all_youtube_videos(playlistId):
    """
    Fetches a playlist of videos from youtube
    We splice the results together in no particular order

    Parameters:
        parm1 - (string) playlistId
    Returns:
        playListItem Dict
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    res = youtube.playlistItems().list(
    part="snippet",
    playlistId=playlistId,
    maxResults="50"
    ).execute()

    nextPageToken = res.get('nextPageToken')
    while ('nextPageToken' in res):
        nextPage = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlistId,
        maxResults="50",
        pageToken=nextPageToken
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    return res

if __name__ == '__main__':
    videos = fetch_all_youtube_videos("PLmFh1W9jg-zYFAtD8qe_0XJwQB9nvUAAN")
    pp = PrettyPrinter()
    pp.pprint(videos)
    urls = []
    for item in videos["items"]:
        video = item['snippet']['resourceId']['videoId']
        urls.append(f"https://www.youtube.com/watch?v={video}")

    print(urls)