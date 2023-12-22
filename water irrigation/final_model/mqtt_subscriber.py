import paho.mqtt.client as mqtt
from time import sleep

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
        self.last_msg = msg.payload.decode()

    def connect(self):
        self.client.connect(self.broker_address, self.port, 60)

    def get_last_msg(self):
        return self.last_msg

    def disconnect(self):
        self.client.disconnect()
