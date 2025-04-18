from google import genai
import os 
import re
import json
import random
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")    
client = genai.Client(api_key=GEMINI_API_KEY)

def load_marcus_aurelius_quotes():
    """
    Load and parse the Marcus Aurelius quotes from JSON file
    
    Returns:
        list: List of Marcus Aurelius quotes
    """
    try:
        with open('data/quotes/marcus_aurelius_quotes.json', 'r', encoding='utf-8') as f:
            quotes = json.load(f)
        return quotes
    except Exception as e:
        print(f"Error loading Marcus Aurelius quotes: {e}")
        return []

def create_quote_script(quote):
    """
    Create a script explaining a single stoic quote in under 30 seconds
    
    Args:
        quote (dict): A quote dictionary with 'quote' and 'author' keys
        
    Returns:
        str: Script text
    """
    quote_text = quote['quote']
    author = quote['author']
    
    prompt = f"""Create a 30-second YouTube Shorts script that explains this stoic quote in simple terms for modern life.

    Quote: "{quote_text}"
    Author: {author}

The script should:
1. Be exactly 30 seconds when read aloud (approximately 75 words)
2. Start with a hook in the first 3 seconds to grab attention
3. Explain the quote in simple, relatable terms
4. Include a practical application for modern life
5. End with a thought-provoking conclusion
6. Be engaging and suitable for YouTube Shorts
7. Only include the narrator's dialogue, no visual cues or music notes
8. Be written in a conversational, engaging tone
9. Use short sentences and simple language
10. Include a call to action at the end

Format the response as a clean script with only the narrator's lines."""

    script_response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    
    return script_response.text

def write_script(script_text, quote):
    """
    Write the script to a file in the output directory
    
    Args:
        script_text (str): The script content to write
        quote (dict): The quote used for the script
        
    Returns:
        str: Path to the written script file
    """
    # Create output directory if it doesn't exist
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = f"output/youtube-stoic-{today}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a filename based on the first few words of the quote
    quote_preview = quote['quote'][:30].replace(" ", "_").replace("?", "").replace("!", "").replace(".", "").replace(",", "").lower()
    filename = f"script-stoic.txt"
    
    # Write script to file
    script_path = os.path.join(output_dir, filename)
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(f"QUOTE: {quote['quote']}\nAUTHOR: {quote['author']}\n\nSCRIPT:\n{script_text}")
    
    print(f"Script written to: {script_path}")
    return script_path


if __name__ == "__main__":
    print("\n--- LOADING MARCUS AURELIUS QUOTES ---\n")
    quotes = load_marcus_aurelius_quotes()
    
    if not quotes:
        print("No quotes found. Exiting...")
        exit(1)
    
    # Select a random quote
    selected_quote = random.choice(quotes)
    print(f"\n--- SELECTED QUOTE ---\n{selected_quote['quote']}\n- {selected_quote['author']}\n")
    
    print("\n--- GENERATING SCRIPT ---\n")
    script = create_quote_script(selected_quote)
    
    print("\n--- WRITING SCRIPT TO FILE ---\n")
    script_path = write_script(script, selected_quote)
    
    print("\n--- SCRIPT GENERATION COMPLETE ---\n")
    