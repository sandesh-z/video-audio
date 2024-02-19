""" Pull All Youtube Videos from a Playlist """

from googleapiclient.discovery import build
import json
from pprint import PrettyPrinter
from pytube import YouTube
import os

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

def downloadYouTube(videourl, path):

    yt = YouTube(videourl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if not os.path.exists(path):
        os.makedirs(path)
    yt.download(path)

def downloadYouTubeAudio(videourl, path):

    yt = YouTube(videourl)
    video = yt.streams.filter(only_audio=True).first() 
  
    output_file = video.download(output_path=path)

    base, ext = os.path.splitext(output_file) 
    new_file = base + '.mp3'
    os.rename(output_file, new_file) 
    print(yt.title + " has been successfully downloaded.")

if __name__ == '__main__':
    videos = fetch_all_youtube_videos("PLmFh1W9jg-zYFAtD8qe_0XJwQB9nvUAAN")
    pp = PrettyPrinter()
    # pp.pprint(videos)
    urls = []
    for item in videos["items"]:
        video = item['snippet']['resourceId']['videoId']
        urls.append(f"https://www.youtube.com/watch?v={video}")

    # print(urls)
    path = '/home/sg/Beginning/youtube_videos'

    for item in urls:
        try:
            downloadYouTubeAudio(item,path)
        except:
            pass    