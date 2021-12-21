from influxdb_client import InfluxDBClient
import os


class InfluxConnector:
    def __init__(self):
        self._token = os.environ.get("INFLUX_TOKEN")
        self._influx_url = os.environ.get("INFLUX")
        self._org = os.environ.get("ORG")
        self._client = InfluxDBClient(
            url=f"http://{self._influx_url}:8086", token=self._token, org=self._org)
        self._bucket = os.environ.get("BUCKET_NAME")
        self._query_api = self._client.query_api()
        print("Influx connected")

    def get_sensor_data(self, city_id, sensor_id, time_range=30):
        query = f' from(bucket: "phtbucket")\
            |> range(start: -{time_range}d)\
            |> filter(fn: (r) => r["_measurement"] == "city")\
            |> filter(fn: (r) => r["_field"] == "{city_id}")\
            |> filter(fn: (r) => r["sensor"] == "{sensor_id}")\
            |> last()'
        result = self._query_api.query(query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append(record.get_value())
        return results

    def get_city_data(self, city_id, time_range=30):
        query = f' from(bucket: "phtbucket")\
            |> range(start: -{time_range}d)\
            |> filter(fn: (r) => r["_measurement"] == "city")\
            |> filter(fn: (r) => r["_field"] == "{city_id}")\
            |> last()'
        result = self._query_api.query(query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append(record.get_value())
        return results

    def get_city_data_from_date(self, city_id, year, month, day, hour, minutes):
        query = f' from(bucket: "phtbucket")\
            |> range(start: {year}-{month}-{day}T{hour}:{minutes}:00Z, stop: {year}-{month}-{day}T{hour}:{minutes}:59Z)\
            |> filter(fn: (r) => r["_measurement"] == "city")\
            |> filter(fn: (r) => r["_field"] == "{city_id}")\
            |> last()'
        result = self._query_api.query(query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append(record.get_value())
        return results
