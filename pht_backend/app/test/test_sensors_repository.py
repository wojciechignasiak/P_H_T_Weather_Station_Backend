import pytest
from app.database.postgresql.repositories.sensors_repository import SensorsRepository
from app.database.postgresql.exceptions.postgres_exceptions import PostgreSQLDatabaseError, PostgreSQLNotFoundError
from app.schema.schema import Sensor
from unittest.mock import Mock


@pytest.mark.asyncio
async def test_get_sensors_success(sensor_object, 
                                mock_postgres_async_session):
    sensors_repository = SensorsRepository(mock_postgres_async_session)

    mock_result = Mock()
    mock_result.all.return_value = [sensor_object]
    mock_postgres_async_session.scalars.return_value = mock_result

    sensors = await sensors_repository.get_sensors()

    assert isinstance(sensors, list)
    sensor = sensors[0]
    assert isinstance(sensor, Sensor)
    assert sensor.id == 1
    assert sensor.name == "sensor_name"
    assert sensor.unit == "unit_name"


@pytest.mark.asyncio
async def test_get_sensors_not_found(mock_postgres_async_session):
    sensors_repository = SensorsRepository(mock_postgres_async_session)

    mock_result = Mock()
    mock_result.all.return_value = []
    mock_postgres_async_session.scalars.return_value = mock_result

    with pytest.raises(PostgreSQLNotFoundError):
        await sensors_repository.get_sensors()


@pytest.mark.asyncio
async def test_get_sensors_database_error(mock_postgres_async_session):
    sensors_repository = SensorsRepository(mock_postgres_async_session)

    mock_postgres_async_session.scalars.side_effect = PostgreSQLDatabaseError("Error Test")

    with pytest.raises(PostgreSQLDatabaseError):
        await sensors_repository.get_sensors()

