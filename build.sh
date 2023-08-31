# if build.sh not working try adding +x parameter:
# $ chmod +x build.sh
echo "++++++Building PHT project for the first time++++++"
docker-compose up -d --build
echo "++++++Creating new InfluxDB Token++++++"
sleep 10
y=$(docker exec -it influxdb influx auth create -o pht -d pht_token --read-buckets --write-buckets | grep '\=' | awk '{print $3}')
env_var="INFLUX_TOKEN=${y}"
echo "" >> .env
echo $env_var >> .env
source .env
echo "++++++Rebuilding necessary containers++++++"
docker-compose up -d --build
echo "++++++Building done check results by visiting++++++"
echo "http://localhost:8081/docs"
