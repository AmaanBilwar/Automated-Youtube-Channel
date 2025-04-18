import requests
from bs4 import BeautifulSoup
import time
import random
import os
import json
from datetime import datetime

def scrape_marcus_aurelius_quotes():
    """
    Scrape Marcus Aurelius quotes from Goodreads.
    """
    url = "https://www.goodreads.com/author/quotes/17212.Marcus_Aurelius"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all quote elements
        quote_elements = soup.select('.quoteText')
        
        quotes = []
        for element in quote_elements:
            # Extract the quote text
            quote_text = element.get_text().strip()
            
            # Clean up the quote text (remove attribution and extra whitespace)
            quote_text = quote_text.split('―')[0].strip()
            quote_text = quote_text.replace('"', '').strip()
            
            if quote_text:
                quotes.append({
                    "quote": quote_text,
                    "author": "Marcus Aurelius",
                    "source": "Goodreads",
                    "date_scraped": datetime.now().strftime("%Y-%m-%d")
                })
        
        # Create directory if it doesn't exist
        os.makedirs("data/quotes", exist_ok=True)
        
        # Save quotes to a JSON file
        with open("data/quotes/marcus_aurelius_quotes.json", "w", encoding="utf-8") as f:
            json.dump(quotes, f, indent=4, ensure_ascii=False)
        
        print(f"Successfully scraped {len(quotes)} quotes from Marcus Aurelius.")
        return quotes
    
    except Exception as e:
        print(f"Error scraping quotes: {e}")
        return []

if __name__ == "__main__":
    scrape_marcus_aurelius_quotes()
