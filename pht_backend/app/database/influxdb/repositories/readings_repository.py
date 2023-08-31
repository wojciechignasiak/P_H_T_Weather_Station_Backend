from influxdb_client import InfluxDBClient
from influxdb_client.client.flux_table import FluxTable
from influxdb_client.client.exceptions import InfluxDBError
from app.database.influxdb.exceptions.influx_exceptions import InfluxDatabaseError, InfluxNotFoundError
import os


class ReadingsRepository:
    def __init__(self, influx_client: InfluxDBClient):
        self._client = influx_client
        self._bucket = os.environ.get("INFLUX_BUCKET_NAME")
        self._query_api = self._client.query_api()

    async def get_readings_from_city_and_sensor(self, city_id, sensor_id, time_range=30):
        try:
            query = f' from(bucket: "{self._bucket}")\
                |> range(start: -{time_range}d)\
                |> filter(fn: (r) => r["_measurement"] == "city")\
                |> filter(fn: (r) => r["_field"] == "{city_id}")\
                |> filter(fn: (r) => r["sensor"] == "{sensor_id}")\
                |> last()'
            result: FluxTable = self._query_api.query(query=query)
            if result:
                results = {}
                for table in result:
                    for record in table.records:
                        results[record['sensor']] = record.get_value()
                return results
            else:
                raise InfluxNotFoundError("No measurements has been found.")
        except InfluxDBError as e:
            print(e)
            raise InfluxDatabaseError("Unspecified Influx Database error.")

    async def get_readings_from_city(self, city_id: int, time_range=30) -> dict:
        try:
            query = f'''
            from(bucket: "{self._bucket}")
            |> range(start: -{time_range}d)
            |> filter(fn: (r) => r["_measurement"] == "city")
            |> filter(fn: (r) => r["_field"] == "{city_id}")
            |> last()
            '''
            result: FluxTable = self._query_api.query(query=query)
            if result:
                results = {}
                for table in result:
                    for record in table.records:
                        results[record['sensor']] = record.get_value()
                return results
            else:
                raise InfluxNotFoundError("No measurements has been found.")
        except InfluxDBError as e:
            print(e)
            raise InfluxDatabaseError("Unspecified Influx Database error.")

    async def get_readings_from_city_and_specific_date(self, city_id, year, month, day, hour, minutes):
        try:
            hour = hour - 2
            if(month < 10):
                month = "0" + str(month)
            if(day < 10):
                day = "0" + str(day)
            if(hour < 10):
                hour = "0" + str(hour)
            if(minutes < 10):
                minutes = "0" + str(minutes)
            query = f'''
                from(bucket: "{self._bucket}")
                |> range(start: {year}-{month}-{day}T{hour}:{minutes}:00Z, stop: {year}-{month}-{day}T{hour}:{minutes}:59Z)
                |> filter(fn: (r) => r["_measurement"] == "city")
                |> filter(fn: (r) => r["_field"] == "{city_id}")
                |> last()
                '''
            result: FluxTable = self._query_api.query(query=query)
            print(result)
            if result:
                results = {}
                for table in result:
                    for record in table.records:
                        results[record['sensor']] = record.get_value()
                return results
            else:
                raise InfluxNotFoundError("No measurements has been found.")
        except InfluxDBError as e:
            print(e)
            raise InfluxDatabaseError("Unspecified Influx Database error.")