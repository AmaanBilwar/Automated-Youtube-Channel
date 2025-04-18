from google import genai
import os 
from dotenv import load_dotenv
from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import numpy as np
import datetime
load_dotenv()


today = datetime.datetime.now().strftime("%Y-%m-%d")
def generate_audio(script_text):
    with open(f'output/youtube-tech-{today}/script-tech.txt', 'r') as f:
        script_text = f.read()

    pipeline = KPipeline(lang_code='a')

    text = f"{script_text}"

    generator = pipeline(text, voice='af_heart')
    
    # Collect all audio chunks
    all_audio_chunks = []
    for i, (gs, ps, audio) in enumerate(generator):
        print(f"Processing chunk {i}")
        all_audio_chunks.append(audio)
    
    # Combine all audio chunks into a single array
    combined_audio = np.concatenate(all_audio_chunks)
    
    # Save the combined audio to a single file
    output_filename = f'output/youtube-tech-{today}/voiceover-tech.wav'
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    sf.write(output_filename, combined_audio, 24000)
    
    print(f"Audio saved to {output_filename}")
    
    # Display the combined audio
    display(Audio(data=combined_audio, rate=24000, autoplay=True))
    
    return combined_audio

generate_audio('script-tech.txt')