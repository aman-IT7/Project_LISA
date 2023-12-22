# This Module is used to publish predicted moisture and all the parameters to the database using mqtt

from paho.mqtt import client as mqtt_client
import time

MQTT_BROKER_LOCAL = "192.168.210.55"
MQTT_BROKER_PUBLIC = "broker.hivemq.com"
MQTT_PORT = 1883


class MqttPublisher:
    def __init__(self, debug=False):
        self.broker = MQTT_BROKER_PUBLIC
        self.port = MQTT_PORT
        self.debug = debug
        self.client = self.create_mqtt_client()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    def create_mqtt_client(self):
        client = mqtt_client.Client()

        if self.debug:
            client.on_connect = self.on_connect

        try:
            client.connect(self.broker, self.port)
        except Exception as e:
            print(f"Error connecting to MQTT Broker: {e}")

        return client

    def publish(self, msg, topic):
        time.sleep(1)
        result = self.client.publish(topic, msg, retain=False)
        status = result[0]
        if status == 0:
            print(f"Sent {msg} to topic {topic}")
        else:
            print(f"Failed to send message to topic {topic}")

    def send_message(self, data, topic):
        self.client.loop_start()
        self.publish(data, topic)
