from dependancies import *
from VisualCrossingAPI import *
from MainLoop import MainLoop
import newMainLoop

if __name__ == "__main__":
    # moisturePredictionModel = MoiturePrediction()
    # weatherApi = VisualCrossingAPI_()
    # ml = MainLoop(moisturePredictionModel, weatherApi)
    # ml.connect_predict()
    newMainLoop.MainLoop_().connectPredict()
