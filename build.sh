# if build.sh not working try adding +x parameter:
# $ chmod +x build.sh
echo "++++++Building PHT project for the first time++++++"
cp ./pht_backend/src/db_connector/models.py ./utils/models.py
docker-compose up -d --build
pip install -r ./utils
echo "++++++Initializing Postgres DB++++++"
sleep 30
python3 ./utils/db_init.py
echo "++++++Creating new InfluxDB Token++++++"
y=$(docker exec -it InfluxDB influx auth create -o pht -d pht_token --read-buckets --write-buckets | grep '\=' | awk '{print $3}')
env_var="INFLUX_TOKEN_ENV=${y}"
echo $env_var > .env
source .env
echo "++++++Rebuilding necessary containers++++++"
docker-compose up -d --build
echo "++++++Building done check results by visiting++++++"
echo "http://localhost:8000/docs"

