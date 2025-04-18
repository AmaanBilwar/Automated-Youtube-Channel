import os

def setup_directories():
    """
    Create necessary directories for the stoic quote scraper and script generator
    """
    # Create data directory for quotes
    os.makedirs("data/quotes", exist_ok=True)
    
    # Create output directory for scripts
    os.makedirs("output", exist_ok=True)
    
    print("Directory structure created successfully!")
    print("- data/quotes/ (for storing scraped quotes)")
    print("- output/ (for storing generated scripts)")

if __name__ == "__main__":
    setup_directories() 