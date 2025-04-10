from google import genai
import os 
import re
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")    
client = genai.Client(api_key=GEMINI_API_KEY)

## add a web scraping function to get the latest information 
def scrape_latest_info(prompt: str):
    
    pass





def research_with_gemini(prompt):
    """
    Research a topic using Gemini API
    
    Args:
        prompt (str): Research topic
        
    Returns:
        str: Research content
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{prompt}"
    )
    
    # Extract the text from the response correctly
    content_text = response.text
        
    # Write to file
    with open('gemini-research.txt', 'w') as f:
        f.write(content_text)
    
    print(content_text)
    return content_text

def write_script(research_content):
    """
    Write a script based on research content
    
    Args:
        research_content (str): Research content
        
    Returns:
        str: Generated script
    """
    script_response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"write a script for short form content most likely to be uploaded on youtube shorts/tiktok from the given content: {research_content}. Dont not include any extra information, just write the script meaning only include parts that the narrator needs to read out. No extra context. remove the additional information Like visual aids and only write the narrator's dialogue.",
    )
    
    # Get the text directly
    script_text = script_response.text
    print(script_text)
    
    # Write script to file
    with open('gemini-script.txt', 'w') as f:
        f.write(script_text)
        
    return script_text

def clean_script_for_audio():
    """
    Clean the script file to extract only narrator's dialogue for audio generation.
    Removes visual cues, music indications, and other non-dialogue elements.
    
    Returns:
        str: Clean narrator dialogue text ready for audio generation
    """
    try:
        with open('gemini-script.txt', 'r') as f:
            script = f.read()
        
        # Extract only the narrator's lines
        narrator_lines = []
        
        # Pattern to match "**Narrator:** <dialogue>"
        narrator_pattern = r"\*\*Narrator:\*\* (.*?)(?=\n\n|\n\*\*|\Z)"
        
        # Find all narrator dialogues using regex
        matches = re.findall(narrator_pattern, script, re.DOTALL)
        
        if matches:
            narrator_lines = [line.strip() for line in matches]
        else:
            # Fallback method if the pattern doesn't match
            lines = script.split('\n')
            for line in lines:
                # Check if this is a narrator line
                if "**Narrator:**" in line:
                    # Extract the dialogue part
                    dialogue = line.split("**Narrator:**")[-1].strip()
                    narrator_lines.append(dialogue)
        
        # Join all narrator lines with appropriate spacing
        clean_script = " ".join(narrator_lines)
        
        # Write the clean script to a new file
        with open('clean-script-for-audio.txt', 'w') as f:
            f.write(clean_script)
            
        print("Script cleaned successfully for audio generation!")
        print(clean_script)
        
        return clean_script
    
    except Exception as e:
        print(f"Error cleaning script: {e}")
        return ""


if __name__ == "__main__":
    prompt = input("Enter what you want to research about: ")
    research_content = research_with_gemini(prompt)
    print("\n--- GENERATING SCRIPT ---\n")
    script = write_script(research_content)
    print("\n--- CLEANING SCRIPT FOR AUDIO ---\n")
    clean_script = clean_script_for_audio()