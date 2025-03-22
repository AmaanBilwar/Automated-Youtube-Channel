import requests
import json
import os 
from dotenv import load_dotenv
load_dotenv()

SERPER_API_KEY = os.environ.get("SERPER_API_KEY")

url = "https://google.serper.dev/search"

payload = json.dumps({
  "q": "trending topics on social media",
  "location": "United States",
  "tbs": "qdr:d"
})
headers = {
  SERPER_API_KEY: os.getenv("SERPER_API_KEY"),
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)