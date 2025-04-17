import os
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload  # Add this import
from dotenv import load_dotenv
load_dotenv()

print("Starting YouTube API connection...")
client_secrets_file = "client_secret.json"
scopes = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtube.upload"]
api_service_name = "youtube"
api_version = "v3"

# Run the OAuth flow
print("Starting OAuth flow...")
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_local_server()
print("OAuth flow completed successfully!")

# Use credentials from OAuth flow instead of API key
print("Building YouTube service...")
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

# Now this should work with the proper authorization
print("Making YouTube API request...")
request = youtube.channels().list(
    part="snippet,contentDetails,statistics",   
    mine=True)

print("Executing request...")
try:
    response = request.execute()
    print("Request successful!")
    print("Channel information:")
    print(response)
    
    # After getting the response
    if 'items' in response and len(response['items']) > 0:
        channel = response['items'][0]
        print(f"Channel Title: {channel['snippet']['title']}")
        print(f"Channel ID: {channel['id']}")
        print(f"Subscriber Count: {channel['statistics'].get('subscriberCount', 'Not available')}")
        print(f"View Count: {channel['statistics']['viewCount']}")
except googleapiclient.errors.HttpError as e:
    print(f"An error occurred: {e}")



def upload_video(youtube,file_path,title,description):
    request_body = {
        "snippet": {
            "categoryId": 22,
            "description": description,
            "title": title,
            "tags": ["test", "api"]
        },
        "status": {
            "privacyStatus": "unlisted"
        }
    }
    media = MediaFileUpload(file_path)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )
    response = request.execute()
    print(response)