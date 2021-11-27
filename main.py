import uvicorn
from fastapi import FastAPI, Path
from postgres_connector import PostgresConnector

app = FastAPI()


@app.get("/cities")
def get_cities():
    results = pc.get_city()
    city_list = []
    for result in results:
        sensor_list = []
        for sensor in result.city_sensors:
            sensor_list.append(sensor.id)
        city = {
            "id": result.id,
            "city_name": result.city_name,
            "sensor_list": sensor_list
        }
        city_list.append(city)

    return city_list


if __name__ == "__main__":
    pc = PostgresConnector("postgres", "1234", "localhost")
    pc.connect()
    uvicorn.run(app, host="0.0.0.0", port=8000)
