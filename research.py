from google import genai
import os 
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")    
client = genai.Client(api_key=GEMINI_API_KEY)

prompt = input("enter what you wanna research abt: ")


response = client.models.generate_content_stream(
    model="gemini-1.5-flash",
    contents=f"{prompt}"
)
for content in response:
    print(content.text)