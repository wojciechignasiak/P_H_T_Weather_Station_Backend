from fastapi.testclient import TestClient
from app.main import app
from app.database.postgresql.session.get_session import get_session
from unittest.mock import Mock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.schema import City
from app.schema.schema import Sensor
from app.database.postgresql.exceptions.postgres_exceptions import PostgreSQLDatabaseError, PostgreSQLNotFoundError

client = TestClient(app)

async def override_dependency_get_cities_success():
    mock_postgres_async_session = Mock(spec=AsyncSession)
    mock_result = Mock()
    mock_result.all.return_value = [City(id=1, name="city_name", sensors=[Sensor(id=1, name="sensor_name", unit="unit_name")])]
    mock_postgres_async_session.scalars.return_value = mock_result
    return mock_postgres_async_session

async def override_dependency_get_cities_not_found():
    mock_postgres_async_session = Mock(spec=AsyncSession)
    mock_postgres_async_session.scalars.side_effect = PostgreSQLNotFoundError('Test Error')
    return mock_postgres_async_session

async def override_dependency_get_cities_error():
    mock_postgres_async_session = Mock(spec=AsyncSession)
    mock_postgres_async_session.scalars.side_effect = PostgreSQLDatabaseError('Test Error')
    return mock_postgres_async_session

async def dependency_get_cities(result: str):
    if result == "200":
        app.dependency_overrides[get_session] = override_dependency_get_cities_success
    if result == "404":
        app.dependency_overrides[get_session] = override_dependency_get_cities_not_found
    if result == "500":
        app.dependency_overrides[get_session] = override_dependency_get_cities_error


################Testing /get_cities 200 response################

@pytest.mark.asyncio
async def test_get_cities_success():
    await dependency_get_cities("200")

    response = client.get("/cities")
    assert response.status_code == 200
    data = response.json()
    assert "cities" in data
    assert isinstance(data["cities"], list)

################Testing /get_cities 404 response################

@pytest.mark.asyncio
async def test_get_cities_not_found():
    await dependency_get_cities("404")

    response = client.get("/cities")
    assert response.status_code == 404

################Testing /get_cities 500 response################

@pytest.mark.asyncio
async def test_get_cities_error():
    await dependency_get_cities("500")

    response = client.get("/cities")
    assert response.status_code == 500