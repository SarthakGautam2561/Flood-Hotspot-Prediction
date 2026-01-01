import requests
from config.settings import GOOGLE_MAPS_KEY


def get_area_name(lat: float, lng: float) -> str:
    """
    Reverse geocode to get human-readable area name
    """
    if not GOOGLE_MAPS_KEY:
        return "Unknown Area"

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{lat},{lng}",
        "key": GOOGLE_MAPS_KEY
    }

    try:
        res = requests.get(url, params=params, timeout=5).json()

        if res.get("status") != "OK":
            return "Unknown Area"

        for result in res["results"]:
            for comp in result["address_components"]:
                if "sublocality_level_1" in comp["types"]:
                    return comp["long_name"]
                if "locality" in comp["types"]:
                    return comp["long_name"]

        return res["results"][0]["formatted_address"]

    except Exception:
        return "Unknown Area"


def get_area_key(lat: float, lng: float) -> str:
    """
    Rough clustering key for ward-wise aggregation
    (~1km grid using rounding)
    """
    return f"{round(lat, 2)}_{round(lng, 2)}"
