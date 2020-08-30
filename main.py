from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google_auth_oauthlib import flow

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
        myRating="like",
    )

    response = request.execute()

    titles: list = []
    for video in response['items']:
        titles.append(video['snippet']['title'])

    return titles



likedVideos = get_liked_youtube_videos()
print(likedVideos)
