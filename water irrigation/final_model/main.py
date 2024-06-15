from dependancies import *
from VisualCrossingAPI import *
from MainLoop import MainLoop

if __name__ == "__main__":
    moisturePredictionModel = MoiturePrediction()
    weatherApi = VisualCrossingAPI_()
    ml = MainLoop(moisturePredictionModel, weatherApi)
    try:
        ml.connect_predict()
    except Exception as err:
        print(f"Error occured -> {err.__str__()}")
        # newMainLoop.MainLoop_().connectPredict()
