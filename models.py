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
    city_id = Column(Integer, unique=True, primary_key=True)
    city_name = Column(String)
    city_sensors_list = Column(ARRAY(Integer))


class Sensors(base):
    __tablename__ = 'Sensors'
    sensor_id = Column(Integer, unique=True, primary_key=True)
    sensor_name = Column(String)
    sensor_unit = Column(String)


Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

temperature_sensor = Sensors(sensor_id=0,
                             sensor_name="temperature",
                             sensor_unit="Celsius")

humidity_sensor = Sensors(sensor_id=1,
                          sensor_name="humidity",
                          sensor_unit="precentage")

pollution_sensor = Sensors(sensor_id=2,
                           sensor_name="pollution",
                           sensor_unit="PM2.5")

session.add(temperature_sensor)
session.add(humidity_sensor)
session.add(pollution_sensor)
session.commit()

czestochowa_city = Cities(city_id=0,
                          city_name="Czestochowa",
                          city_sensors_list=[
                              temperature_sensor.sensor_id,
                              humidity_sensor.sensor_id,
                              pollution_sensor.sensor_id
                          ])

myszkow_city = Cities(city_id=1,
                      city_name="Myszkow",
                      city_sensors_list=[
                          temperature_sensor.sensor_id,
                          humidity_sensor.sensor_id, pollution_sensor.sensor_id
                      ])

krzepice_city = Cities(city_id=2,
                       city_name="Krzepice",
                       city_sensors_list=[
                           temperature_sensor.sensor_id,
                           humidity_sensor.sensor_id,
                           pollution_sensor.sensor_id
                       ])

session.add(czestochowa_city)
session.add(myszkow_city)
session.add(krzepice_city)
session.commit()