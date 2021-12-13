from influxdb_client import InfluxDBClient, Point
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

    def write_data(self, topic, payload):
        topic_data = topic.split("/")
        print(topic_data)
        payload_data = payload.decode()
        print(payload_data)
        p = Point(topic_data[1]).tag(
            topic_data[3], topic_data[4]).field(topic_data[2], payload_data)
        self._write_api.write(bucket=self._bucket, record=p)
