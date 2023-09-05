from fastapi.testclient import TestClient
from app.main import app
from app.database.influxdb.client.get_influx_client import get_influx_client
from unittest.mock import Mock
import pytest
from influxdb_client import InfluxDBClient
from app.database.influxdb.exceptions.influx_exceptions import InfluxDatabaseError, InfluxNotFoundError
from influxdb_client.client.flux_table import FluxTable, FluxRecord
from app.test.test_sensors_router import dependency_get_sensors

client = TestClient(app)

async def override_dependency_get_readings_success():
    mock_influx_client = Mock(spec=InfluxDBClient)
    mock_record = FluxRecord(0, {'sensor': '1', '_value': 21.37})
    mock_flux_table = Mock(spec=FluxTable)
    mock_flux_table.records = [mock_record]
    mock_influx_client.query_api().query.return_value = [mock_flux_table]
    return mock_influx_client

async def override_dependency_get_readings_not_found():
    mock_influx_client = Mock(spec=InfluxDBClient)
    mock_influx_client.query_api().query.side_effect = InfluxNotFoundError('Test Error')
    return mock_influx_client

async def override_dependency_get_readings_error():
    mock_influx_client = Mock(spec=InfluxDBClient)
    mock_influx_client.query_api().query.side_effect = InfluxDatabaseError('Test Error')
    return mock_influx_client

async def dependency_get_readings(result: str):
    if result == "200":
        app.dependency_overrides[get_influx_client] = override_dependency_get_readings_success
    if result == "404":
        app.dependency_overrides[get_influx_client] = override_dependency_get_readings_not_found
    if result == "500":
        app.dependency_overrides[get_influx_client] = override_dependency_get_readings_error


@pytest.mark.asyncio
async def test_get_readings_from_specific_city_success():
    await dependency_get_readings("200")
    await dependency_get_sensors("200")

    response = client.get("/readings/1")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_readings_from_specific_city_not_found():
    await dependency_get_readings("404")
    await dependency_get_sensors("200")

    response = client.get("/readings/1")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_readings_from_specific_city_error():
    await dependency_get_readings("500")
    await dependency_get_sensors("200")

    response = client.get("/readings/1")
    assert response.status_code == 500


@pytest.mark.asyncio
async def test_get_specific_sensor_readings_from_specific_city_success():
    await dependency_get_readings("200")
    await dependency_get_sensors("200")

    response = client.get("/readings/1/1")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_specific_sensor_readings_from_specific_city_not_found():
    await dependency_get_readings("404")
    await dependency_get_sensors("200")

    response = client.get("/readings/1/1")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_specific_sensor_readings_from_specific_city_error():
    await dependency_get_readings("500")
    await dependency_get_sensors("200")

    response = client.get("/readings/1/1")
    assert response.status_code == 500


@pytest.mark.asyncio
async def test_get_readings_from_specific_city_and_date_success():
    await dependency_get_readings("200")
    await dependency_get_sensors("200")

    response = client.get("/readings-date/1/2023-09-01T16:15:00Z")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_readings_from_specific_city_and_date_not_found():
    await dependency_get_readings("404")
    await dependency_get_sensors("200")

    response = client.get("/readings-date/1/2023-09-01T16:15:00Z")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_readings_from_specific_city_and_date_error():
    await dependency_get_readings("500")
    await dependency_get_sensors("200")

    response = client.get("/readings-date/1/2023-09-01T16:15:00Z")
    assert response.status_code == 500