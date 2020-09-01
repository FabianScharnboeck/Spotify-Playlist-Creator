
import spotipy
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotifycredentials
import youtube_dl


class PlaylistCreator:

    def __init__(self):
        self.SPOTIFY_CLIENT_ID = spotifycredentials.client_id_spotify
        self.SPOTIFY_CLIENT_SECRET = spotifycredentials.client_secret_spotify
        self.SPOTIFY_USER_ID = spotifycredentials.user_id
        self.REDIRECT_URI = spotifycredentials.redirect_uri
        self.OAUTH_KEY_FILE = "client_secret_306315169899-d9fj3lvr1jnddrpbtel2nag14u2fa37n.apps.googleusercontent.com" \
                              ".json "
        scope = 'playlist-modify-private'

        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.SPOTIFY_CLIENT_ID,
                                                                 client_secret=self.SPOTIFY_CLIENT_SECRET,
                                                                 scope=scope,
                                                                 redirect_uri=self.REDIRECT_URI,
                                                                 username="1168818363"))

        #self.liked_videos = self.get_song_infos()

    # Returns general song infos about all liked Youtube Videos
    def get_song_infos(self):
        api_name = "youtube"
        api_version = "v3"
        oauth_key_file = self.OAUTH_KEY_FILE
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
                "spotify_uri": self.get_spotify_uri(song_name, artist)
            }
        return song_info

    # Returns the spotify URI of the searched song.
    def get_spotify_uri(self, song_name, artist):
        q = "track:{} artist:{}".format(song_name, artist)
        result = self.spotify.search(q=q, type="track", offset=0, limit=20)
        songs = result['tracks']['items']
        return songs[0]['uri']

    def create_playlist(self):
        description = "This is a playlist with all my liked songs on Youtube."
        self.spotify.user_playlist_create(user=self.SPOTIFY_USER_ID, public=False, name="Youtube liked Songs",
                                          description=description,  )
