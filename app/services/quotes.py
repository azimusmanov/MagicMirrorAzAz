import json
import urllib.request
import random

# List of fallback quotes in case API is unavailable
FALLBACK_QUOTES = [
    {"content": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"content": "Life is what happens when you're busy making other plans.", "author": "John Lennon"},
    {"content": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
    {"content": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
    {"content": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius"},
]

def get_daily_quote():
    """Get a random inspirational quote from the Quotable API or fallback to local quotes."""
    try:
        with urllib.request.urlopen("https://api.quotable.io/random", timeout=3) as response:
            return json.loads(response.read())
    except Exception:
        # Use a local quote if the API fails
        return random.choice(FALLBACK_QUOTES)