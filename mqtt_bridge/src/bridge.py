from influx_connector import InfluxConnector
import paho.mqtt.client as mqtt
import os


class Bridge(mqtt.Client):
    def __init__(self):
        super().__init__()
        print("MqttConnect init")
        self._influx_connector = InfluxConnector()
        self._broker_url = os.environ.get("BROKER")

    def run(self):
        self.connect(self._broker_url, 1883)
        self.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.subscribe("#")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        self._influx_connector.write_data(msg.topic, msg.payload)
