import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

def authenticate_youtube():
    """Authenticate with YouTube API using OAuth flow"""
    print("Starting YouTube API authentication...")
    client_secrets_file = "client_secret.json"
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    
    # Allow OAuth flow in development environment
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
    # Run the OAuth flow
    print("Starting OAuth flow...")
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=8090)
    print("OAuth flow completed successfully!")
    
    # Create YouTube service
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)
    
    return youtube

def upload_video(youtube, file_path, title, description, tags=None, category_id="22"):
    """Upload a video to YouTube as unlisted"""
    if tags is None:
        tags = ["api", "upload", "automated"]
        
    # Create request body
    request_body = {
        "snippet": {
            "categoryId": category_id,
            "description": description,
            "title": title,
            "tags": tags
        },
        "status": {
            "privacyStatus": "unlisted",
            "selfDeclaredMadeForKids": False
        }
    }
    
    # Prepare the media file
    print(f"Preparing to upload: {file_path}")
    media = MediaFileUpload(file_path, resumable=True)
    
    # Create the upload request
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )
    
    # Execute the upload
    print("Starting upload... This may take a while depending on file size")
    response = request.execute()
    
    # Return upload details
    video_id = response.get("id")
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    print(f"Upload successful!")
    print(f"Video title: {title}")
    print(f"Video ID: {video_id}")
    print(f"Video URL: {video_url}")
    
    return response

def main():
    # Authenticate
    youtube = authenticate_youtube()
    
    # Upload details
    video_path = input("Enter the path to your video file: ")
    video_title = input("Enter video title: ")
    video_description = input("Enter video description: ")
    
    # Validate the file exists
    if not os.path.exists(video_path):
        print(f"Error: File not found at {video_path}")
        return
    
    # Upload the video
    response = upload_video(
        youtube=youtube,
        file_path=video_path,
        title=video_title,
        description=video_description
    )
    
    print("Upload complete!")

if __name__ == "__main__":
    main()