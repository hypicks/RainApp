import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os

api_key = os.environ.get("OMW_API_KEY")
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
account_sid = "AC122f58c79dbb6534f48dc72f1ebbde37"
auth_token = os.environ.get("AUTH_TOKEN")

# The parameters have to match what the URL says. To a tee.

parameters = {
    "lat": 59.3326,
    "lon": 18.0649,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=parameters)
# To see if the response requests works as planned
print(response.status_code)
# If error-code is discovered, raise a status
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
                    .create(
                         body="It's going to rain today. Don't forget to bring an ☂️",
                         from_='number_from_twilio',
                         to='your_number'
                     )

    print(message.status)
