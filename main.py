import uvicorn
from fastapi import FastAPI, Path
from postgres_connector import PostgresConnector

app = FastAPI()


@app.get("/cities")
def get_cities():
    pc = PostgresConnector("postgres", "1234", "localhost")
    pc.connect()
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


@app.get("/sensors")
def get_sensors():
    pc = PostgresConnector("postgres", "1234", "localhost")
    pc.connect()
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


@app.get("/readings/{city_id}")
def get_city_readings(city_id: int):
    pc = PostgresConnector("postgres", "1234", "localhost")
    pc.connect()
    cities = pc.get_cities()
    xd = next((x for x in cities if x.id == city_id), None)
    readings = {}
    for sensor in xd.sensors:
        readings[sensor.name] = "chuj"

    return readings


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
