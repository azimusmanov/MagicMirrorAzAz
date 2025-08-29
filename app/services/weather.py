import os
from dotenv import load_dotenv
load_dotenv()
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta  # <-- add timedelta
from app.services.get_loc import get_location
import requests

API_BASE = "https://api.openweathermap.org/data/2.5/forecast"

def get_units(lat, lon):
    # Use a free geolocation API to get country code
    try:
        resp = requests.get(f"https://geocode.maps.co/reverse?lat={lat}&lon={lon}")
        country = resp.json().get("address", {}).get("country_code", "us").lower()
        return "imperial" if country == "us" else "metric"
    except Exception:
        return "metric"
    
def fetch_weather():
    key = os.getenv("OPENWEATHER_API_KEY")
    lat, lon = get_location()
    units = get_units(lat, lon)
    if not lat or not key or not lon:
        print("failed")
        return None

    params = {"lat": lat, "lon": lon, "units": units, "appid": key}
    url = f"{API_BASE}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            data = json.loads(r.read().decode("utf-8"))

        current = data["list"][0]

        # Build tz from OpenWeather’s city timezone offset (seconds from UTC)
        offset_sec = int(data["city"].get("timezone", 0))
        local_tz = timezone(timedelta(seconds=offset_sec))

        now_local = datetime.now(local_tz)
        today_local = now_local.date()

        summary = []
        for entry in data["list"]:
            # forecast dt is a UTC unix timestamp
            entry_utc = datetime.fromtimestamp(int(entry["dt"]), tz=timezone.utc)
            entry_local = entry_utc.astimezone(local_tz)

            # keep only items AFTER now, and (optional) only for the rest of today
            if entry_local > now_local and entry_local.date() == today_local:
                summary.append({
                    "time": entry_local.strftime("%I:%M %p").lstrip("0"),
                    "temp": entry["main"]["temp"],
                    "weather": entry["weather"][0]["main"],
                    "rain": entry.get("rain", {}).get("3h", 0),
                })

        result = {
            "current": {
                "temp": current["main"]["temp"],
                "weather": current["weather"][0]["main"],
                "rain": current.get("rain", {}).get("3h", 0),
            },
            "city": data["city"]["name"],
            "today_summary": summary,
            "units": units
        }
        return result

    except Exception as e:
        print("Exception:", repr(e))
        return None
