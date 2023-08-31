from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, DataError
from app.database.postgresql.exceptions.postgres_exceptions import (PostgreSQLDatabaseError, PostgreSQLNotFoundError)
from app.schema.schema import City
from sqlalchemy import select
from sqlalchemy.orm import subqueryload

class CitiesRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get_cities(self) -> list:
        try:
            statement = select(City).options(subqueryload(City.sensors))
            result = await self.session.scalars(statement)
            cities = result.all()
            if cities:
                return cities
            else:
                raise PostgreSQLNotFoundError("No cities in database.")
        except (IntegrityError, DataError) as e:
            print(e)
            raise PostgreSQLDatabaseError("Error related to database occured.")
