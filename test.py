#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from unidecode import unidecode


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyB0KMU3GZcwr5D-UqN46ZhlnjQLyNQwi20"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        channelId="UCTv-XvfzLX3i4IGWAm4sbmA",
        part="id,snippet",
        type="video",
        maxResults=options.max_results
    ).execute()

    videos = []
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        title = unidecode(search_result['snippet']['title'])
        videoId = search_result['id']['videoId']
        video_response = youtube.videos().list(
            part='id,snippet,player',
            id=videoId
        ).execute()
        video = video_response.get("items", [])[0]
        thumbs = video['snippet']['thumbnails']
        player = video['player']['embedHtml']

        videos.append("%s (%s) %s %s" % (title, videoId, thumbs, player))
    print "Videos:\n", "\n".join(videos), "\n"


if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=50)
    args = argparser.parse_args()

    try:
        youtube_search(args)
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
