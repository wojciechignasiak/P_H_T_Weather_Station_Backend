# if build.sh not working try adding +x parameter:
# $ chmod +x build.sh
echo "++++++Building PHT project for the first time++++++"
cp ./pht_backend/src/db_connector/models.py ./utils/models.py
sudo docker-compose up -d --build
echo "++++++Initializing Postgres DB++++++"
sleep 10
sudo python3 ./utils/db_init.py
echo "++++++Creating new InfluxDB Token++++++"
y=$(sudo docker exec -it InfluxDB influx auth create -o pht -d pht_token --read-buckets --write-buckets | grep '\=' | awk '{print $3}')
echo "++++++Copy this Token to your docker-compose.yml: "
echo $y
sudo env_var="INFLUX_TOKEN_ENV=${y}"
echo $env_var > .env
source .env
echo "++++++Rebuilding necessary containers++++++"
sudo docker-compose up -d --build
echo "++++++Building done check results by visiting++++++"
echo "http://localhost:8000/docs"
