from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import session
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import ForeignKey

db_string = "postgresql://postgres:1234@localhost:5438"

db = create_engine(db_string)
base = declarative_base()


class Cities(base):
    __tablename__ = 'Cities'
    id = Column(Integer, unique=True, primary_key=True)
    city_name = Column(String)
    city_sensors = relationship("Sensors")


class Sensors(base):
    __tablename__ = 'Sensors'
    id = Column(Integer, unique=True, primary_key=True)
    sensor_name = Column(String)
    sensor_unit = Column(String)
    city_id = Column(Integer, ForeignKey('Cities.id'))


Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

czestochowa_city = Cities(city_name="Czestochowa")

myszkow_city = Cities(city_name="Myszkow")

krzepice_city = Cities(city_name="Krzepice")

session.add(czestochowa_city)
session.add(myszkow_city)
session.add(krzepice_city)
session.commit()


temperature_sensor1 = Sensors(sensor_name="temperature",
                              sensor_unit="Celsius",
                              city_id=1)

humidity_sensor1 = Sensors(sensor_name="humidity",
                           sensor_unit="precentage",
                           city_id=1)

pollution_sensor1 = Sensors(sensor_name="pollution",
                            sensor_unit="PM2.5",
                            city_id=1)

temperature_sensor2 = Sensors(sensor_name="temperature",
                              sensor_unit="Celsius",
                              city_id=2)

humidity_sensor2 = Sensors(sensor_name="humidity",
                           sensor_unit="precentage",
                           city_id=2)

pollution_sensor2 = Sensors(sensor_name="pollution",
                            sensor_unit="PM2.5",
                            city_id=2)

temperature_sensor3 = Sensors(sensor_name="temperature",
                              sensor_unit="Celsius",
                              city_id=3)

humidity_sensor3 = Sensors(sensor_name="humidity",
                           sensor_unit="precentage",
                           city_id=3)

pollution_sensor3 = Sensors(sensor_name="pollution",
                            sensor_unit="PM2.5",
                            city_id=3)


session.add(temperature_sensor1)
session.add(humidity_sensor1)
session.add(pollution_sensor1)

session.add(temperature_sensor2)
session.add(humidity_sensor2)
session.add(pollution_sensor2)

session.add(temperature_sensor3)
session.add(humidity_sensor3)
session.add(pollution_sensor3)

session.commit()
