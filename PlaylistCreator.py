import bz2

import spotipy
import youtube_dl
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from spotipy.oauth2 import SpotifyOAuth
import spotifycredentials


# Cuts a string from the start of a '(' symbol
def preprocess_song_name(song_name: str):
    song_name.lower()
    if song_name.__contains__("("):
        begin = song_name.index("(")
        song_name = song_name[0:begin]
    return song_name


class PlaylistCreator:

    def __init__(self):
        self.SPOTIFY_CLIENT_ID = spotifycredentials.client_id_spotify
        self.SPOTIFY_CLIENT_SECRET = spotifycredentials.client_secret_spotify
        self.SPOTIFY_USER_ID = spotifycredentials.user_id
        self.REDIRECT_URI = spotifycredentials.redirect_uri

        # Insert your youtube oauth file here.
        self.OAUTH_KEY_FILE = "client_secret.json"
        playlistjson = open("playlist.json")
        self.PLAYLIST = json.load(playlistjson)
        scope = 'playlist-modify-private'

        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.SPOTIFY_CLIENT_ID,
                                                                 client_secret=self.SPOTIFY_CLIENT_SECRET,
                                                                 scope=scope,
                                                                 redirect_uri=self.REDIRECT_URI,
                                                                 username=self.SPOTIFY_USER_ID))
        self.song_info = {}
        self.assign_song_infos()
        print(self.song_info)

    # Returns general song infos about all liked Youtube Videos
    def assign_song_infos(self):
        api_name = "youtube"
        api_version = "v3"
        oauth_key_file = self.OAUTH_KEY_FILE
        scopes = "https://www.googleapis.com/auth/youtube"
        flow = InstalledAppFlow.from_client_secrets_file(oauth_key_file, scopes)
        credentials = flow.run_console()
        service = build(api_name, api_version, credentials=credentials)

        request = service.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like",
            maxResults=100
        )
        response = request.execute()

        youtube_dl.utils.std_headers['User-Agent'] = "facebookexternalhit/1.1 (" \
                                                     "+http://www.facebook.com/externalhit_uatext.php) "
        for video in response["items"]:
            url = video["id"]
            info = youtube_dl.YoutubeDL({}).extract_info(url, download=False)
            song_name = info["track"]
            artist = info["artist"]

            if not song_name:
                song_name = preprocess_song_name(info["title"])

            self.song_info[song_name] = {
                "url": url,
                "song_name": song_name,
                "artist": artist,
                "spotify_uri": self.get_spotify_uri(song_name)
            }

    # Returns the spotify URI of the searched song.
    def get_spotify_uri(self, song_name, artist=None):
        if artist:
            q = "track:{} artist:{}".format(song_name, artist)
        else:
            q = song_name

        result = self.spotify.search(q=q, type="track", offset=0, limit=20)
        songs = result['tracks']['items']

        if not songs:
            return []
        else:
            return songs[0]['uri']

    # Creates a private playlist 'Youtube liked songs' and returns the id
    def create_playlist(self):
        description = "This is a playlist with all my liked songs on Youtube."
        response = self.spotify.user_playlist_create(user=self.SPOTIFY_USER_ID, public=False,
                                                     name="Youtube liked Songs",
                                                     description=description)
        pl: str = "playlist.json"
        playlist = open(pl, "w")
        playlist.write(json.dumps({"playlist_id": response['id']}))
        playlist = open(pl, "r")
        self.PLAYLIST = json.load(playlist)
        return response['id']

    # Adds the liked songs to the playlist.
    def add_songs_to_playlist(self):
        if not self.PLAYLIST['playlist_id']:
            self.create_playlist()
        playlist_id = self.PLAYLIST['playlist_id']
        print(playlist_id)

        # Add the songs to the playlist
        tracklist: list = []
        for key in self.song_info.keys():
            track: str = self.song_info[key]['spotify_uri']
            track = track[14:]
            tracklist.append(track)

        self.spotify.playlist_add_items(playlist_id=playlist_id, items=tracklist)
