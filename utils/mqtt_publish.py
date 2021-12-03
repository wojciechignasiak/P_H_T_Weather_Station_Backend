import paho.mqtt.client as paho
broker = "localhost"
port = 1883


def on_publish(client, userdata, result):
    print("data published \n")
    pass


client1 = paho.Client("control1")
client1.on_publish = on_publish
client1.connect(broker, port)
ret = client1.publish("pht/city/{city_id}/sensor/{sensor_id}", 6.2)
# ret1 = client1.publish("pht/Czestochowa/humidity", 60.1)
# ret2 = client1.publish("pht/Czestochowa/pollution", 17.8)
# ret3 = client1.publish("pht/Myszkow/temperature", 7.1)
# ret4 = client1.publish("pht/Myszkow/humidity", 55.2)
# ret5 = client1.publish("pht/Myszkow/pollution", 10.2)
# ret6 = client1.publish("pht/Krzepice/temperature", 5.1)
# ret7 = client1.publish("pht/Krzepice/humidity", 40.7)
# ret8 = client1.publish("pht/Krzepice/pollution", 12.9)
