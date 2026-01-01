import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")

DEBUG = True
