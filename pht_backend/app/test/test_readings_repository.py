import pytest
from app.database.influxdb.repositories.readings_repository import ReadingsRepository
from influxdb_client.client.flux_table import FluxRecord
from app.database.influxdb.exceptions.influx_exceptions import InfluxDatabaseError, InfluxNotFoundError


@pytest.mark.asyncio
async def test_get_readings_from_city_and_sensor_success(mock_influx_client, mock_flux_table):
    readings_repository = ReadingsRepository(mock_influx_client)

    mock_record = FluxRecord(0, {'sensor': '1', '_value': 21.37})
    mock_flux_table.records = [mock_record]
    mock_influx_client.query_api().query.return_value = [mock_flux_table]
    
    readings = await readings_repository.get_readings_from_city_and_sensor(city_id=1, sensor_id=1, time_range=30)
    
    assert isinstance(readings, dict)
    assert readings == {'1': 21.37}


@pytest.mark.asyncio
async def test_get_readings_from_city_and_sensor_not_found(mock_influx_client):
    readings_repository = ReadingsRepository(mock_influx_client)

    mock_influx_client.query_api().query.return_value = []
    
    with pytest.raises(InfluxNotFoundError):
        await readings_repository.get_readings_from_city_and_sensor(city_id=1, sensor_id=1, time_range=30)


@pytest.mark.asyncio
async def test_get_readings_from_city_and_sensor_database_error(mock_influx_client):
    readings_repository = ReadingsRepository(mock_influx_client)

    mock_influx_client.query_api().query.side_effect = InfluxDatabaseError("Test error")

    with pytest.raises(InfluxDatabaseError):
        await readings_repository.get_readings_from_city_and_sensor(city_id=1, sensor_id=1, time_range=30)


@pytest.mark.asyncio
async def test_get_readings_from_city_success(mock_influx_client, mock_flux_table):
    readings_repository = ReadingsRepository(mock_influx_client)

    mock_record1 = FluxRecord(0, {'sensor': '1', '_value': 21.37})
    mock_record2 = FluxRecord(0, {'sensor': '2', '_value': 37.21})
    mock_record3 = FluxRecord(0, {'sensor': '3', '_value': 71.23})
    
    mock_flux_table.records = [mock_record1, mock_record2, mock_record3]
    mock_influx_client.query_api().query.return_value = [mock_flux_table]

    readings = await readings_repository.get_readings_from_city(city_id=1)
    
    assert isinstance(readings, dict)
    assert readings == {'1': 21.37, '2': 37.21, '3': 71.23}


@pytest.mark.asyncio
async def test_get_readings_from_city_not_found(mock_influx_client):
    readings_repository = ReadingsRepository(mock_influx_client)
    
    mock_influx_client.query_api().query.return_value = []

    with pytest.raises(InfluxNotFoundError):
        await readings_repository.get_readings_from_city(city_id=1)


@pytest.mark.asyncio
async def test_get_readings_from_city_database_error(mock_influx_client):
    readings_repository = ReadingsRepository(mock_influx_client)

    mock_influx_client.query_api().query.side_effect = InfluxDatabaseError("Test error")

    with pytest.raises(InfluxDatabaseError):
        await readings_repository.get_readings_from_city(city_id=1)


@pytest.mark.asyncio
async def test_get_readings_from_city_and_specific_date_success(mock_influx_client, mock_flux_table):
    readings_repository = ReadingsRepository(mock_influx_client)

    mock_record1 = FluxRecord(0, {'sensor': '1', '_value': 21.37})
    mock_record2 = FluxRecord(0, {'sensor': '2', '_value': 37.21})
    mock_record3 = FluxRecord(0, {'sensor': '3', '_value': 71.23})

    mock_flux_table.records = [mock_record1, mock_record2, mock_record3]
    mock_influx_client.query_api().query.return_value = [mock_flux_table]

    readings = await readings_repository.get_readings_from_city_and_specific_date(city_id=1, year="2023", month="08", day="31", hour="10", minutes="11")
    
    assert isinstance(readings, dict)
    assert readings == {'1': 21.37, '2': 37.21, '3': 71.23}


@pytest.mark.asyncio
async def test_get_readings_from_city_and_specific_date_not_found(mock_influx_client):
    readings_repository = ReadingsRepository(mock_influx_client)
    
    mock_influx_client.query_api().query.return_value = []

    with pytest.raises(InfluxNotFoundError):
        await readings_repository.get_readings_from_city_and_specific_date(city_id=1, year="2023", month="08", day="31", hour="10", minutes="11")


@pytest.mark.asyncio
async def test_get_readings_from_city_and_specific_date_database_error(mock_influx_client):
    readings_repository = ReadingsRepository(mock_influx_client)
    
    mock_influx_client.query_api().query.side_effect = InfluxDatabaseError("Test error")

    with pytest.raises(InfluxDatabaseError):
        await readings_repository.get_readings_from_city_and_specific_date(city_id=1, year="2023", month="08", day="31", hour="10", minutes="11")
