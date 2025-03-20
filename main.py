import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages and session

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'wmv', 'flv', 'mkv'}
TOKEN_PICKLE_PATH = 'token.pickle'
CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_authenticated_service():
    """Get YouTube API client with stored credentials or new ones."""
    credentials = None
    
    # Load credentials from pickle file if exists
    if os.path.exists(TOKEN_PICKLE_PATH):
        with open(TOKEN_PICKLE_PATH, 'rb') as token:
            credentials = pickle.load(token)
    
    # If credentials don't exist or are invalid, authenticate
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=8090)
        
        # Save credentials for future use
        with open(TOKEN_PICKLE_PATH, 'wb') as token:
            pickle.dump(credentials, token)
    
    # Build the YouTube service
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_to_youtube(file_path, title, description, tags=None, category_id="22"):
    """Upload a video to YouTube as unlisted"""
    youtube = get_authenticated_service()
    
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
    media = MediaFileUpload(file_path, resumable=True)
    
    # Create the upload request
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )
    
    # Execute the upload
    response = request.execute()
    
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate')
def authenticate():
    """Force re-authentication"""
    if os.path.exists(TOKEN_PICKLE_PATH):
        os.remove(TOKEN_PICKLE_PATH)
    get_authenticated_service()
    flash('Authentication successful!', 'success')
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'video' not in request.files:
            flash('No video file part', 'error')
            return redirect(request.url)
        
        file = request.files['video']
        
        # If user doesn't select file, browser also submit an empty part
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            title = request.form.get('title', 'Untitled Video')
            description = request.form.get('description', '')
            
            try:
                response = upload_to_youtube(filepath, title, description)
                video_id = response.get('id')
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                flash(f'Video uploaded successfully! URL: {video_url}', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error uploading to YouTube: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('File type not allowed', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """API endpoint for programmatic uploads"""
    data = request.json
    
    if not data or 'file_path' not in data:
        return jsonify({'error': 'Missing file path'}), 400
    
    file_path = data['file_path']
    title = data.get('title', 'Untitled Video')
    description = data.get('description', '')
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        response = upload_to_youtube(file_path, title, description)
        video_id = response.get('id')
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        return jsonify({
            'success': True,
            'video_id': video_id,
            'video_url': video_url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Enable HTTPS locally for OAuth
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(debug=True, host='0.0.0.0', port=5000)