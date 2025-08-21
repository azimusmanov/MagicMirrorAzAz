import os, json, urllib.request

API = "https://api.openweathermap.org/data/2.5/weather?q={q}&units=metric&appid={k}"

def fetch_weather():
    key = os.getenv("OPENWEATHER_API_KEY")
    city = os.getenv("CITY", "Chicago,US")
    if not key: return None
    url = API.format(q=urllib.parse.quote(city), k=key)
    with urllib.request.urlopen(url, timeout=8) as r:
        return json.loads(r.read().decode())
