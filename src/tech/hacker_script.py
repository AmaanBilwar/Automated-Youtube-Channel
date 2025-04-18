import json
import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")    
client = genai.Client(api_key=GEMINI_API_KEY)

def load_tech_news():
    """
    Load and parse the tech news from JSON file
    
    Returns:
        list: List of tech news items
    """
    try:
        with open('hacker_news_stories.json', 'r', encoding='utf-8') as f:
            news_items = json.load(f)
        return news_items[:5]  # Get only the first 5 news items
    except Exception as e:
        print(f"Error loading tech news: {e}")
        return []

def create_tech_script(news_items):
    """
    Create a script from multiple tech news items
    
    Args:
        news_items (list): List of tech news items
        
    Returns:
        str: Combined script text
    """
    # Prepare the content for the prompt
    news_content = ""
    for i, item in enumerate(news_items, 1):
        news_content += f"\nNews {i}:\nTitle: {item['title']}\nURL: {item['link']}\nPoints: {item['points']}\n"
    
    prompt = f"""Create a 60-second YouTube Shorts script that summarizes these 5 tech news stories in an engaging way.

    {news_content}

The script should:
1. Be exactly 60 seconds when read aloud (approximately 150 words)
2. Start with a hook in the first 3 seconds to grab attention
3. Summarize each news item in 10-12 seconds
4. Include why these news items matter to the viewer
5. End with a thought-provoking conclusion
6. Be engaging and suitable for YouTube Shorts
7. Only include the narrator's dialogue, no visual cues or music notes
8. Be written in a conversational, engaging tone
9. Use short sentences and simple language
10. Include a call to action at the end
11. Flow smoothly between different news items
12. Highlight the most interesting aspects of each story

Format the response as a clean script with only the narrator's lines."""

    script_response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    
    return script_response.text

def write_tech_script(script_text, news_items):
    """
    Write the script to a file in the output directory
    
    Args:
        script_text (str): The script content to write
        news_items (list): The news items used for the script
        
    Returns:
        str: Path to the written script file
    """
    # Create output directory if it doesn't exist
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = f"output/youtube-tech-{today}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Write script to file
    script_path = os.path.join(output_dir, "script-tech.txt")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_text)
    
    print(f"Script written to: {script_path}")
    return script_path

def main():
    # Load news items
    news_items = load_tech_news()
    if not news_items:
        print("No news items found")
        return
    
    # Create combined script for all news items
    script_text = create_tech_script(news_items)
    
    # Write the script to file
    script_path = write_tech_script(script_text, news_items)
    print(f"Combined script generated and saved to: {script_path}")

if __name__ == "__main__":
    main() 