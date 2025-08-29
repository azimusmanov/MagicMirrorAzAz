import json
import urllib.request
import random

# List of fallback quotes in case API is unavailable
LOCAL_QUOTES = [
    {"content": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"content": "Life is what happens when you're busy making other plans.", "author": "John Lennon"},
    {"content": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
    {"content": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
    {"content": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius"},

    # Custom quotes
    {"content": "The best time to plant a tree was 20 years ago. The second best time is now.", "author": "Chinese Proverb"},
    {"content": "You don’t rise to the level of your goals, you fall to the level of your systems.", "author": "James Clear"},
    {"content": "Suffer the pain of discipline, or suffer the pain of regret.", "author": "Unknown"},
    {"content": "A man who chases two rabbits catches none.", "author": "Chinese Proverb"},
    {"content": "One percent better every day beats intensity that burns out.", "author": "Atomic Habits, distilled"},
    {"content": "Don’t let your phone dictate your focus — silence is a weapon.", "author": "Self-Reminder"},
    {"content": "Obsession over others is wasted energy — put that fire into your grind.", "author": "Self-Reminder"},
    {"content": "Amateurs wait for inspiration. Professionals get to work.", "author": "Steven Pressfield"},
    {"content": "Discipline equals freedom.", "author": "Jocko Willink"},
    {"content": "If you get tired, learn to rest, not quit.", "author": "Banksy"},
    {"content": "The day you plant the seed is not the day you eat the fruit.", "author": "Chinese Proverb"},
    {"content": "Your competition is not other people. Your competition is your own procrastination.", "author": "Unknown"},
    {"content": "Lock in now, so you don’t have to play catch-up later.", "author": "Self-Reminder"},
    {"content": "Don’t wish it were easier, wish you were better.", "author": "Jim Rohn"},
    {"content": "Consistency beats intensity every time.", "author": "Self-Reminder"},
    {"content": "What consumes your mind controls your life.", "author": "Unknown"}
]

def get_daily_quote():
    """Return a random local quote"""
    return random.choice(LOCAL_QUOTES)

# Unused because I have enough custome quotes to keep me motivated tbh
def get_daily_quote_fromAPI():
    """Get a random inspirational quote from the Quotable API or fallback to local quotes."""
    try:
        with urllib.request.urlopen("https://api.quotable.io/random", timeout=3) as response:
            return json.loads(response.read())
    except Exception:
        # Use a local quote if the API fails
        return random.choice(LOCAL_QUOTES)