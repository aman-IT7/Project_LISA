from paho.mqtt import client as mqtt_client
import time

MQTT_BROKER = "192.168.210.55"
MQTT_PORT = 1883


def create_mqtt_client(broker, port, debug):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client()

    if debug:
        client.on_connect = on_connect

    try:
        client.connect(broker, port)
    except Exception as e:
        print(f"Error connecting to MQTT Broker: {e}")

    return client


def publish(client, msg, topic):
    time.sleep(1)
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Sent {msg} to topic {topic}")
    else:
        print(f"Failed to send message to topic {topic}")


def send_message(data, topic, debug=False):
    client = create_mqtt_client(MQTT_BROKER, MQTT_PORT, debug)
    client.loop_start()
    publish(client, data, topic)
