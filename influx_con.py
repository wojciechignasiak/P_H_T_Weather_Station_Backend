from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

mytoken = 'nllRPbBwfCSFVGDcLmJqlc3eqmb3wl6r7ZYUt0x28HaSao78cyOqhgPrqOi_PGqsedrs1N9x48CHzSSl5jZ7Fw=='
client = InfluxDBClient(url="http://localhost:8086", token=mytoken, org="pht")
bucket = 'phtbucket'

print(client)

query_api = client.query_api()


write_api = client.write_api(write_options=SYNCHRONOUS)

p = Point("sensor_reading").tag(
    "location", "Czestochowa").field("temperature", 10.3).field("humidity", 60).field("pollution", 30)

write_api.write(bucket=bucket, record=p)

tables = query_api.query(f'from(bucket:"{bucket}") |> range(start: -10m)')

for table in tables:
    print(table)

    for row in table.records:
        print(row.values)
