from bridge import Bridge

if __name__ == '__main__':
    print("started mqtt bridge")
    mqtt_connect = Bridge()
    print("connecting")
    mqtt_connect.run()
    print("listening")
