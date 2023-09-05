from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.database.influxdb.client.get_influx_client import get_influx_client
from influxdb_client import InfluxDBClient
from app.database.influxdb.repositories.readings_repository import ReadingsRepository
from app.database.influxdb.exceptions.influx_exceptions import InfluxDatabaseError, InfluxNotFoundError
from app.database.postgresql.session.get_session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.postgresql.repositories.sensors_repository import SensorsRepository
from app.database.postgresql.exceptions.postgres_exceptions import PostgreSQLDatabaseError, PostgreSQLNotFoundError
from app.utils.convert_datetime_for_influx import convert_datetime_for_influx


router = APIRouter()

@router.get("/readings/{city_id}")
async def get_readings_from_specific_city(city_id: int, 
                                    influx_client: InfluxDBClient = Depends(get_influx_client),
                                    async_session: AsyncSession = Depends(get_session)):
    try:
        
        readings_repository = ReadingsRepository(influx_client)
        city_readings = await readings_repository.get_readings_from_city(city_id)

        sensor_repository = SensorsRepository(async_session)
        sensors = await sensor_repository.get_sensors()
        
        result_dict = {}
        for sensor in sensors:
            if str(sensor.id) in city_readings:
                result_dict[sensor.name] = city_readings[str(sensor.id)]

        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result_dict))
    except (InfluxNotFoundError, PostgreSQLNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (InfluxDatabaseError, PostgreSQLDatabaseError) as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Unspecified error occured: {e}")
        raise HTTPException(status_code=500, detail="Unspecified server error.")


@router.get("/readings/{city_id}/{sensor_id}")
async def get_specific_sensor_readings_from_specific_city(city_id: int, 
                                                        sensor_id: int,
                                                        influx_client: InfluxDBClient = Depends(get_influx_client),
                                                        async_session: AsyncSession = Depends(get_session)):
    try:
        
        readings_repository = ReadingsRepository(influx_client)
        city_readings = await readings_repository.get_readings_from_city_and_sensor(city_id, sensor_id)

        sensor_repository = SensorsRepository(async_session)
        sensors = await sensor_repository.get_sensors()
        
        result_dict = {}
        for sensor in sensors:
            if str(sensor.id) in city_readings:
                result_dict[sensor.name] = city_readings[str(sensor.id)]

        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result_dict))
    except (InfluxNotFoundError, PostgreSQLNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (InfluxDatabaseError, PostgreSQLDatabaseError) as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Unspecified error occured: {e}")
        raise HTTPException(detail="Unspecified server error.")

@router.get("/readings-date/{city_id}/{year}-{month}-{day}T{hour}:{minutes}:00Z")
async def get_readings_from_specific_city_and_date(city_id: int,
                                                    year: int,
                                                    month: int,
                                                    day: int,
                                                    hour: int,
                                                    minutes: int,
                                                    influx_client: InfluxDBClient = Depends(get_influx_client),
                                                    async_session: AsyncSession = Depends(get_session)):
    try:
        datetime_dict = await convert_datetime_for_influx(year, month, day, hour, minutes)

        readings_repository = ReadingsRepository(influx_client)
        city_readings = await readings_repository.get_readings_from_city_and_specific_date(city_id, datetime_dict["year"], datetime_dict["month"], datetime_dict["day"], datetime_dict["hour"], datetime_dict["minutes"])

        sensor_repository = SensorsRepository(async_session)
        sensors = await sensor_repository.get_sensors()
        
        result_dict = {}
        for sensor in sensors:
            if str(sensor.id) in city_readings:
                result_dict[sensor.name] = city_readings[str(sensor.id)]

        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result_dict))
    except (InfluxNotFoundError, PostgreSQLNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (InfluxDatabaseError, PostgreSQLDatabaseError) as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Unspecified error occured: {e}")
        raise HTTPException(status_code=500, detail="Unspecified server error.")