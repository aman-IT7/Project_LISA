import numpy as np
import pandas as pd
import tensorflow as tf
import joblib

UNWANTED_PARAMS = [
    "Date",
    "SM_2",
    "SM_8",
    "SM_20",
    "SM_40",
    "ST_2",
    "ST_8",
    "ST_20",
    "ST_40",
    "solarenergy",
    "precipprob",
    "preciptype",
    "snow",
    "snowdepth",
    "windgust",
    "winddir",
    "sealevelpressure",
    "visibility",
    "solarenergy",
    "uvindex",
    "severerisk",
    "icon",
    "stations",
    "dew",
    "solarradiation",
    "Time",
    "feelslike",
]


class MoiturePrediction:
    def __init__(self, data: pd.Series) -> None:
        self.data = data
        self.ct = joblib.load(
            "water irrigation/final_model/moisture_pred_columntranformer.joblib"
        )
        self.scalar = joblib.load(
            "water irrigation/final_model/moisture_pred_minmaxscalar.joblib"
        )
        self.model = tf.keras.models.load_model("water irrigation/final_model/zeus.h5")
        self.mlrModel = joblib.load("water irrigation/final_model/mlrmodel.bin")
        self.preProcessData()

    def preProcessData(self):
        self.data = self.data.values
        self.data = self.ct.transform(self.data)
        self.data[:, 8:] = self.scalar.transform(self.data[:, 8:])
        self.data = np.asarray(self.data).astype("float32")

    def Predict(self):
        return self.mlrModel.predict(self.data)


dataset = pd.read_csv(
    "C:/Users/ganes/OneDrive/Documents/GitHub/Project_LISA/water irrigation/storage_dataset/prototype_final_dataset.csv"
)

dataset.drop(UNWANTED_PARAMS, inplace=True, axis=1)
dataset.dropna(inplace=True)
dataset = dataset.iloc[:, 1:]

data1 = dataset.iloc[2875:2876, :]
print(data1)
print(data1.shape)


MoiturePrediction(data1)
