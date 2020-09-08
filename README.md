# Spotify-Playlist-Creator
## This is my first try of using the 'YouTube Data API v3' and the 'Spotify API'
### Spotify API: https://developer.spotify.com/
### Youtube API: https://developers.google.com/youtube/v3
#### This project gets information about your liked voutube videos and tries to find fitting spotify tracks, create a playlist and adds the songs. It is only tested for an account that only likes youtube music.

#### To correctly use this project you need several things:
``` python
client_id_spotify = input("Spotify Client ID:")
client_secret_spotify = input("Spotify Client Secret:")
user_id = input("Spotify User ID:")
oauth_token = input("Spotify Oauth Token:")
```
#### You need your Spotify Client ID, the Client Secret ID, the User ID and an Oauth Token: https://developer.spotify.com/documentation/general/guides/authorization-guide/
#### Furthermore you need to have a Youtbe API Key and OAuth 2.0 Client ID which you can obtain from: https://console.developers.google.com/apis/credentials
## Note that the client_secret.json file is empty. When downloading it from the credentials page you can copy paste the data into client_secret.json
