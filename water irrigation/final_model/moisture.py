import pandas as pd
import json
from dependancies import *


data = pd.read_json(json.dumps(input()))

predicted_moisture = MoiturePrediction().Predict(data)
print(predicted_moisture)
