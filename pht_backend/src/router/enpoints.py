from fastapi import APIRouter
from db_connector.postgres_connector import PostgresConnector
from influx_connector.influx_connector import InfluxConnector
import os

router = APIRouter()
postgres_login = os.environ.get("POSTGRES_LOGIN")
postgres_pass = os.environ.get("POSTGRES_PASSWORD")
postgres_url = os.environ.get("POSTGRES_URL")
pc = PostgresConnector(postgres_login, postgres_pass, postgres_url)
pc.connect()
ic = InfluxConnector()


@router.get("/")
def get_index():
    return "Welcome to PHT backend"


@router.get("/cities")
def get_cities():
    results = pc.get_cities()
    city_list = []
    try:
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
    except:
        city_list = {
            "error_code": 4040,
            "error_message": "Internal server error"
        }

    return city_list


@router.get("/sensors")
def get_sensors():
    results = pc.get_sensors()
    sensor_list = []
    try:
        for result in results:
            sensor = {
                "id": result.id,
                "sensor_name": result.name,
                "unit": result.unit
            }
            sensor_list.append(sensor)
    except:
        sensor_list = {
            "error_code": 4040,
            "error_message": "Internal server error"
        }
    return sensor_list


@router.get("/readings")
def readings_info():
    return {
        "error_code": 4045,
        "error_message": "Specify at least city"
    }


@router.get("/readings/{city_id}")
def get_city_readings(city_id: int):
    cities = pc.get_cities()
    try:
        city_readings = ic.get_city_data(city_id)
        city = next((x for x in cities if x.id == city_id), None)
        readings = {}
        for i, sensor in enumerate(city.sensors):
            readings[sensor.name] = city_readings[i]
    except:
        readings = {
            "error_code": 4041,
            "error_message": "City does not exist"
        }
    return readings


@router.get("/readings/{city_id}/{sensor_id}")
def get_exact_sensor(city_id: int, sensor_id: int):
    cities = pc.get_cities()
    try:
        sensor_readings = ic.get_sensor_data(city_id, sensor_id)
        city = next((x for x in cities if x.id == city_id), None)
        readings = {}
        for sensor in city.sensors:
            if sensor.id == sensor_id:
                readings[sensor.name] = sensor_readings[0]
    except:
        readings = {
            "error_code": 4042,
            "error_message": "Sensor or city does not exist"
        }
    return readings


@router.get("/readings-date/{city_id}/{year}-{month}-{day}T{hour}:{minutes}:00Z")
def get_city_readings_from_date(city_id: int, year: int, month: int, day: int, hour: int, minutes: int):
    cities = pc.get_cities()
    hour = hour - 1  # diferent time zone in InfluxDB
    try:
        city_readings = ic.get_city_data_from_date(
            city_id, year, month, day, hour, minutes)
        print(city_readings)
        city = next((x for x in cities if x.id == city_id), None)
        readings = {}
        print(readings)
        for i, sensor in enumerate(city.sensors):
            readings[sensor.name] = city_readings[i]
    except:
        readings = {
            "error_code": 4041,
            "error_message": "City does not exist or date has been given in wrong format"
        }
    return readings
