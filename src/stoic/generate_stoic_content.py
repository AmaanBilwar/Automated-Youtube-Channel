import os
import sys
from stoic_news_scraper import scrape_marcus_aurelius_quotes
from stoic_script import load_marcus_aurelius_quotes, create_quote_script, write_script
import random

def main():
    """
    Main function to run the stoic content generation pipeline
    """
    print("\n=== STOIC CONTENT GENERATION PIPELINE ===\n")
    
    # Step 1: Check if quotes already exist
    quotes_file = "data/quotes/marcus_aurelius_quotes.json"
    if not os.path.exists(quotes_file) or os.path.getsize(quotes_file) == 0:
        print("No quotes found. Running scraper...")
        scrape_marcus_aurelius_quotes()
    else:
        print("Quotes file already exists. Skipping scraping.")
    
    # Step 2: Load quotes
    print("\n--- LOADING MARCUS AURELIUS QUOTES ---\n")
    quotes = load_marcus_aurelius_quotes()
    
    if not quotes:
        print("No quotes found. Exiting...")
        sys.exit(1)
    
    # Step 3: Select a random quote
    selected_quote = random.choice(quotes)
    print(f"\n--- SELECTED QUOTE ---\n{selected_quote['quote']}\n- {selected_quote['author']}\n")
    
    # Step 4: Generate script
    print("\n--- GENERATING SCRIPT ---\n")
    script = create_quote_script(selected_quote)
    
    # Step 5: Write script to file
    print("\n--- WRITING SCRIPT TO FILE ---\n")
    script_path = write_script(script, selected_quote)
    
    print("\n=== CONTENT GENERATION COMPLETE ===")
    print(f"Script saved to: {script_path}")

if __name__ == "__main__":
    main() 