from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.database.postgresql.session.get_session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.postgresql.exceptions.postgres_exceptions import (PostgreSQLDatabaseError, PostgreSQLNotFoundError)
from app.database.postgresql.repositories.cities_repository import CitiesRepository

router = APIRouter()

@router.get("/cities")
async def get_cities(async_session: AsyncSession = Depends(get_session)):
    try:
        cities_repository: CitiesRepository = CitiesRepository(async_session)
        cities = await cities_repository.get_cities()
        cities_list = []
        for city in cities:
            city_data = {
                "id": city.id,
                "city_name": city.name,
                "sensor_list": [sensor.id for sensor in city.sensors]
            }
            cities_list.append(city_data)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"cities":cities_list}))
    except PostgreSQLNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PostgreSQLDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Unspecified error occured: {e}")
        raise HTTPException(status_code=500, detail="Unspecified server error.")