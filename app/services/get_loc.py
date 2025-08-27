import json
import urllib.request
from timezonefinder import TimezoneFinder

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
    
def get_timezone_from_coords(lat, lon):
    tf = TimezoneFinder()
    tzname = tf.timezone_at(lat=lat, lng=lon)  # e.g., "America/Aruba"
    return tzname

if __name__ == "__main__":
    lat, lon = get_location()
    tzname = get_timezone_from_coords(lat, lon)
    print("Latitude:", lat)
    print("Longitude:", lon)
    print("Timezone: ", tzname)