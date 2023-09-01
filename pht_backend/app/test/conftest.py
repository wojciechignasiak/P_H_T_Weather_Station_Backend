import pytest
from unittest.mock import Mock
from sqlalchemy.ext.asyncio import AsyncSession
from influxdb_client import InfluxDBClient
from influxdb_client.client.flux_table import FluxTable
from app.schema.schema import City
from app.schema.schema import Sensor

@pytest.fixture
def mock_postgres_async_session():
    return Mock(spec=AsyncSession)

@pytest.fixture
def sensor_object():
    return Sensor(id=1, name="sensor_name", unit="unit_name")

@pytest.fixture
def city_object(sensor_object):
    return City(id=1, name="city_name", sensors=[sensor_object])

@pytest.fixture
def mock_influx_client():
    return Mock(spec=InfluxDBClient)

@pytest.fixture
def mock_flux_table():
    return Mock(spec=FluxTable)