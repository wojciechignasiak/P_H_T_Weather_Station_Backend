from influxdb import InfluxDBClient
client = InfluxDBClient(host='localhost', port=8086)

print(client)

client.create_database('pyexample')
client.get_list_database()
client.switch_database('pyexample')
