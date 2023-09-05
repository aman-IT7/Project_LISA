from dateutil import parser
import requests
import datetime

lat_lon = 18.611060, 73.759697


class WeatherApi:
    def __init__(self, cur_pos: tuple[float, float]) -> None:
        """cur_pos: (lat , lon)"""
        self.cur_pos = cur_pos
        self.__api_key = "b7bbcc47b267a503b91b217e48b0a950"
        self.current_weather_api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.cur_pos[0]}&lon={self.cur_pos[1]}&appid={self.__api_key}&units=metric"
        self.forecast = f"api.openweathermap.org/data/2.5/forecast?lat={self.cur_pos[0]}&lon={self.cur_pos[1]}&appid={self.__api_key}"

    def getCurrentWeatherData(
        self,
    ):
        """Fetched the Current weather data for the given latitude and longitude"""
        try:
            response = requests.get(self.current_weather_api_url)
            if response.status_code == 200:
                # data = response.json()["main"]
                data = response.json()["main"]
                data["timeStamp"] = datetime.datetime.now().__str__()
                print(data)
                return data

            else:
                print(response.status_code)

        except Exception as err:
            raise err
            print(err)

    def getForecastWeatherData(
        self,
    ):
        """Fetched the forecast of 5 days
        currently not working (server side issue invalid url)"""

        try:
            response = requests.get(self.forecast)
            if response.status_code == 200:
                # data = response.json()["main"]
                data = response.json()["main"]
                return data
            else:
                print(response.status_code)

        except Exception as err:
            raise err
            print(err)


obj = WeatherApi(lat_lon).getCurrentWeatherData()
