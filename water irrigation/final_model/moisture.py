import pandas as pd
import json
from dependancies import *


data = pd.read_json(json.dumps(input()))

predicted_moisture = MoiturePrediction(data).Predict()
print(predicted_moisture)
