import pytest
from app.database.postgresql.repositories.cities_repository import CitiesRepository
from app.database.postgresql.exceptions.postgres_exceptions import PostgreSQLDatabaseError, PostgreSQLNotFoundError
from app.schema.schema import City
from app.schema.schema import Sensor
from unittest.mock import Mock


@pytest.mark.asyncio
async def test_get_cities_success(city_object, 
                                mock_postgres_async_session):
    cities_repository = CitiesRepository(mock_postgres_async_session)

    mock_result = Mock()
    mock_result.all.return_value = [city_object]
    mock_postgres_async_session.scalars.return_value = mock_result

    cities = await cities_repository.get_cities()

    assert isinstance(cities, list)
    city = cities[0]
    assert isinstance(city, City)
    assert city.id == 1
    assert city.name == "city_name"
    assert isinstance(cities[0].sensors, list)
    sensor = cities[0].sensors[0]
    assert isinstance(sensor, Sensor)
    assert sensor.id == 1
    assert sensor.name == "sensor_name"
    assert sensor.unit == "unit_name"


@pytest.mark.asyncio
async def test_get_cities_not_found(mock_postgres_async_session):
    cities_repository = CitiesRepository(mock_postgres_async_session)

    mock_result = Mock()
    mock_result.all.return_value = []
    mock_postgres_async_session.scalars.return_value = mock_result

    with pytest.raises(PostgreSQLNotFoundError):
        await cities_repository.get_cities()


@pytest.mark.asyncio
async def test_get_cities_database_error(mock_postgres_async_session):
    cities_repository = CitiesRepository(mock_postgres_async_session)

    mock_postgres_async_session.scalars.side_effect = PostgreSQLDatabaseError('Test Error')

    with pytest.raises(PostgreSQLDatabaseError):
        await cities_repository.get_cities()