#!/usr/bin/env python3
"""
Hacker News Scraper

This script scrapes the top 5 stories from Hacker News (https://news.ycombinator.com/)
and extracts information from each linked article.
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
import os
from typing import Dict, List, Optional, Tuple

class HackerNewsScraper:
    """Scraper for Hacker News website."""
    
    def __init__(self, base_url: str = "https://news.ycombinator.com/"):
        """Initialize the scraper with the base URL."""
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def get_top_stories(self, limit: int = 5) -> List[Dict]:
        """
        Get the top stories from Hacker News.
        
        Args:
            limit: Number of stories to retrieve
            
        Returns:
            List of dictionaries containing story information
        """
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            stories = []
            
            # Find all story items
            story_items = soup.select(".athing")
            
            for i, item in enumerate(story_items[:limit]):
                # Get the story ID
                story_id = item.get("id")
                
                # Get the story title and link
                title_cell = item.select_one(".titleline > a")
                if not title_cell:
                    continue
                    
                title = title_cell.text
                link = title_cell.get("href")
                
                # Make sure the link is absolute
                if link and not link.startswith(("http://", "https://")):
                    link = f"https://news.ycombinator.com/{link}"
                
                # Get the story details from the following row
                details_row = item.find_next_sibling("tr")
                if not details_row:
                    continue
                
                # Get points, author, and comments
                score = details_row.select_one(".score")
                score_text = score.text.split()[0] if score else "0"
                
                author = details_row.select_one(".hnuser")
                author_text = author.text if author else "unknown"
                
                comments_link = details_row.select_one("a[href*='item']")
                comments_count = "0"
                if comments_link:
                    comments_text = comments_link.text
                    if "comment" in comments_text:
                        comments_count = comments_text.split()[0]
                
                # Get article content if possible
                article_content = self._get_article_content(link) if link else None
                
                story = {
                    "id": story_id,
                    "title": title,
                    "link": link,
                    "points": score_text,
                    "author": author_text,
                    "comments": comments_count,
                    "article_content": article_content,
                    "scraped_at": datetime.now().isoformat()
                }
                
                stories.append(story)
                
                # Be nice to the server
                time.sleep(1)
            
            return stories
            
        except Exception as e:
            print(f"Error scraping Hacker News: {e}")
            return []
    
    def _get_article_content(self, url: str) -> Optional[Dict]:
        """
        Get content from the linked article.
        
        Args:
            url: URL of the article
            
        Returns:
            Dictionary with article content or None if failed
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Try to get the title
            title = None
            title_tag = soup.select_one("title")
            if title_tag:
                title = title_tag.text.strip()
            
            # Try to get the main content
            content = None
            
            # Try different common content selectors
            content_selectors = [
                "article", 
                "main", 
                ".article-content", 
                ".post-content", 
                ".entry-content",
                "#content",
                ".content"
            ]
            
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    # Get text from paragraphs
                    paragraphs = content_elem.select("p")
                    if paragraphs:
                        content = "\n\n".join([p.text.strip() for p in paragraphs if p.text.strip()])
                        break
            
            # If no paragraphs found, try to get all text
            if not content:
                content_elem = soup.select_one("body")
                if content_elem:
                    content = content_elem.text.strip()
            
            # Try to get meta description
            description = None
            meta_desc = soup.select_one('meta[name="description"]')
            if meta_desc:
                description = meta_desc.get("content")
            
            return {
                "title": title,
                "description": description,
                "content": content[:1000] if content else None  # Limit content length
            }
            
        except Exception as e:
            print(f"Error getting article content from {url}: {e}")
            return None
    
    def save_stories(self, stories: List[Dict], filename: str = "hacker_news_stories.json"):
        """
        Save stories to a JSON file.
        
        Args:
            stories: List of story dictionaries
            filename: Output filename
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(stories, f, indent=2, ensure_ascii=False)
            print(f"Stories saved to {filename}")
        except Exception as e:
            print(f"Error saving stories: {e}")


def main():
    """Main function to run the scraper."""
    scraper = HackerNewsScraper()
    print("Scraping top 5 stories from Hacker News...")
    stories = scraper.get_top_stories(limit=5)
    
    if stories:
        print(f"Successfully scraped {len(stories)} stories")
        
        # Print summary of each story
        for i, story in enumerate(stories, 1):
            print(f"\n{i}. {story['title']}")
            print(f"   Points: {story['points']} | Author: {story['author']} | Comments: {story['comments']}")
            print(f"   Link: {story['link']}")
            
            if story.get('article_content'):
                content = story['article_content']
                if content.get('description'):
                    print(f"   Description: {content['description'][:150]}...")
                elif content.get('content'):
                    print(f"   Content: {content['content'][:150]}...")
        
        # Save to file
        scraper.save_stories(stories)
    else:
        print("Failed to scrape any stories")


if __name__ == "__main__":
    main()
