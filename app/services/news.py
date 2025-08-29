import json
import urllib.request
import os
from dotenv import load_dotenv
load_dotenv()

# Fallback news in case API is unavailable
FALLBACK_NEWS = [
    {"title": "Sample News Headline 1", "url": "#"},
    {"title": "Sample News Headline 2", "url": "#"},
    {"title": "Sample News Headline 3", "url": "#"},
]

def get_news_headlines(count=5):
    """Get latest news headlines using NewsAPI or fallback to sample news."""
    api_key = os.getenv("NEWS_API_KEY")
    
    # If no API key, return fallback news
    if not api_key:
        return FALLBACK_NEWS[:count]
    
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read())
            articles = data.get("articles", [])
            return [{"title": a["title"], "url": a["url"]} for a in articles[:count]]
    except Exception:
        return FALLBACK_NEWS[:count]