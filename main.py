import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient



LAT = 51.5074
LON = -0.1278

OWN_Endopoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWN_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

weather_params= {
    "lat": LAT,
    "lon": LON,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWN_Endopoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
# print(weather_data)

will_rain = False

for hour_data in weather_data["list"]:
    condition_code = hour_data['weather'][0]['id']

    if int(condition_code) < 1700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella",
        from_=os.environ.get("MY_TWILIO_VIRTUAL_NUMBER"),
        to=os.environ.get("MY_TWILIO_VERIFIED_REAL_NUMBER"),
    )

    print(message.status)

    print("Bring an Umbrella")


