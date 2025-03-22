import requests
import json
import os
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv
load_dotenv()

# Your Serper API key - store in environment variable for security
SERPER_API_KEY = os.environ.get("SERPER_API_KEY")  # Set this as an environment variable

def get_trending_topics(query="trending news", time_period="d1", num_results=5):
    """
    Get trending topics using Serper API
    time_period: d1 (past 24 hours) or d2 (past 48 hours)
    """
    url = "https://google.serper.dev/search"
    
    payload = json.dumps({
        "q": query,
        "gl": "us",  # Geographic location (US)
        "hl": "en",  # Language (English)
        "tbs": f"qdr:{time_period}",  # Time period: d1 (24h) or d2 (48h)
        "num": num_results
    })
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        results = response.json()
        return extract_topics(results)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []

def extract_topics(results):
    """Extract trending topics from Serper API results"""
    topics = []
    
    # Extract from organic results
    if "organic" in results:
        for item in results["organic"]:
            topics.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", ""),
                "source": item.get("source", "")
            })
    
    # You could also extract from news results if available
    if "news" in results:
        for item in results["news"]:
            topics.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", ""),
                "source": item.get("source", ""),
                "date": item.get("date", "")
            })
            
    return topics

def main():
    # Choose a variety of search queries to get diverse trending topics
    search_queries = [
        "trending news today",
        "viral stories now",
        "trending topics social media",
        "what's happening today",
        "breaking news today"
    ]
    
    # Randomly select a time period (24h or 48h)
    time_period = random.choice(["d1", "d2"])
    
    # Get trending topics from multiple queries
    all_topics = []
    for query in search_queries:
        print(f"Searching for: {query} (past {time_period.replace('d', '')} days)")
        topics = get_trending_topics(query, time_period)
        all_topics.extend(topics)
        
    # Remove duplicates (by link)
    unique_topics = []
    seen_links = set()
    for topic in all_topics:
        if topic["link"] not in seen_links:
            seen_links.add(topic["link"])
            unique_topics.append(topic)
    
    # Print results
    print(f"\nFound {len(unique_topics)} unique trending topics:")
    for i, topic in enumerate(unique_topics, 1):
        print(f"\n{i}. {topic['title']}")
        print(f"   {topic['snippet']}")
        print(f"   Source: {topic.get('source', 'Unknown')}")
        print(f"   Link: {topic['link']}")
        if "date" in topic:
            print(f"   Date: {topic['date']}")

if __name__ == "__main__":
    main()
