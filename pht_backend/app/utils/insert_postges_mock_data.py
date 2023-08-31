from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.schema.schema import City, Sensor

async def insert_postgres_mock_data(db_string):
    engine = create_async_engine(db_string)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        try:
            print("Inserting cities and sensors mock data...")
            mock_city_tuple = ("Czestochowa", "Myszkow", "Krzepice")
            mock_sensor_dict = {
                                "Temperature": "Celsius", 
                                "Humidity": "Percentage", 
                                "Pollution": "PM2.5"
                                }

            cities_object_list = []
            for mock_city in mock_city_tuple:
                cities_object_list.append(City(name=mock_city))

            sensors_object_list = []
            for k in mock_sensor_dict:
                sensors_object_list.append(Sensor(name=k, unit=mock_sensor_dict[k]))

            for city_object in cities_object_list:
                city_object.sensors = sensors_object_list

            session.add_all(cities_object_list)
            session.add_all(sensors_object_list)

            await session.commit()

        except Exception as e:
            print(e)
            await session.flush()
            await session.rollback()
