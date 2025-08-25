import json
import urllib.request

def get_location():
    try:
        with urllib.request.urlopen("https://ipinfo.io/json") as response:
            data = json.load(response)
            loc = data.get("loc", "")
            if loc:
                lat, lon = loc.split(",")
                return float(lat), float(lon)
    except Exception as e:
        print("Location error:", e)
        return None, None

if __name__ == "__main__":
    lat, lon = get_location()
    print("Latitude:", lat)
    print("Longitude:", lon)