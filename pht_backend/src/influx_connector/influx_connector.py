from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import os


class InfluxConnector:
    def __init__(self):
        self._token = os.environ.get("TOKEN")
        self._influx_url = os.environ.get("DB")
        self._org = os.environ.get("ORG")
        self._client = InfluxDBClient(
            url=f"http://{self._influx_url}:8086", token=self._token, org=self._org)
        self._bucket = os.environ.get("BUCKET_NAME")
        self._query_api = self._client.query_api()
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)
        print("influx connected")

    def get_data(self, city_id, sensor_id):
        query = f' from(bucket: "phtbucket")\
            |> range(start: -5m)\
            |> filter(fn: (r) => r["_measurement"] == "sensor")\
            |> filter(fn: (r) => r["_field"] == "{sensor_id}")\
            |> filter(fn: (r) => r["city"] == "{city_id}")'

        result = self._query_api.query(org=self._query_api, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_field(), record.get_value()))
        return results
