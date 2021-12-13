from fastapi import APIRouter
from db_connector.postgres_connector import PostgresConnector
from influx_connector.influx_connector import InfluxConnector


router = APIRouter()
pc = PostgresConnector("postgres", "1234", "0.0.0.0")
pc.connect()
# ic = InfluxConnector()


@router.get("/cities")
def get_cities():
    results = pc.get_cities()
    city_list = []
    for result in results:
        sensor_list = []
        for sensor in result.sensors:
            sensor_list.append(sensor.id)
        city = {
            "id": result.id,
            "city_name": result.name,
            "sensor_list": sensor_list
        }
        city_list.append(city)

    return city_list


@router.get("/sensors")
def get_sensors():
    results = pc.get_sensors()
    sensor_list = []
    for result in results:
        sensor = {
            "id": result.id,
            "sensor_name": result.name,
            "unit": result.unit
        }
        sensor_list.append(sensor)

    return sensor_list


@router.get("/readings/{city_id}")
def get_city_readings(city_id: int):
    cities = pc.get_cities()
    city = next((x for x in cities if x.id == city_id), None)
    readings = {}
    for sensor in city.sensors:
        readings[sensor.name] = "kotek"

    return readings


@router.get("/readings/{city_id}/{sensor_id}")
def get_exact_sensor(city_id: int, sensor_id: int):
    cities = pc.get_cities()
    # sensor_readings = ic.get_data(city_id, sensor_id)
    # print(sensor_readings)
    city = next((x for x in cities if x.id == city_id), None)
    readings = {}
    for sensor in city.sensors:
        if sensor.id == sensor_id:

            readings[sensor.name] = "sensor_readings"

    return readings
