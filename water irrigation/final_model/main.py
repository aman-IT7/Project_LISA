import pandas as pd
from dependancies import *
import paho.mqtt.client as mqtt
from mqtt_subscriber import MqttClient
from VisualCrossingAPI import *
import paho.mqtt.client as mqtt

MQTT_BROKER_LOCAL = "192.168.210.55"
MQTT_BROKER_PUBLIC = "broker.hivemq.com"
MQTT_PORT = 1883
TOPIC = "/node/id"


class MqttClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.broker_address = MQTT_BROKER_PUBLIC
        self.port = MQTT_PORT
        self.topic = TOPIC
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.last_msg = None

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
        self.last_msg = json.loads(msg.payload.decode())
        try:
            print("test")
            node_data = rm.get_last_msg()
            if node_data:
                wd = get_weather_data(23)
                wd = format_weather_data(wd)
                nd = format_node_data(node_data)
                final_data = final_format(nd, wd)
                print(final_data)
                print()
                p_moisture = predicted_moisture.Predict(final_data)
                print(p_moisture)
                print()
        except Exception as Error:
            raise Error

    def connect(self):
        self.client.connect(self.broker_address, self.port, 60)
        self.client.loop_forever()

    def get_last_msg(self):
        return self.last_msg

    def disconnect(self):
        self.client.disconnect()


def get_weather_data(time: int):
    """get weather data"""
    weather_data = weather_api.getData_current_weather()[time]
    return weather_data


def format_weather_data(weather_data: json):
    COLUMN_ORDER_WEATHER = [
        "precip",
        "windspeed",
        "cloudcover",
        "conditions",
    ]
    pd_data = pd.DataFrame(weather_data, index=[0])
    formatted_data = pd_data[COLUMN_ORDER_WEATHER]
    return formatted_data


def format_node_data(node_data):
    COLUMN_ORDER_NODE = ["SoilTemp", "AmbientTemp", "AmbientHumidity"]
    data = pd.DataFrame(node_data, index=[0])
    formatted_data = data[COLUMN_ORDER_NODE]
    formatted_data.rename(
        columns={
            "SoilTemp": "ST_4",
            "AmbientTemp": "temp",
            "AmbientHumidity": "humidity",
        },
        inplace=True,
    )
    return formatted_data


def final_format(node_data: pd.DataFrame, weather_data: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([node_data, weather_data], axis=1)


if __name__ == "__main__":
    predicted_moisture = MoiturePrediction()
    weather_api = VisualCrossingAPI()
    rm = MqttClient()
    rm.connect()
