import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ---------------------------- CONSTANTS ------------------------------- #

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

LATITUDE = 31.5497
LONGITUDE = 73.1236

API_KEY = os.getenv("OWM_API_KEY")

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

TWILIO_PHONE = os.getenv("TWILIO_PHONE")
MY_PHONE = os.getenv("MY_PHONE")

# ---------------------------- WEATHER REQUEST ------------------------------- #

parameters = {
    "lat": LATITUDE,
    "lon": LONGITUDE,
    "appid": API_KEY,
    "cnt": 4,
}

response = requests.get(OWM_ENDPOINT, params=parameters)
response.raise_for_status()

weather_data = response.json()

# ---------------------------- RAIN CHECK ------------------------------- #

will_rain = False

for forecast in weather_data["list"]:
    weather_id = forecast["weather"][0]["id"]

    if weather_id < 700:
        will_rain = True

# ---------------------------- SEND SMS ------------------------------- #

if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages.create(
        body="🌧️ It's going to rain today.\nDon't forget to take an umbrella! ☔",
        from_=TWILIO_PHONE,
        to=MY_PHONE,
    )

    print("SMS Sent Successfully!")
    print("Message SID:", message.sid)

else:
    print("No rain expected today.")