import json

import spotipy
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from spotipy.oauth2 import SpotifyClientCredentials
import youtube_dl

with open("client_secret_spotify.json") as json_file:
    spotify_credentials = json.load(json_file)

SPOTIFY_CLIENT_ID = spotify_credentials["client_id_spotify"]
SPOTIFY_CLIENT_SECRET = spotify_credentials["client_secret_spotify"]
auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


# Returns the liked Youtube Videos
def get_liked_youtube_videos():
    api_name = "youtube"
    api_version = "v3"
    oauth_key_file = "client_secret_306315169899-d9fj3lvr1jnddrpbtel2nag14u2fa37n.apps.googleusercontent.com.json"
    scopes = "https://www.googleapis.com/auth/youtube"
    flow = InstalledAppFlow.from_client_secrets_file(oauth_key_file, scopes)
    credentials = flow.run_console()
    service = build(api_name, api_version, credentials=credentials)

    request = service.videos().list(
        part="snippet,contentDetails,statistics",
        myRating="like"
    )

    response = request.execute()
    for video in response["items"]:
        url = "https://www.youtube.com/watch?v={}".format(video["id"])
        video = youtube_dl.YoutubeDL({}).extract_info(url, download=False)
        song_name = video["track"]
        artist = video["artist"]
        song_info = {
            "url": url,
            "song_name": song_name,
            "artist": artist,
            "spotify_uri": get_spotify_uri(song_name, artist)
        }
    return song_info


def get_spotify_uri(song_name, artist):
    pass


likedVideos = get_liked_youtube_videos()
print(likedVideos)
