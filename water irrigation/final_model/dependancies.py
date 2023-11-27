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
    def __init__(self) -> None:
        """Loading columnTransformer, MinMaxScalar, Model and taking user input"""
        self.ct = joblib.load(
            "water irrigation/final_model/moisture_pred_columntranformer.joblib"
        )
        self.scalar = joblib.load(
            "water irrigation/final_model/moisture_pred_minmaxscalar.joblib"
        )
        self.dtrModel = joblib.load(
            "C:/Users/ganes/OneDrive/Documents/GitHub/Project_LISA/water irrigation/final_model/dtr.bin"
        )

    def __preProcessData(self, data: pd.Series):
        """converts pd.series data to numpy with columnTransformation, MinMaxScalar"""
        self.data = data.values
        self.data = self.ct.transform(self.data)
        self.data[:, 9:] = self.scalar.transform(self.data[:, 9:])
        self.data = np.asarray(self.data).astype("float32")
        return self.data

    def Predict(self, data: pd.Series):
        self.processedData = self.__preProcessData(data)
        return self.dtrModel.predict(self.processedData)


# dataset = pd.read_csv(
#     "C:/Users/ganes/OneDrive/Documents/GitHub/Project_LISA/water irrigation/storage_dataset/prototype_final_dataset.csv"
# )

# dataset.drop(UNWANTED_PARAMS, inplace=True, axis=1)
# dataset.dropna(inplace=True)
# dataset = dataset.iloc[:, 1:]

# data1 = dataset.iloc[3621:3622, :]
# print(data1)
# print(data1.shape)

# test = MoiturePrediction()
# print(test.Predict(data1))
