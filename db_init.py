from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy.orm.session import Session
from models import City, Sensor, base


db_string = "postgresql://postgres:1234@localhost:5438"

db = create_engine(db_string)

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

czestochowa_city = City(name="Czestochowa")

myszkow_city = City(name="Myszkow")

krzepice_city = City(name="Krzepice")

temperature_sensor = Sensor(name="temperature",
                            unit="Celsius")

humidity_sensor = Sensor(name="humidity",
                         unit="precentage")

pollution_sensor = Sensor(name="pollution",
                          unit="PM2.5")

czestochowa_city.sensors = [temperature_sensor,
                            humidity_sensor, pollution_sensor]
myszkow_city.sensors = [temperature_sensor,
                        humidity_sensor, pollution_sensor]
krzepice_city.sensors = [temperature_sensor,
                         humidity_sensor, pollution_sensor]


session.add(czestochowa_city)
session.add(myszkow_city)
session.add(krzepice_city)
session.add(temperature_sensor)
session.add(humidity_sensor)
session.add(pollution_sensor)


session.commit()
