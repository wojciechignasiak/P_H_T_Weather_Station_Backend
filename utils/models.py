from sqlalchemy import Column, String, Integer, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey

base = declarative_base()

city_m2m_sensor = Table('city_m2m_sensor', base.metadata,
                        Column('cities_id', Integer, ForeignKey('Cities.id')),
                        Column('sensors_id', Integer,
                               ForeignKey('Sensors.id')),
                        )


class City(base):
    __tablename__ = 'Cities'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String)
    sensors = relationship(
        'Sensor', secondary=city_m2m_sensor, backref=backref('Cities'))


class Sensor(base):
    __tablename__ = 'Sensors'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String)
    unit = Column(String)
