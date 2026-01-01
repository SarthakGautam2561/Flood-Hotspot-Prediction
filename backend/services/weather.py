import requests
from config.settings import WEATHER_API_KEY as API_KEY

def get_rainfall(lat: float, lng: float) -> float:
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lng}&appid={API_KEY}&units=metric"
    )

    try:
        res = requests.get(url, timeout=5)
        data = res.json()

        rain = data.get("rain", {})
        return rain.get("1h", 0.0)

    except Exception as e:
        print("Weather API error:", e)
        return 0.0
