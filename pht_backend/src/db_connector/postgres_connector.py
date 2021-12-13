from sqlalchemy.engine import create_engine
from db_connector.models import City, Sensor
from sqlalchemy.orm import sessionmaker


class PostgresConnector:
    def __init__(self, user, password, url, port=5432) -> None:
        self._user = user
        self._password = password
        self._url = url
        self._port = port
        self._db_string = f"postgresql://{self._user}:{self._password}@{self._url}:{self._port}"
        self._engine = None
        self.Session = None
        self._session = None

    def connect(self):
        self._engine = create_engine(self._db_string)
        self.Session = sessionmaker(bind=self._engine)
        self._session = self.Session()
        print("Postgres connected")

    def get_cities(self):
        cities = self._session.query(City).all()
        return cities

    def get_sensors(self):
        sensors = self._session.query(Sensor).all()
        return sensors
