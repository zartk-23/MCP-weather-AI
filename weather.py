# weather.py - Gets real weather (no API key!)
import requests

def get_weather(city):
    # Clean city name
    city = "".join(c for c in city if c.isalpha() or c.isspace()).strip()
    if not city:
        return "Invalid city name."
    
    try:
        url = f"http://wttr.in/{city}?format=%t+%c"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            temp = response.text.strip()
            return f"Weather in {city}: {temp}"
        else:
            return "Weather service down."
    except:
        return "No internet or city not found."