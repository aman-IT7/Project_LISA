import pymongo
import visual_crossing_weather_api
import json


weatherAPI = visual_crossing_weather_api.VisualCrossingAPI()
file_name = weatherAPI.filename
mongoClient = pymongo.MongoClient("mongodb://localhost:27017")


mongoDB = mongoClient.get_database("learning")
learningCOL = mongoDB["weatherdata"]

with open(file_name, 'r') as file:
    data = json.load(file)
    learningCOL.insert_one(data)
