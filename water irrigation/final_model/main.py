from dependancies import *
from MainLoop import MainLoop
from VisualCrossingAPI import *


if __name__ == "__main__":
    moisturePredictionModel = MoiturePrediction()
    weatherApi = VisualCrossingAPI()
    ml = MainLoop(moisturePredictionModel, weatherApi)
    ml.connect_predict()
