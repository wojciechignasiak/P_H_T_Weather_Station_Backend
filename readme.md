# **PHT Weather Station - Backend**

## **General info**

<br>

    PHT Weather Station is a project created by group of students from the Częstochowa University of Technology. 
    The project goal was to create a Service that will measure
    temperature, air humidity and pollution in the 
    cities of Częstochowa, Myszków and Krzepice
    located in Silesia in Poland.

<br>

## **Setup - Linux Ubuntu <img src="readme_images/linuxicon.png" alt="Linux Icon" width="32"/>**
    
        
    1. Open P_H_T_Weather_Station_Backend folder.
    2. Install Docker-compose.
    3. Start command:
        
        ./build.sh

    4. Done

## **Project Structure Diagram**

<br>

![Project Structure](readme_images/SystemDiagram.png)

<br>

## **How it works? - Backend**

<br>

#### **Docker-compose**

    Backend layer has been built on Docker-Compose containers technology:

![Docker-compose](readme_images/dockercompose.png)

<br>

#### **MQTT Bridge**

    MQTT Bridge receives data with 
    structure "pht/city/{city_id}/sensor/{sensor_id}, "sensor_data""
    send by electronic sensors on {ip_adress}:1883 adress. 
    Then MQTT breake the structure into InfluxDB topics:

![MQTT](readme_images/mqttbridge.png)

<br>

#### **InfluxDB**

    MQTT correctly transfers data and topics structure to InfluxDB and by 
    Explore tab we can see collected data:

![InfluxDB](readme_images/influxdb.png)

<br>

#### **PostgreSQL**

    We use PostgreSQL to store the names of cities, sensors and units of measurement.
    In addition, we structure them by, for example, giving them identification 
    numbers, which help us to provide endpoints.
    These endpoints only use PostgreSQL and show the adopted data organization:

![Postgres Structure](readme_images/PostgreSQL.png)

<br>

#### **FastAPI**

    We decided to use FastAPI due to its speed and lightness, which is 
    perfect for our small project. In FastAPI we connect to PostgreSQL 
    and InfluxDB to provide structured data in the form of endpoints.
    You can check all enpoints on {ip_adress}/docs.
    Here is an example:

![FastAPI](readme_images/fastAPI.png)

<br>

## **Endpoint list:**

<br>

Endpoint:

```
/cities
```

Example request:

**`http://localhost:8081/cities`**

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
  "detail": "No cities in database."
}
```

<br><br>

### **GET sensors**

Endpoint:

```
/sensors
```

Example request:

**`http://localhost:8081/sensors`**

Example success response:

```json
{
  "sensors": [
    {
      "id": 1,
      "sensor_name": "Temperature",
      "unit": "Celsius"
    },
    {
      "id": 2,
      "sensor_name": "Humidity",
      "unit": "Percentage"
    },
    {
      "id": 3,
      "sensor_name": "Pollution",
      "unit": "PM2.5"
    }
  ]
}
```

Example error response:

```json
{
  "detail": "No sensors in database."
}
```

<br><br>

### **GET city readings**

Endpoint:

```
/readings/{city_id}
```

Example request:

**`http://localhost:8081/readings/1`**

Example success response:

```json
{
  "Temperature": 21.37,
  "Humidity": 60.17,
  "Pollution": 80.37
}
```

Example error response:

```json
{
  "detail": "No measurements has been found."
}
```

<br><br>

### **GET city specific sensor readings**

Endpoint:

```
/readings/{city_id}/{sensor_id}
```

Example request:

**`http://localhost:8081/readings/1/0`**

Example success response:

```json
{
  "Humidity": 60.00
}
```

Example error response:

```json
{
  "detail": "No measurements has been found."
}
```

<br><br>

### **GET city readings from given date**

Date format (iso8601): `YYYY-MM-DDThh:mm:ssZ`\
Date example: `2021-10-22T00:09:00Z`

Endpoint:

```
/readings-date/{city_id}/{year}-{month}-{day}T{hour}:{minutes}:00Z
```

Example request:

**`http://localhost:8081/readings-date/1/2021-10-22T00:09:00Z`**

Example success response:

```json
{
  "Temperature": 21.37,
  "Humidity": 60.00,
  "Pollution": 25.17
}
```

Example error response:

```json
{
  "detail": "No measurements has been found."
}
```
