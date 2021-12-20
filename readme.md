# **PHT Wheather Checker - Backend**

## **General info**

<br>

    PHT is a project created by group of students. The project goal was to create a Web Service that will measure temperature, air humidity and pollution in the cities of Częstochowa, Myszków and Krzepice located in Silesia in Poland.

<br>

## **Setup**

    1. Install:

        Docker
        Docker-compose

    2. Start Terminal
    3. Get to P_H_T_Project_Backend folder.
    4. Start command:

        sudo ./build.sh

    5. Done

## **Project Structure Diagram**

<br>

![Project Structure](readme_images/SystemDiagram.png)

<br>

## **PostgreSQL Structure Diagram**

<br>

![Postgres Structure](readme_images/PostgreSQL.png)

<br>

## **Technologies**

<br>

### Docker-compose

<br>

### FastAPI

<br>

### MQTT Bridge

<br>

### MQTT Broker (docker image)

    toke/mosquitto

### PostgreSQL (docker image)

    postgres:14.0

### InfluxDB >2.0 (docker image)

    influxdb:latest

## **Endpoint list:**

<br>

Endpoint:

```
/cities
```

Example request:

**`http://178.43.161.159/cities`**

Example success response:

```json
{
  "cities": [
    {
      "id": 1,
      "city_name": "Czestochowa",
      "sensor_list": [1, 2, 3]
    },
    {
      "id": 2,
      "city_name": "Myszkow",
      "sensor_list": [1, 2, 3]
    },
    {
      "id": 3,
      "city_name": "Krzepice",
      "sensor_list": [1, 2, 3]
    }
  ]
}
```

Example error response:

```json
{
  "error_code": "4040",
  "error_message": "Internal server error"
}
```

<br><br>

### **GET sensors**

Endpoint:

```
/sensors
```

Example request:

**`http://178.43.161.159/sensors`**

Example success response:

```json
{
  "sensors": [
    {
      "id": 1,
      "sensor_name": "temperature",
      "unit": "Celsius degrees"
    },
    {
      "id": 2,
      "sensor_name": "humidity",
      "unit": "percent"
    }
    {
      "id": 3,
      "sensor_name": "pollution",
      "unit": "PM2.5"
    }
  ]
}
```

Example error response:

```json
{
  "error_code": "4040",
  "error_message": "Internal server error"
}
```

<br><br>

### **GET city readings**

Endpoint:

```
/readings/{city_id}
```

Example request:

**`http://178.43.161.159/readings/1`**

Example success response:

```json
{
  "temperature": "20",
  "humidity": "60",
  "pollution": "10"
}
```

Example error response:

```json
{
  "error_code": "4041",
  "error_message": "City does not exist"
}
```

<br><br>

### **GET city exact sensor readings**

Endpoint:

```
/readings/{city_id}/{sensor_id}
```

Example request:

**`http://178.43.161.159/readings/1/0`**

Example success response:

```json
{
  "humidity": "60"
}
```

Example error response:

```json
{
  "error_code": "4042",
  "error_message": "Sensor does not exist"
}
```

<br><br>
