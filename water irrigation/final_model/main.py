import pandas as pd
from dependancies import *
from io import StringIO
from VisualCrossingAPI import *

# json_input = StringIO(input())

# sample data to test
# test = """ {"ST_4": 30.4, "temp": 40.0, "humidity": 70.27, "precip": 0.0, "windspeed": 10.7, "cloudcover": 50.2, "conditions": "Clear"} """
# weather_data = pd.read_json(test, orient="index").T

predicted_moisture = MoiturePrediction()
weather_api = VisualCrossingAPI()


def weather_data(time: int):
    """get weather data"""
    weather_data = weather_api.getData_current_weather()[time]
    return json.dumps(weather_data)


def format_weather_data(weather_data):
    COLUMN_ORDER_WEATHER = [
        "temp",
        "humidity",
        "precip",
        "windspeed",
        "cloudcover",
        "conditions",
    ]
    pd_data = pd.read_json(weather_data)
    formatted_data = pd_data[COLUMN_ORDER_WEATHER]
    return formatted_data


# wd = weather_data(1)
# print(format_weather_data(wd))
