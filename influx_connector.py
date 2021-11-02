from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

mytoken = 'MvDHUN7TnU3-vdsdBDvLDnTRPmVdz6DewHXGCEqAnAjT-PnH13dhpmf2jqD4Ifo2UVVh_O4rEwtOV7mvg-Xz_A=='
client = InfluxDBClient(url="http://localhost:8086", token=mytoken, org="pht")
bucket = 'phtbucket'

print(client)

query_api = client.query_api()


write_api = client.write_api(write_options=SYNCHRONOUS)

p = Point("sensor_reading").tag(
    "location", "Czestochowa").field("temperature", 1000000.3).field("humidity", 60).field("pollution", 30)

write_api.write(bucket=bucket, record=p)

tables = query_api.query(f'from(bucket:"{bucket}") |> range(start: -10m)')

for table in tables:
    print(table)

    for row in table.records:
        print(row.values)
