import datetime
import json
import pandas as pd
from paho.mqtt.client import Client
from VisualCrossingAPI import VisualCrossingAPI_
from dependancies import MoiturePrediction


class MainLoop_(Client, VisualCrossingAPI_, MoiturePrediction):
    MQTT_BROKER_LOCAL = "192.168.210.55"
    MQTT_BROKER_PUBLIC = "broker.hivemq.com"
    MQTT_PORT = 1883
    TOPIC = "/node/id"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_connect(self, client, userdata, flags, rc):
        # This callback function is called when we establish connection using connectPredict
        # after connecting to the broker we subscribe to a topic

        print("Connected with result code " + str(rc))
        self.subscribe(self.TOPIC)

    def on_message(self, client, userdata, msg):
        # this callback function is called when we recieve data from the topic we subscribed to
        # this is the core of retrieving ,predicting ,and storing data to database happens

        print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
        try:
            node_data = json.loads(msg.payload.decode())
            if node_data:
                predictionTime = (
                    datetime.now().hour + 3
                ) % 23  # current hour + 3hrs and then moding it with 23 so it remains in 24hr timeformat and dosent exceed 24+
                formatedWeatherData = self._get_weather_data(predictionTime)
                formatedNodeData = self.__format_node_data(node_data)
                final_data = self.__final_format(
                    formatedNodeData, formatedWeatherData)
                print(final_data)
                p_moisture = self.predictMositure(final_data)
                print(p_moisture)
        except Exception as Error:
            raise Error

    def connectPredict(self):
        # The method which will start the system (essentially main function)
        self.connect(self.MQTT_BROKER_PUBLIC, self.MQTT_PORT, 60)
        self.loop_forever()

    def disconnect(self):
        self.disconnect()

    def _get_weather_data(self, time: int):
        """get weather data"""
        weather_data = self.getData_current_weather()[time]
        return self.__format_weather_data(weather_data)

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
