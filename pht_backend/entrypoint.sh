#!/bin/sh

echo "Waiting for Postgres..."

while ! nc -z postgresql 5432; do
  sleep 0.1
done

echo "Postgres started!"

echo "Waiting for Influx..."

while ! nc -z influxdb 8086; do
  sleep 0.1
done

echo "Influx started!"

exec "$@"