from google import genai
import os 
import re
import json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")    
client = genai.Client(api_key=GEMINI_API_KEY)

def load_hacker_news_stories():
    """
    Load and parse the hacker news stories from JSON file
    
    Returns:
        list: List of hacker news stories
    """
    try:
        with open('stoic_ideaologies.json', 'r', encoding='utf-8') as f:
            stories = json.load(f)
        return stories
    except Exception as e:
        print(f"Error loading hacker news stories: {e}")
        return []

def create_combined_script(stories):
    """
    Create a combined script from multiple hacker news stories
    
    Args:
        stories (list): List of hacker news stories
        
    Returns:
        str: Combined script text
    """
    # Prepare the content for the prompt
    stories_content = "\n".join([
        f"Title: {story['title']}\nPoints: {story['points']}\n"
        for story in stories[:5]  # Use top 5 stories
    ])
    
    prompt = f"""Create a 30-second engaging script for stoic ideologies video using these ideologies:
{stories_content}

The script should:
1. Be exactly 30 seconds when read aloud
2. Focus on the most interesting aspects of each ideaology
3. Be engaging and suitable for YouTube Shorts
4. Include a brief introduction and conclusion
5. Only include the narrator's dialogue, no visual cues or music notes
6. Be written in a conversational, engaging tone

Format the response as a clean script with only the narrator's lines."""

    script_response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    
    return script_response.text

def write_script(script_text):
    """
    Write the script to a file in the output directory
    
    Args:
        script_text (str): The script content to write
        
    Returns:
        str: Path to the written script file
    """
    # Create output directory if it doesn't exist
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = f"output/youtube-stoic-{today}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Write script to file
    script_path = os.path.join(output_dir, "script-stoic.txt")
    with open(script_path, 'w') as f:
        f.write(script_text)
    
    print(f"Script written to: {script_path}")
    return script_path


if __name__ == "__main__":
    print("\n--- LOADING STOIC IDEOLOGIES ---\n")
    stories = load_hacker_news_stories()
    
    if not stories:
        print("No ideologies found. Exiting...")
        exit(1)
    
    print("\n--- GENERATING COMBINED SCRIPT ---\n")
    combined_script = create_combined_script(stories)
    
    print("\n--- WRITING SCRIPT TO FILE ---\n")
    script_path = write_script(combined_script)
    