import pandas as pd
from dependancies import *
from io import StringIO

json_input = StringIO(input())

# sample data to test
# test = """ {"ST_4": 30.4, "temp": 40.0, "humidity": 70.27, "precip": 0.0, "windspeed": 10.7, "cloudcover": 50.2, "conditions": "Clear"} """

weather_data = pd.read_json(json_input, orient="index").T


predicted_moisture = MoiturePrediction().Predict(weather_data)
print(predicted_moisture)


"""
final stats:

ANN:
    mean absolute error =  3.0655832
    mean Squared error =  13.80442

MLR:
    mean absolute error = 3.027409
    mean Squared error =  13.826493

DTR:
    DTR MAE: 2.4106774283905894
    DTR MSE: 11.722721501863939

SVR:
    mean_absolute_error =  2.904093050843496
    mean_squared_error =  13.453183997821128
"""
