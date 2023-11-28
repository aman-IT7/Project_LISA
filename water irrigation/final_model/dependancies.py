import numpy as np
import pandas as pd
import joblib
from publisher import *
import json


COLUMN_TRANSFORMER_FILE = (
    "water irrigation/final_model/moisture_pred_columntranformer.joblib"
)
SCALAR_FILE = "water irrigation/final_model/moisture_pred_minmaxscalar.joblib"
MODEL_FILE = "C:/Users/ganes/OneDrive/Documents/GitHub/Project_LISA/water irrigation/final_model/dtr.bin"
COLUMN_ORDER = [
    "SM_4",
    "ST_4",
    "temp",
    "humidity",
    "precip",
    "windspeed",
    "cloudcover",
    "conditions",
]


class MoiturePrediction:
    def __init__(self) -> None:
        """Loading columnTransformer, MinMaxScalar, Model and taking user input"""
        self.rawData = None
        self.predictedMoisture = None
        self.ct = joblib.load(COLUMN_TRANSFORMER_FILE)
        self.scalar = joblib.load(SCALAR_FILE)
        self.dtrModel = joblib.load(MODEL_FILE)

    def __preProcessData(self, data: pd.DataFrame):
        """converts pd.series data to numpy with columnTransformation, MinMaxScalar"""
        COLUMN_START_INDEX = 9
        self.data = self.ct.transform(data.values)
        self.data[:, COLUMN_START_INDEX:] = self.scalar.transform(
            self.data[:, COLUMN_START_INDEX:]
        )
        self.data = np.asarray(self.data).astype("float32")
        return self.data

    def Predict(self, data: pd.DataFrame):
        self.rawData = data
        self.processedData = self.__preProcessData(data)
        self.predictedMoisture = self.dtrModel.predict(self.processedData)
        self.pushToDatabase()
        return self.predictedMoisture

    def pushToDatabase(self):
        self.rawData["SM_4"] = self.predictedMoisture
        self.rawData = self.rawData[COLUMN_ORDER]
        self.toSend = json.loads(self.rawData.to_json(orient="records", indent=4))[0]
        self.toSend = json.dumps(self.toSend)
        send_message(self.toSend, "test69")


# UNWANTED_PARAMS = [
#     "Date",
#     "SM_2",
#     "SM_8",
#     "SM_20",
#     "SM_40",
#     "ST_2",
#     "ST_8",
#     "ST_20",
#     "ST_40",
#     "solarenergy",
#     "precipprob",
#     "preciptype",
#     "snow",
#     "snowdepth",
#     "windgust",
#     "winddir",
#     "sealevelpressure",
#     "visibility",
#     "solarenergy",
#     "uvindex",
#     "severerisk",
#     "icon",
#     "stations",
#     "dew",
#     "solarradiation",
#     "Time",
#     "feelslike",
# ]

# dataset = pd.read_csv(
#     "C:/Users/ganes/OneDrive/Documents/GitHub/Project_LISA/water irrigation/storage_dataset/prototype_final_dataset.csv",
# )
# dataset.drop(UNWANTED_PARAMS, inplace=True, axis=1)
# dataset.dropna(inplace=True)
# to_predict = dataset.iloc[230:231, 0].values
# dataset = dataset.iloc[:, 1:]


# data1 = dataset.iloc[230:231, :]

# test = MoiturePrediction()
# print(to_predict, " => ", test.Predict(data1))
