from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.postgresql.exceptions.postgres_exceptions import (PostgreSQLDatabaseError, PostgreSQLNotFoundError)
from app.database.postgresql.repositories.sensors_repository import SensorsRepository
from app.database.postgresql.session.get_session import get_session

router = APIRouter()

@router.get("/sensors")
async def get_sensors(async_session: AsyncSession = Depends(get_session)):
    try:
        sensors_repository: SensorsRepository = SensorsRepository(async_session)
        sensors = await sensors_repository.get_sensors()
        sensors_list = []
        for sensor in sensors:
            sensor_data = {
                "id": sensor.id,
                "sensor_name": sensor.name,
                "unit": sensor.unit
            }
            sensors_list.append(sensor_data)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"sensors": sensors_list}))
    except PostgreSQLNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PostgreSQLDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Unspecified error occured: {e}")
        raise HTTPException(status_code=500, detail="Unspecified server error.")