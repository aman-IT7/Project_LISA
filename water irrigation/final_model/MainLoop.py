import paho.mqtt.client as mqtt
import json
import datetime
import pandas as pd

MQTT_BROKER_LOCAL = "192.168.210.55"
MQTT_BROKER_PUBLIC = "broker.hivemq.com"
MQTT_PORT = 1883
TOPIC = "/node/id"


class MainLoop:
    def __init__(self, moisturePredictionModel, weatherApi):
        self.client = mqtt.Client()
        self.broker_address = MQTT_BROKER_PUBLIC
        self.port = MQTT_PORT
        self.topic = TOPIC
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.last_msg = None
        self.moisturePredictionModel = moisturePredictionModel
        self.weatherApi = weatherApi

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
        self.last_msg = json.loads(msg.payload.decode())
        try:
            node_data = self.__get_last_msg()
            if node_data:
                predictionTime = (datetime.now().hour + 3) % 23
                weatherData = self.__get_weather_data(predictionTime)
                formatedWeatherData = self.__format_weather_data(weatherData)
                formatedNodeData = self.__format_node_data(node_data)
                final_data = self.__final_format(formatedNodeData, formatedWeatherData)
                print(final_data)
                p_moisture = self.moisturePredictionModel.Predict(final_data)
                print(p_moisture)
        except Exception as Error:
            raise Error

    def connect_predict(self):
        self.client.connect(self.broker_address, self.port, 60)
        self.client.loop_forever()

    def __get_last_msg(self):
        return self.last_msg

    def disconnect(self):
        self.client.disconnect()

    def __get_weather_data(self, time: int):
        """get weather data"""
        weather_data = self.weatherApi.getData_current_weather()[time]
        return weather_data

    def __format_weather_data(self, weather_data: json):
        COLUMN_ORDER_WEATHER = [
            "precip",
            "windspeed",
            "cloudcover",
            "conditions",
        ]
        pd_data = pd.DataFrame(weather_data, index=[0])
        formatted_data = pd_data[COLUMN_ORDER_WEATHER]
        return formatted_data

    def __format_node_data(self, node_data):
        COLUMN_ORDER_NODE = [
            "SoilMoisture",
            "SoilTemp",
            "AmbientTemp",
            "AmbientHumidity",
        ]
        data = pd.DataFrame(node_data, index=[0])
        formatted_data = data[COLUMN_ORDER_NODE]
        formatted_data.rename(
            columns={
                "SoilMoisture": "SM_INI",
                "SoilTemp": "ST_4",
                "AmbientTemp": "temp",
                "AmbientHumidity": "humidity",
            },
            inplace=True,
        )
        return formatted_data

    def __final_format(
        self, node_data: pd.DataFrame, weather_data: pd.DataFrame
    ) -> pd.DataFrame:
        return pd.concat([node_data, weather_data], axis=1)
