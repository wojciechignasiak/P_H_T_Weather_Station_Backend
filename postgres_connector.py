from sqlalchemy.engine import create_engine
from models import City, Sensor
from sqlalchemy.orm import sessionmaker


class PostgresConnector:
    def __init__(self, user, password, url, port=5438) -> None:
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

    def get_city(self):
        city = self._session.query(City).all()
        return city

    def get_sensor(self):
        sensor = None
        with self.Session() as session:
            with session.begin():
                sensor = session.query(Sensor).all()
        return sensor


# records = session.query(Cities).all()

# for record in records:
#     print(record)
