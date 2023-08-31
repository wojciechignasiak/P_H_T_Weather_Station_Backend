#!/bin/sh

echo "Waiting for MQTT Broker..."

while ! nc -z mqtt 1883; do
  sleep 0.1
done

echo "MQTT Broker started!"

echo "Waiting for Influx..."

while ! nc -z influxdb 8086; do
  sleep 0.1
done

echo "Influx started!"

exec "$@"