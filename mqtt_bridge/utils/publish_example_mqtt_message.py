import paho.mqtt.client as paho
import os

broker = os.environ.get("MQTT_BROKER_HOST")
port = int(os.environ.get("MQTT_BROKER_PORT"))


def on_publish(client, userdata, result):
    print("data published \n")
    pass


city_id = 3
sensor_id = 2

client1 = paho.Client("control1")
client1.on_publish = on_publish
client1.connect(broker, port)
ret = client1.publish(f"pht/city/{city_id}/sensor/{1}", 4)
ret = client1.publish(f"pht/city/{city_id}/sensor/{2}", 5)
ret = client1.publish(f"pht/city/{city_id}/sensor/{3}", 6)

city_id = 1
ret = client1.publish(f"pht/city/{city_id}/sensor/{1}", 4)
ret = client1.publish(f"pht/city/{city_id}/sensor/{2}", 5)
ret = client1.publish(f"pht/city/{city_id}/sensor/{3}", 6)

city_id = 2
ret = client1.publish(f"pht/city/{city_id}/sensor/{1}", 4)
ret = client1.publish(f"pht/city/{city_id}/sensor/{2}", 5)
ret = client1.publish(f"pht/city/{city_id}/sensor/{3}", 6)
