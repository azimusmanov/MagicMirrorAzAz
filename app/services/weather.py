import os
from dotenv import load_dotenv
load_dotenv()
import json
import urllib.request
import urllib.parse
from get_loc import get_location

API_BASE = "https://api.openweathermap.org/data/2.5/forecast"

def fetch_weather():
    key = os.getenv("OPENWEATHER_API_KEY")
    lat, lon = get_location()

    if not lat:
        print("NO Lat")
    if not key or not lat or not lon:
        print("failed")
        return None

    params = {
        "lat": lat,
        "lon": lon,
        "units": "imperial",  # Fahrenheit
        "appid": key
    }

    url = f"{API_BASE}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            data = json.loads(r.read().decode("utf-8"))
            # Extract essential info for widget (from forecast list)
            current = data["list"][0]
            result = {
                "current": {
                    "temp": current["main"]["temp"],
                    "weather": current["weather"][0]["main"],
                    "rain": current.get("rain", {}).get("3h", 0)
                },
                "city": data["city"]["name"]
            }
            return result
    except Exception:
        print("Exception")
        return None