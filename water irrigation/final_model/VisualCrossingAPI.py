""" This module will be used to gather data on-site and then upload it using MQTT to our cloud daatbase """


import requests
import json

API_KEY = "5EFS2W483U3M4U2423H758CN5"  # visual crossing api key
LOCATION = (18.611134, 73.759569)  # Tathwade
ENDPOINT_FORECAST_HOURLY = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/pune?unitGroup=us&key=5EFS2W483U3M4U2423H758CN5&contentType=json"
ENDPOINT_FORECAST_DAILY = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/pune?unitGroup=us&include=days&key=5EFS2W483U3M4U2423H758CN5&contentType=json"
ENDPOINT_TODAY = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/tathawade/today?unitGroup=metric&include=hours&key=5EFS2W483U3M4U2423H758CN5&contentType=json"


class VisualCrossingAPI:
    def getData_forecast_15_perhour(self) -> dict:
        """gets hourly forecast of next 15 days"""
        try:
            response = requests.get(url=ENDPOINT_FORECAST_HOURLY)
            if response.status_code == 200:
                return response.json()["days"]
            else:
                raise Exception("ERROR OCCURED")
        except Exception as e:
            raise e

    def getData_forecast_15_perday(self) -> dict:
        """Gets daily forecast of next 15 days"""
        try:
            response = requests.get(url=ENDPOINT_FORECAST_DAILY)
            if response.status_code == 200:
                data = response.json()["days"]
                return data
            else:
                raise Exception("ERROR OCCURED")
        except Exception as e:
            raise e

    def getData_current_weather(
        self,
    ) -> dict:
        """Retrives current weather (Todays) weather data"""
        try:
            response = requests.get(ENDPOINT_TODAY)
            if response.status_code == 200:
                data = response.json()
                # with open("testing.json", "w") as f:
                #     f.write(json.dumps(data["days"][0]["hours"]))
                return data["days"][0]["hours"]
            else:
                raise Exception(response.status_code)

        except Exception as e:
            raise e
