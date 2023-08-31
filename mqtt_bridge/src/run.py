from bridge import Bridge

if __name__ == '__main__':
    while True:
        print("Creating MQTT Bridge...")
        mqtt_connect = Bridge()
        print("Connecting to MQTT Broker...")
        mqtt_connect.run()
        print("Listening on MQTTT Broker messages...")
