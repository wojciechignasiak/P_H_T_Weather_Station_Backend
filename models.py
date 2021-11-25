from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

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
