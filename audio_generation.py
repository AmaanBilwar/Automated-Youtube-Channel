from google import genai
import os 
from dotenv import load_dotenv
from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import torch
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")    
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_audio(script_text):
    with open('clean-script-for-audio.txt', 'r') as f:
        script_text = f.read()

    pipeline = KPipeline(lang_code='a')

    text = f"{script_text}"

    generator = pipeline(text, voice='af_heart')
    for i, (gs, ps, audio) in enumerate(generator):
        print(i, gs, ps)
        display(Audio(data=audio, rate=24000, autoplay=i==0))
        sf.write(f'{i}.wav', audio, 24000)

    return audio

generate_audio('clean-script-for-audio.txt')