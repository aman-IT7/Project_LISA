import pandas as pd
from dependancies import *

from io import StringIO

json_input = StringIO(input())
data = pd.read_json(json_input, orient="index").T


predicted_moisture = MoiturePrediction().Predict(data)
print(predicted_moisture)


test = """ {"ST_4": 27.4, "temp": 25.0, "humidity": 80.27, "precip": 0.0, "windspeed": 2.7, "cloudcover": 14.2, "conditions": "Clear"} """
