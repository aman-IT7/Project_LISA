import pandas as pd
from dependancies import *

from io import StringIO

json_input = StringIO(input())

# sample data to test
# test = """ {"ST_4": 30.4, "temp": 40.0, "humidity": 70.27, "precip": 0.0, "windspeed": 10.7, "cloudcover": 50.2, "conditions": "Clear"} """

data = pd.read_json(json_input, orient="index").T


predicted_moisture = MoiturePrediction().Predict(data)
print(predicted_moisture)
