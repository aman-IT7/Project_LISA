import numpy as np
import pandas as pd
import joblib
from mqtt_publisher import *
import json

COLUMN_TRANSFORMER_FILE = "final_model/moisture_pred_columntranformer.joblib"

SCALAR_FILE = "final_model/moisture_pred_minmaxscalar.joblib"

DTR_MODEL = "C:/Users/ganes/OneDrive/Documents/GitHub/Project_LISA/water irrigation/final_model/models/dtr.bin"

GBR_MODEL = "C:/Users/ganes/OneDrive/Documents/GitHub/Project_LISA/water irrigation/final_model/models/GBR.bin"


# column order for sending it to database
COLUMN_ORDER = [
    "SM_4",
    "SM_INI",
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
        self.rawData = None
        self.predictedMoisture = None
        self.column_transformer = joblib.load(COLUMN_TRANSFORMER_FILE)
        self.scalar = joblib.load(SCALAR_FILE)
        self.MqttPublisher = MqttPublisher()
        self.gbr = joblib.load(GBR_MODEL)
        self.topic = "/node/api"

    def _preProcessData(self, data: pd.DataFrame):
        """converts pd.series data to numpy with columnTransformation, MinMaxScalar"""
        COLUMN_START_INDEX = 9
        self.data = self.column_transformer.transform(data.values)
        self.data[:, COLUMN_START_INDEX:] = self.scalar.transform(
            self.data[:, COLUMN_START_INDEX:]
        )
        self.data = np.asarray(self.data).astype("float32")
        return self.data

    def __pushToDatabase(self):
        self.rawData["SM_4"] = self.predictedMoisture
        self.rawData = self.rawData[COLUMN_ORDER]
        self.toSend = json.loads(
            self.rawData.to_json(orient="records", indent=4))[0]
        self.toSend = json.dumps(self.toSend)
        self.MqttPublisher.send_message(self.toSend, self.topic)

    def predictMositure(self, data: pd.DataFrame):
        self.rawData = data
        self.processedData = self._preProcessData(data)
        self.predictedMoisture = self.gbr.predict(self.processedData)
        self.__pushToDatabase()
        return self.predictedMoisture
