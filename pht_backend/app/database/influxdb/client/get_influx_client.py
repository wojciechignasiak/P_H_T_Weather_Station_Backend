from fastapi import Request
from influxdb_client import InfluxDBClient

async def get_influx_client(request: Request) -> InfluxDBClient:
        yield request.app.state.influx_client