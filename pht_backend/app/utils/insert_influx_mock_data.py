from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os

async def insert_influx_mock_data(client: InfluxDBClient):
    try:
        print("Inserting sensors readings mock data...")
        bucket = os.environ.get("INFLUX_BUCKET_NAME")
        write_api = client.write_api(write_options=SYNCHRONOUS)

        cities_ids = [1,2,3]
        sensors_ids = [1,2,3]

        for city in cities_ids:
            for sensor in sensors_ids:
                p = Point("city").tag(
                            "sensor", sensor).field(city, 21.37)
                write_api.write(bucket=bucket, record=p)
    except Exception as e:
        print(e)