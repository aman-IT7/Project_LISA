""" This module is used to store data loaclly in mongoDB """


import pymongo
import visual_crossing_weather_api

weatherAPI = visual_crossing_weather_api.VisualCrossingAPI()
file_name = weatherAPI.filename
mongoClient = pymongo.MongoClient("mongodb://localhost:27017")


mongoDB = mongoClient.get_database("learning")
learningCOL = mongoDB["weatherdata"]

data = weatherAPI.getData_current_weather()
# Rertrieve the todays weather data and insert it into locat database
learningCOL.insert_one(data)
