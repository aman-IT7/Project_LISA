import requests
import json


API_KEY = "5EFS2W483U3M4U2423H758CN5"  # visual crossing api key
LOCATION = (18.611134, 73.759569)  # Tathwade


class VisualCrossingAPI:

    def __init__(self) -> None:
        """ As of right now we can get data for different location using name of place we can also use lat,long """
        self.filename = "current_weather.json"
        self.__endpoint_forecast_hourly = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/pune?unitGroup=us&key=5EFS2W483U3M4U2423H758CN5&contentType=json"
        self.__endpoint_forecast_daily = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/pune?unitGroup=us&include=days&key=5EFS2W483U3M4U2423H758CN5&contentType=json"
        self.__endpoint_today = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/tathawade/today?unitGroup=metric&include=hours&key=5EFS2W483U3M4U2423H758CN5&contentType=json"

    def getData_forecast_15_perhour(self) -> dict:
        """gets hourly forecast of next 15 days"""
        try:
            response = requests.get(url=self.__endpoint_forecast_hourly)
            if response.status_code == 200:
                with open("visualJSON_debug.json", "w") as file:
                    file.write(response.text)
                return response.json()["days"]
            else:
                raise Exception("ERROR OCCURED")
        except Exception as e:
            raise e

    def getData_forecast_15_perday(self) -> dict:
        """Gets daily forecast of next 15 days"""
        try:
            response = requests.get(url=self.__endpoint_forecast_daily)
            if response.status_code == 200:
                with open("visualJSON_debug.json", "w") as file:
                    file.write(response.text)

                data = response.json()["days"]
                return data
            else:
                raise Exception("ERROR OCCURED")
        except Exception as e:
            raise e

    def getData_current_weather(self,) -> dict:
        """ Retrives current weather (Todays) weather data """
        try:
            response = requests.get(self.__endpoint_today)
            if response.status_code == 200:
                with open("current_weather.json", 'w') as file:
                    data = response.json()
                    final_data = json.dumps(data['days'][0])
                    file.write(final_data)

                return data
            else:
                raise Exception(response.status_code)

        except Exception as e:
            raise e
