from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, DataError
from app.database.postgresql.exceptions.postgres_exceptions import (PostgreSQLDatabaseError, PostgreSQLNotFoundError)
from app.schema.schema import Sensor
from sqlalchemy import select

class SensorsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get_sensors(self) -> list:
        try:
            statement = select(Sensor)
            result: list = await self.session.scalars(statement)
            sensors = result.all()
            if sensors:
                return sensors
            else:
                raise PostgreSQLNotFoundError("No sensors in database")
        except (IntegrityError, DataError) as e:
            print(e)
            raise PostgreSQLDatabaseError("Error related to database occured.")